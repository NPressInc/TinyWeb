import nacl.utils
from nacl.public import PrivateKey, Box

from Packages.Serialization.Serialization import Serialization
from nacl.signing import SigningKey, VerifyKey
import json
from nacl.exceptions import BadSignatureError


class Signing:
    
    @staticmethod
    def normalSigning(private_key, data):
        PKBytes = private_key.encode()

        signing_key = SigningKey(PKBytes)

        data = data.encode()

        signed_message = signing_key.sign(data)

        return Serialization.serializeObjToJson(signed_message)
        

    def verifyingTheSignature(public_key, signature, data):

        verify_key = VerifyKey(public_key)
        data = data.encode()
        try:
            # Verify the signature using the public key
            verify_key.verify(data, signature)
            print("Signature is valid.")
            return True
        except BadSignatureError:
            print("Signature is invalid.")
            return verify_key()


class PrivateKeyMethods:

    @staticmethod
    def generatePrivateKey() -> nacl.public.PrivateKey:
        skbob = PrivateKey.generate()
        return skbob

    @staticmethod
    def savePrivateKeyClient(privateKey: nacl.public.PrivateKey, clientId):
        PKBytes = privateKey.encode()
        with open("../src/State/private_keyClient" + str(clientId) + ".pem", 'wb') as f:
            f.write(PKBytes)

    @staticmethod
    def savePrivateKeyNode(privateKey: nacl.public.PrivateKey, nodeId):
        PKBytes = privateKey.encode()
        with open("../src/State/private_keyNode" + str(nodeId) + ".pem", 'wb') as f:
            f.write(PKBytes)

    @staticmethod
    def loadPrivateKeyClient(clientId):
        with open("../src/State/private_keyClient" + str(clientId) + ".pem", "rb") as key_file:
            private_key_bytes = key_file.read()
            private_key = PrivateKey(private_key_bytes)
            return private_key

    @staticmethod
    def loadPrivateKeyNode(nodeId):
        try:
            path = "../src/State/private_keyNode" + str(nodeId) + ".pem"
            print({"filePath": path})
            with open(path, "rb") as key_file:
                private_key_bytes = key_file.read()
                private_key = PrivateKey(private_key_bytes)
                return private_key
        except:
            print(f"No Private key found for nodeId {nodeId}")
    

    @staticmethod
    def generatePublicKeyFromPrivate(privateKey: nacl.public.PrivateKey):
        return privateKey.public_key


     