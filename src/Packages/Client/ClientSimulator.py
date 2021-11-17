import requests

from ..Serialization.Serialization import Serialization
import time
import sys
from ..Verification.Signing import Signing
nodeId = 0
if len(sys.argv) > 2:
    nodeId = int(sys.argv[2])

class ClientSimulator:

    def __init__(self, privateKeySender,publicKeySender, publicKeyReciever):
        self.FauxTransactionList = []
        self.initTransactions(privateKeySender,publicKeySender, publicKeyReciever)

    def initTransactions(self, privateKeySender , publicKeySender, publicKeyReciever):


        message1 = "Lets Rage"

        message2 = "No, lets age"

        signature1 = Signing.normalSigning(privateKeySender, message1)
        signature2 = Signing.normalSigning(privateKeySender, message2)

        self.FauxTransactionList.append({"sender": publicKeySender, "receiver":publicKeyReciever, "content":message1, "signature": signature1})
        self.FauxTransactionList.append({"sender": publicKeySender, "receiver":publicKeyReciever, "content":message2, "signature": signature2})
        self.FauxTransactionList.append({"sender": publicKeySender, "receiver":publicKeyReciever, "content":message1, "signature": signature1})
        self.FauxTransactionList.append({"sender": publicKeySender, "receiver":publicKeyReciever, "content":message2, "signature": signature2})
        self.FauxTransactionList.append({"sender": publicKeySender, "receiver":publicKeyReciever, "content":message1, "signature": signature1})
        self.FauxTransactionList.append({"sender": publicKeySender, "receiver":publicKeyReciever, "content":message2, "signature": signature2})
        self.FauxTransactionList.append({"sender": publicKeySender, "receiver":publicKeyReciever, "content":message1, "signature": signature1})
        self.FauxTransactionList.append({"sender": publicKeySender, "receiver":publicKeyReciever, "content":message2, "signature": signature2})
        self.FauxTransactionList.append({"sender": publicKeySender, "receiver":publicKeyReciever, "content":message1, "signature": signature1})
        self.FauxTransactionList.append({"sender": publicKeySender, "receiver":publicKeyReciever, "content":message2, "signature": signature2})

        

    @staticmethod
    def sendTransaction(transactionObject):
        url = "http://127.0.0.1:"+ str(5000 + nodeId) +"/Transaction"
        data = Serialization.serializeObjToJson(transactionObject)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)
        print("sent Transaction")

    @staticmethod
    def sendRequestGroups(publicKeyString):
        url = "http://127.0.0.1:"+ str(5050 + nodeId) +"/GetAllGroups"
        data = Serialization.serializeObjToJson({"publicKey":publicKeyString})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)
        print(r.json)

    
    def sendTransactionsEverySoOften(self, secondsBetweenMessages, numberOfMessages):
        counter = 0
        while counter < numberOfMessages:
            counter += 1
            index = counter % (len(self.FauxTransactionList) - 1)
            time.sleep(secondsBetweenMessages)
            ClientSimulator.sendTransaction(self.FauxTransactionList[index])

