
import binascii
from tokenize import String
from typing_extensions import IntVar
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from Packages.Serialization.Serialization import Serialization
from Packages.Serialization.keySerialization import keySerialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

import base64


class Encryption:

    TWDataHeader = b"::TWDataHeader::"

    @staticmethod
    def encryptDataForPublicKey(myPrivateKey, recipientPublicKeyString, data):

        recipientPublicKey = keySerialization.deserializePublicKey(recipientPublicKeyString)

        shared_key = myPrivateKey.exchange(
            ec.ECDH(), recipientPublicKey)
        
        key = Encryption.getDigest(shared_key)

        encrypted, iv = Encryption.AESEncrypt(key, data)

        return encrypted, iv



    @staticmethod
    def decryptdataFromPrivateKey(myPrivateKey, SenderPublicKeyString, data, iv):

        SenderPublicKey = keySerialization.deserializePublicKey(SenderPublicKeyString)

        same_shared_key = myPrivateKey.exchange(
            ec.ECDH(), SenderPublicKey)
        # Perform key derivation.
        key = Encryption.getDigest(same_shared_key)

        res = Encryption.AESDecrypt(key, data, iv)

        if res == None:
            print("Invalid Key")
        else:
            return res

    
    @staticmethod
    def encryptDataForMultiplePublicKeys(privateKey, recipientPublicKeyStrings, data, generatedKey = None):

        encryptedKeys = []
        ivs = []

        if generatedKey == None:
            generatedKey = os.urandom(32)

        

        encryptedData, MasterIv  = Encryption.AESEncrypt(generatedKey,data)

        for recipientPublicKeyString in recipientPublicKeyStrings:

            recipientPublicKey = keySerialization.deserializePublicKey(recipientPublicKeyString)
            shared_key = privateKey.exchange(
                ec.ECDH(), recipientPublicKey)
            # Perform key derivation.
            key = Encryption.getDigest(shared_key)

            

            cipherText, iv = Encryption.AESEncrypt(key, generatedKey)
            
            encryptedKeys.append(cipherText)
            ivs.append(iv)
        
        return {"EncryptedData": encryptedData, "iv": MasterIv, "EncryptedKeys": encryptedKeys, "ivs": ivs}
    @staticmethod
    def decryptDataFromMultiEncryptedData(myPrivateKey, senderPublicKeyString, encryptedKeys,data, iv, ivs):

        SenderPublicKey = keySerialization.deserializePublicKey(senderPublicKeyString)
        same_shared_key = myPrivateKey.exchange(
            ec.ECDH(), SenderPublicKey)
        # Perform key derivation.
        key = Encryption.getDigest(same_shared_key)

        for i in range(len(encryptedKeys)):
            decryptedKey = Encryption.AESDecrypt(key, encryptedKeys[i], ivs[i])
            if decryptedKey == None:
                continue
            else:
                break
        if decryptedKey == None:
            raise Exception("No Encrypted Keys Matched. No access given")

        finalData = Encryption.AESDecrypt(decryptedKey, data, iv)

        return finalData

    @staticmethod
    def AESEncrypt(key: bytearray, data: String):
        iv = os.urandom(16)
        data = Encryption.addTWHeader(data)
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return (ciphertext, iv)
        
        
    @staticmethod
    def AESDecrypt(key: bytearray, data: bytearray, iv: bytearray):
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        res = decryptor.update(data) + decryptor.finalize()
        if Encryption.checkForHeader(res):
            res = Encryption.removeTWHeader(res)
        else:
            return None
        return res
       
    @staticmethod
    def checkForHeader(data):
        if len(data) > 16:
            if data[:16] == Encryption.TWDataHeader:
                return True
        return False

    @staticmethod
    def removeTWHeader(data):
        if len(data) > 16:
            return data[16:]
        else:
            raise Exception("Data Length not sufficient")


    @staticmethod
    def addTWHeader(data):
        return Encryption.TWDataHeader + data


    @staticmethod
    def getDigest(inputBytes: bytearray):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt="null".encode("utf-8"),
            iterations=15000,
        )
        res = kdf.derive(inputBytes)
        return res

    @staticmethod
    def testEncrypt():
        data = b"hellofdsaafsdffasdf"

        print(data)

        digest = Encryption.getDigest(b"secret1")

        fakedigest = Encryption.getDigest(b"secret21")

        ciphertext, iv = Encryption.AESEncrypt(digest, data)

        print({"encData": ciphertext, "iv": iv})

        print(Encryption.AESDecrypt(key=fakedigest, data=ciphertext, iv=iv))


