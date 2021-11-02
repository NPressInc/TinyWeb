from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


def normalSigning():
    private_key = ec.generate_private_key(
        ec.SECP384R1()
    )
    data = b"this is some data I'd like to sign"
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )


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

def verifyingTheSignature(public_key, signature, data):
    return public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))