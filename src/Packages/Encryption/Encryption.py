from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from Packages.Serialization.Serialization import Serialization
from Packages.Serialization.keySerialization import keySerialization

from cryptography.fernet import Fernet

import json



class Encryption:
    @staticmethod
    def encryptDataForPublicKey(myPrivateKey, recipientPublicKeyString, data):

        recipientPublicKey = keySerialization.deserializePublicKey(recipientPublicKeyString)

        shared_key = myPrivateKey.exchange(
            ec.ECDH(), recipientPublicKey)
        # Perform key derivation.
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)

        print(type(derived_key))
        print(derived_key)

        f = Fernet(derived_key)

        return f.encrypt(data)



    def decryptdata(myPrivateKey, SenderPublicKeyString, data):

        SenderPublicKey = keySerialization.deserializePublicKey(SenderPublicKeyString)

        same_shared_key = myPrivateKey.exchange(
            ec.ECDH(), SenderPublicKey)
        # Perform key derivation.
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(same_shared_key)

        print(type(derived_key))
        print(derived_key)

        f = Fernet(derived_key)

        return f.decrypt(data)




