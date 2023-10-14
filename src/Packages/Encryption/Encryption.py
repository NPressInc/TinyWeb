
from nacl.public import PrivateKey, PublicKey, SealedBox, Box
import os
import nacl.secret
import nacl.utils

class Encryption:

    TWDataHeader = b"::TWDataHeader::"

    @staticmethod
    def encryptDataForPublicKey(myPrivateKey, recipient_pub_key, data):
        
        bob_box = Box(myPrivateKey, recipient_pub_key)

        encrypted = bob_box.encrypt(data)

        return encrypted


    @staticmethod
    def decryptdataFromPrivateKey(myPrivateKey, sender_pub_key, data):

        box = Box(myPrivateKey, sender_pub_key)

        return box.decrypt(data)

    
    @staticmethod
    def encryptDataForMultiplePublicKeys(myPrivateKey, recipient_public_keys, data, generatedKey = None):

        encryptedKeys = []

        if generatedKey == None:
            generatedKey = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        
        box = nacl.secret.SecretBox(generatedKey)

        encryptedData  = box.encrypt(data)

        for recipient_public_key in recipient_public_keys:
            
            encryptedKeys.append(Encryption.encryptDataForPublicKey(myPrivateKey,recipient_public_key,generatedKey))
        
        return {"EncryptedData": encryptedData, "EncryptedKeys": encryptedKeys}

    @staticmethod
    def decryptDataFromMultiEncryptedData(myPrivateKey, sender_public_key, encryptedKeys,data):
        # Perform key derivation.
        decryptedKey = None
        for key in encryptedKeys:
            try:
                decryptedKey = Encryption.decryptdataFromPrivateKey(myPrivateKey, sender_public_key, key)
                break
            except:
                continue

        if decryptedKey == None:
            raise Exception("No Encrypted Keys Matched. No access given")

        box = nacl.secret.SecretBox(decryptedKey)
        finalData = box.decrypt(data)

        return finalData
