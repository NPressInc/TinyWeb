
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class keySerialization:
    @staticmethod
    def serializePrivateKey(privateKey: ec.EllipticCurvePrivateKey):
        PKBytes = privateKey.private_bytes(
            encoding = serialization.Encoding.PEM, 
            format=serialization.PrivateFormat.PKCS8, 
            encryption_algorithm = serialization.NoEncryption()
            )
        return PKBytes.decode("utf-8")

    @staticmethod
    def deserializePrivateKeyPemFromString(PEMString):
        private_key = serialization.load_pem_private_key(
                PEMString,
                password=None,
                backend=default_backend()
            )
        return private_key




    @staticmethod
    def serializePublicKey(public_key: ec.EllipticCurvePublicKey):
        public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_pem.decode("utf-8")

    @staticmethod
    def deserializePublicKey(PEMString):
        public_key = serialization.load_pem_public_key(
            PEMString,
            backend=default_backend()
        )
        return public_key