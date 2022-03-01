
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from Packages.Serialization.Serialization import Serialization

class PrivateKeyMethods:

    @staticmethod
    def generatePrivateKey():
        private_key = ec.generate_private_key(ec.SECP384R1())
        return private_key

    @staticmethod
    def savePrivateKeyClient(privateKey: ec.EllipticCurvePrivateKey, clientId):
        PKBytes = privateKey.private_bytes(
            encoding = serialization.Encoding.PEM, 
            format=serialization.PrivateFormat.PKCS8, 
            encryption_algorithm = serialization.NoEncryption()
            )
        with open("State/private_keyClient" + str(clientId) + ".pem", 'wb') as f:
            f.write(PKBytes)

    @staticmethod
    def savePrivateKeyNode(privateKey: ec.EllipticCurvePrivateKey, nodeId):
        PKBytes = privateKey.private_bytes(
            encoding = serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8, 
            encryption_algorithm = serialization.NoEncryption()
            )
        with open("State/private_keyNode" + str(nodeId) + ".pem", 'wb') as f:
            f.write(PKBytes)

    @staticmethod
    def loadPrivateKeyClient(clientId):
        with open("State/private_keyClient" + str(clientId) + ".pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
            return private_key

    @staticmethod
    def loadPrivateKeyNode(nodeId):
        path = "State/private_keyNode" + str(nodeId) + ".pem"
        #print({"filePath": path})
        with open(path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
            return private_key
    

    @staticmethod
    def generatePublicKeyFromPrivate(privateKey: ec.EllipticCurvePrivateKey):
        return privateKey.public_key()