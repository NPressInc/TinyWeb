import nacl.utils
from nacl.public import PrivateKey, Box, PublicKey
from nacl.signing import SignedMessage

from Packages.Serialization.Serialization import Serialization
from nacl.signing import SigningKey, VerifyKey
import base64
from nacl.exceptions import BadSignatureError
from Packages.Structures.Signature import Signature

class Signing:
    
    @staticmethod
    def normalSigning(private_key: PrivateKey, data)->str:
        PKBytes = private_key.encode()

        signing_key = SigningKey(PKBytes)

        data = data.encode()

        signed_message = Signature(signing_key.sign(data))

        serialized_signed_message_base64 = signed_message.serialized

        return serialized_signed_message_base64
    
    
    def verifyStringSignatureData(public_key: PublicKey, signatureString) -> bool:
        data, signature = Signature.deserialize_from_string(signatureString)
        PKBytes = public_key.encode()
        verify_key = VerifyKey(PKBytes)
        try:
            verify_key.verify(data, signature)
            return True
        except:
            return False
        

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


     