
from ..Serialization.Serialization import Serialization
from ..Serialization.keySerialization import keySerialization
import requests

class apiConnectorMethods:

    @staticmethod
    def getAllGroups(client):
        print("Getting groups where I am a member")
        print(client.publicKey)
        data = {
            "publicKey": keySerialization.serializePublicKey(client.publicKey)
        }
        url = "http://127.0.0.1:5001/GetAllGroups"
        data = Serialization.serializeObjToJson(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)
        print(r.content.decode())



    @staticmethod
    def sendTransaction(transactionObject):
        url = "http://127.0.0.1:5000/Transaction"
        data = Serialization.serializeObjToJson(transactionObject)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)
        print("Done Broadcasting new block")