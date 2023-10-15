
from nacl.public import PrivateKey, PublicKey
import base64

class keySerialization:
    @staticmethod
    def serializePrivateKey(privateKey):
        return privateKey.encode()

    @staticmethod
    def deserializePrivateKeyPemFromString(KeyBytes):
        return PrivateKey(KeyBytes)


    @staticmethod
    def serializePublicKeyToString(public_key):
        return base64.b64encode(public_key.encode()).decode()
    
    @staticmethod
    def serializePublicKeyToBytes(public_key):
        return public_key.encode()
    
    @staticmethod
    def deserializePublicKeyFromString(publicKeyString: str):
        return PublicKey(base64.b64decode(publicKeyString.encode()))
    
    @staticmethod
    def deserializePublicKeyFromBytes(publicKeyBytes: bytes):
        return PublicKey(publicKeyBytes)
   