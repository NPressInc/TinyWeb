from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from Packages.Serialization.Serialization import Serialization

import json



class Signing:
    @staticmethod
    def normalSigning(private_key, data):
        data = data.encode()
        signature = private_key.sign(
            data,
            ec.ECDSA(hashes.SHA256())
        )
        return Serialization.serializeObjToJson(utils.decode_dss_signature(signature))

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
        data = data.encode()
        #print(type(signature))
        #print(signature)
        signature = json.loads(signature)
        #print(type(signature))
        #print(signature)
        signature = utils.encode_dss_signature(signature[0], signature[1])
        return public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))

     