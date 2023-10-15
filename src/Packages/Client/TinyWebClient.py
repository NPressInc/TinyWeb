
import imp
import json
import numbers
from tokenize import Double

from Packages.Client.ApiConnector import apiConnectorMethods

from Packages.Serialization.Serialization import Serialization
from ..Verification.Signing import Signing, PrivateKeyMethods

from ..Serialization.keySerialization import keySerialization
from ..Encryption.Encryption import Encryption

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from Packages.Serialization.Serialization import Serialization
from Packages.Serialization.keySerialization import keySerialization

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
    

    def signData(self, data) -> str:
        return Signing.normalSigning(self.__privateKey, data)
    

    def sendTextMessage(self, recipient, message):
        senderPublicKeyString = keySerialization.serializePublicKeyToString(self.publicKey)
        recipientKeyString = keySerialization.serializePublicKeyToString(recipient.publicKey)
        groupId = ""
        if recipient.clientId == "4" or self.clientId == "4":
            
            groupId = "fledgling"
        else:
            groupId = "number1"

        EncMessage, iv = self.encryptDataForPublicKey(self, recipientKeyString,message)

        conversationId = TinyWebClient.getConversationIdFromKeys(senderPublicKeyString, recipientKeyString)

        transaction = {"messageType": "SMS","sender": senderPublicKeyString, "receiver":recipientKeyString, "conversationId":conversationId, "iv":iv ,"context":EncMessage,"groupId":groupId, "dateTime": time.time()}

        signature = Signing.normalSigning(self.__privateKey, Serialization.hashObject(transaction))

        TinyWebClient.sendTransaction({"transaction":transaction, "signature": signature})

    @staticmethod
    def getConversationIdFromKeys(key1, key2): # this takes the keys of a conversation and creates a unique conversationID for the participants in the conversation. This makes it easy for the clients to recal a conversation based on Id or by the participants
        concat = (key1 + key2)

        import hashlib

        encoded = concat.encode()

        hash = hashlib.sha256(encoded)

        return int(hash.hexdigest(),16)%(10 ** 8)



    def sendTestMessages(self, recipient):
        message1 = "Lets Rage"
        message2 = "No, lets age"

        senderPublicKeyString = keySerialization.serializePublicKeyToString(self.publicKey)
        recipientKeyString = keySerialization.serializePublicKeyToString(recipient.publicKey)

        FauxTransactionList = []

        for i in range(0,1000):
            transaction1 = {"messageType": "SMS","sender": senderPublicKeyString, "receiver":recipientKeyString, "context":message1, "dateTime": time.time() + i}
            transaction2 = {"messageType": "SMS","sender": senderPublicKeyString, "receiver":recipientKeyString, "context":message2, "dateTime": time.time() + i}
            signature1 = Signing.normalSigning(self.__privateKey, Serialization.hashObject(transaction1))
            signature2 = Signing.normalSigning(self.__privateKey, Serialization.hashObject(transaction2))
            FauxTransactionList.append({"transaction":transaction1,"signature": signature1})
            FauxTransactionList.append({"transaction":transaction2, "signature": signature2})
            
        
        counter = 0
        numberOfMessages = 200
        secondsBetweenMessages = 0.5

        while counter < numberOfMessages:
            counter += 1
            index = counter % (len(FauxTransactionList) - 1)
            time.sleep(secondsBetweenMessages)
            TinyWebClient.sendTransaction(FauxTransactionList[index])

    @staticmethod
    def sendTransaction(transactionObject):
        import requests
        print("about to send transaction")
        url = "http://127.0.0.1:"+ str(5000 + nodeId) +"/Transaction"
        data = Serialization.serializeObjToJson(transactionObject)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)
        if r.status_code == requests.codes.ok:
            data = Serialization.deserializeObjFromJsonR(r.text)
            print(data)

        print("sent Transaction")

    @staticmethod
    def initializeClient(clientId):
        client = None
        try:
            __privateKey = PrivateKeyMethods.loadPrivateKeyClient(clientId)
            client = TinyWebClient(privateKey=__privateKey, publicKey=PrivateKeyMethods.generatePublicKeyFromPrivate(__privateKey), clientId=clientId,LocationOn= True)
            print("Loaded Client: " + clientId)
        except:
            client = TinyWebClient.initializeNewClient(clientId)
            PrivateKeyMethods.savePrivateKeyClient(client.__privateKey, clientId)
            print("Created New Client: " + clientId)

        return client
        

    @staticmethod
    def initializeNewClient(clientId):
        client = TinyWebClient()
        client.__privateKey = PrivateKeyMethods.generatePrivateKey()
        client.publicKey = PrivateKeyMethods.generatePublicKeyFromPrivate(client.__privateKey)
        client.LocationOn = True
        client.clientId = clientId

        return client


    def seriralizeJSON(self):
        outputObject = {
            "_privateKey": keySerialization.serializePrivateKey(self.__privateKey).decode("utf-8"),
            "publicKey": keySerialization.serializePublicKeyToString(self.publicKey).decode("utf-8"),
            "LocationOn": self.LocationOn,
            "clientId": self.clientId
        }
        return json.dumps(outputObject, sort_keys=True)


    @staticmethod
    def deseriralizeJSON(jsonString):
        jsonDict = json.loads(jsonString)
        return TinyWebClient(**jsonDict)




    def createGroup(self, groupMembers, groupDesctiption):
        groupId = Serialization.hashString(groupMembers[0] + str(time.time())) #random string to be groupID. Realized that I cant identify via hash becuase groups can change.
        groupDef = {
                "messageType": "GroupDescriptor",
                "sender": keySerialization.serializePublicKeyToString(self.publicKey),
                "groupType": "People",
                "entities": groupMembers,
                "description": groupDesctiption,
                "groupId": groupId
            }
        groupHash = Serialization.hashObject(groupDef)

        signature = Signing.normalSigning(self.__privateKey, groupHash)

        data = {
            "transaction":groupDef,
            "signature":signature
        }

        apiConnectorMethods.sendTransaction(data)

    def encryptDataForMultiplePublicKeys(self, recipientPublicKeyStrings, data):
        return Encryption.encryptDataForMultiplePublicKeys(self.__privateKey, recipientPublicKeyStrings, data)


    def decryptDataFromMultiEncryptedData(self, senderPublicKeyString, encryptedKeys,data, iv, ivs):
        return Encryption.decryptDataFromMultiEncryptedData(self.__privateKey, senderPublicKeyString, encryptedKeys,data, iv, ivs)


    def encryptDataForPublicKey(self, recipientPublicKeyString, data):
        return Encryption.encryptDataForPublicKey(self.__privateKey, recipientPublicKeyString, data)


    def decryptdata(self, SenderPublicKeyString, data):
        return Encryption.decryptdata(self.__privateKey, SenderPublicKeyString, data)


    def getPeers(self):
        print("TBI")
    
    def sendGroupMessage(self, RecievingGroup, Message):
        print("TBI")

    def broadcastGPSLocation(self, Location):
        print("TBI")

    def sendVoiceCallRequest(self, Receiver):
        print("TBI")

    def pollForUpdates(self):
        print("TBI")

    def sendGroupMessage(self, RecievingGroup, Message):
        print("TBI")



