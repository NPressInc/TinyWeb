
from ..Serialization.Serialization import Serialization
import requests
import json

import sys
nodeId = 0
if len(sys.argv) > 2:
    nodeId = int(sys.argv[2])

class apiConnectorMethods:

    @staticmethod
    def getAllGroups(client):
        data = {
            "publicKey": client.publicKey.encode()
        }
        url = "http://127.0.0.1:"+ str(5050 + nodeId) +"/GetAllGroups"
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
            "publicKey": client.publicKey.encode()
        }
        url = "http://127.0.0.1:"+ str(5050 + nodeId) +"/GetSentMessages"
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
            "publicKey": client.publicKey.encode()
        }
        url = "http://127.0.0.1:"+ str(5050 + nodeId) +"/GetReceivedMessages"
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
        url = "http://127.0.0.1:"+ str(5000 + nodeId) +"/Transaction"
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