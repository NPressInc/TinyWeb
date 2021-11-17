
import json

from cryptography.hazmat.primitives import serialization

from Packages.Serialization.Serialization import Serialization
from ..Verification.Signing import Signing

from ..Serialization.keySerialization import keySerialization



import time

import sys
nodeId = 0
if len(sys.argv) > 2:
    nodeId = int(sys.argv[2])

class TinyWebClient:
    def __init__(self, privateKey = None, publicKey = None,clientId = None ,LocationOn=None):
        self.__privateKey = privateKey
        self.publicKey = publicKey
        self.clientId = clientId
        self.LocationOn = LocationOn
    

    def signData(self, data):
        return Signing.normalSigning(self.__privateKey, data)


    def sendTestMessages(self, recipient):
        message1 = "Lets Rage"

        message2 = "No, lets age"

        senderPublicKeyString = keySerialization.serializePublicKey(self.publicKey)
        recipientKeyString = keySerialization.serializePublicKey(recipient.publicKey)

        FauxTransactionList = []

        for i in range(0,12):
            transaction1 = {"messageType": "SMS","sender": senderPublicKeyString, "receiver":recipientKeyString, "context":message1, "dateTime": time.time() + i}
            transaction2 = {"messageType": "SMS","sender": senderPublicKeyString, "receiver":recipientKeyString, "context":message2, "dateTime": time.time() + i}
            signature1 = Signing.normalSigning(self.__privateKey, Serialization.hashObject(transaction1))
            signature2 = Signing.normalSigning(self.__privateKey, Serialization.hashObject(transaction2))
            FauxTransactionList.append({"transaction":transaction1,"signature": signature1})
            FauxTransactionList.append({"transaction":transaction2, "signature": signature2})
            
        
        counter = 0
        numberOfMessages = 2000
        secondsBetweenMessages = 2

        while counter < numberOfMessages:
            counter += 1
            index = counter % (len(FauxTransactionList) - 1)
            time.sleep(secondsBetweenMessages)
            TinyWebClient.sendTransaction(FauxTransactionList[index])

    @staticmethod
    def sendTransaction(transactionObject):
        import requests
        url = "http://127.0.0.1:"+ str(5000 + nodeId) +"/Transaction"
        data = Serialization.serializeObjToJson(transactionObject)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)
        print("sent Transaction")

    @staticmethod
    def initializeClient(clientId):
        client = None
        try:
            __privateKey = Signing.PrivateKeyMethods.loadPrivateKeyClient(clientId)
            client = TinyWebClient(privateKey=__privateKey, publicKey=Signing.PrivateKeyMethods.generatePublicKeyFromPrivate(__privateKey), clientId=clientId,LocationOn= True)
            print("Loaded Client: " + clientId)
        except:
            client = TinyWebClient.initializeNewClient(clientId)
            Signing.PrivateKeyMethods.savePrivateKeyClient(client.__privateKey, clientId)
            print("Created New Client: " + clientId)

        return client
        

    @staticmethod
    def initializeNewClient(clientId):
        client = TinyWebClient()
        client.__privateKey = Signing.PrivateKeyMethods.generatePrivateKey()
        client.publicKey = Signing.PrivateKeyMethods.generatePublicKeyFromPrivate(client.__privateKey)
        client.LocationOn = True
        client.clientId = clientId

        return client


    def seriralizeJSON(self):
        outputObject = {
            "_privateKey": keySerialization.serializePrivateKey(self.__privateKey),
            "publicKey": keySerialization.serializePublicKey(self.publicKey),
            "LocationOn": self.LocationOn,
            "clientId": self.clientId
        }
        return json.dumps(outputObject, sort_keys=True)


    




    @staticmethod
    def deseriralizeJSON(jsonString):
        jsonDict = json.loads(jsonString)
        return TinyWebClient(**jsonDict)

    def getPeers(self):
        print("TBI")

    def sendTextMessage(self, Reciever, Message):
        print("TBI")
    
    def sendGroupMessage(self, RecievingGroup, Message):
        print("TBI")

    def broadcastGPSLocation(self, Location):
        print("TBI")

    def sendVoiceCallRequest(self, Reciever):
        print("TBI")

    def pollForUpdates(self):
        print("TBI")

    def sendGroupMessage(self, RecievingGroup, Message):
        print("TBI")



