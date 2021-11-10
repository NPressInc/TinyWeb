from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class Signing:


    class PrivateKeyMethods:

        @staticmethod
        def generatePrivateKey():
            private_key = ec.generate_private_key(ec.SECP384R1())
            return private_key

        @staticmethod
        def savePrivateKey(privateKey: ec.EllipticCurvePrivateKey, clientId):
            PKBytes = privateKey.private_bytes(
                encoding = serialization.Encoding.PEM, 
                format=serialization.PrivateFormat.PKCS8, 
                encryption_algorithm = serialization.NoEncryption()
                )
            with open("State/private_key" + clientId + ".pem", 'wb') as f:
                f.write(PKBytes)

        @staticmethod
        def loadPrivateKey(clientId):
            with open("State/private_key" + clientId + ".pem", "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
                return private_key

        

        @staticmethod
        def generatePublicKeyFromPrivate(privateKey: ec.EllipticCurvePrivateKey):
            return privateKey.public_key()

        

        
        


    

    
    @staticmethod
    def normalSigning():
        
        private_key = ec.generate_private_key(
            ec.SECP384R1()
        )
        data = b"this is some data I'd like to sign"
        signature = private_key.sign(
            data,
            ec.ECDSA(hashes.SHA256())
        )

    @staticmethod
    def largeDataSigning():
        
        private_key = ec.generate_private_key(
            ec.SECP384R1()
        )
        chosen_hash = hashes.SHA256()
        hasher = hashes.Hash(chosen_hash)
        hasher.update(b"data & ")
        hasher.update(b"more data")
        digest = hasher.finalize()
        sig = private_key.sign(
            digest,
            ec.ECDSA(utils.Prehashed(chosen_hash))
        )
        
    #public_key = private_key.public_key()
    def verifyingTheSignature(public_key, signature, data):
        return public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))

     