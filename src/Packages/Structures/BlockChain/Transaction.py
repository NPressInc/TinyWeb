from nacl.public import PublicKey
import hashlib
import base64
import json
from Packages.Structures.Signature import Signature

class Transaction:
    def __init__(self, messageType: str, peers: list[str], publicKeys: list[PublicKey], ids: list[int], sender: PublicKey, signatureStr:str = None ):
        self.messageType = messageType
        self.peers = peers
        self.publicKeys = publicKeys
        self.ids = ids
        self.sender = sender
        self.signatureStr = signatureStr

    def hash(self) -> str:
        hash_input = ""
        hash_input += self.messageType
        for pk in self.publicKeys:
            hash_input += str(base64.b64encode(pk.encode()).decode())
        for id in self.ids:
            hash_input += str(id)
        hash_input += str(str(base64.b64encode(self.sender.encode()).decode()))
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    def serializeJson(self) -> str:
        data = {
            "messageType": self.messageType,
            "peers": self.peers,
            "publicKeys": [str(base64.b64encode(pk.encode()).decode()) for pk in self.publicKeys],
            "ids": self.ids,
            "sender": str(str(base64.b64encode(self.sender.encode()).decode()))
        }
        return json.dumps(data)
    
    @staticmethod
    def loadJson(json_dict):
        return Transaction(
            messageType = json_dict.get("messageType"),
            peers = json_dict.get("peers"),
            publicKeys=[PublicKey(base64.b64decode(base64Pk.encode())) for base64Pk in json_dict.get("publicKeys")],
            ids=json_dict.get("ids"),
            sender=PublicKey(base64.b64decode(json_dict.get("sender").encode()))
        )
    
    