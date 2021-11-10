
from ..Serialization.Serialization import Serialization
from ..Serialization.keySerialization import keySerialization
import requests
import json

class apiConnectorMethods:

    @staticmethod
    def getAllGroups(client):
        data = {
            "publicKey": keySerialization.serializePublicKey(client.publicKey)
        }
        url = "http://127.0.0.1:5001/GetAllGroups"
        data = Serialization.serializeObjToJson(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == requests.codes.ok:

            data = Serialization.deserializeObjFromJsonR(response.text)
            
            print(type(data))

            return data
        else:
            return None

    @staticmethod
    def getSentMessages(client):
        data = {
            "publicKey": keySerialization.serializePublicKey(client.publicKey)
        }
        url = "http://127.0.0.1:5001/GetSentMessages"
        data = Serialization.serializeObjToJson(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == requests.codes.ok:

            data = Serialization.deserializeObjFromJsonR(response.text)
            
            print(type(data))

            return data
        else:
            return None

    @staticmethod
    def getReceivedMessages(client):
        data = {
            "publicKey": keySerialization.serializePublicKey(client.publicKey)
        }
        url = "http://127.0.0.1:5001/GetReceivedMessages"
        data = Serialization.serializeObjToJson(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == requests.codes.ok:

            data = Serialization.deserializeObjFromJsonR(response.text)
            
            print(type(data))

            return data
        else:
            return None


    @staticmethod
    def sendTransaction(transactionObject):
        url = "http://127.0.0.1:5000/Transaction"
        data = Serialization.serializeObjToJson(transactionObject)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == requests.codes.ok:

            print(response.text)

            data = Serialization.deserializeObjFromJsonR(response.text)
            
            print(type(data))

            return data
        else:
            return None