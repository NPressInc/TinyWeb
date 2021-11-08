import requests
from ..Serialization.Serialization import Serialization
import time

class ClientSimulator:

    def __init__(self):
        self.FauxTransactionList = []
        self.initTransactions()

    def initTransactions(self):

        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})
        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})
        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})
        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})
        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})
        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})
        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})
        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})
        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})
        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})
        self.FauxTransactionList.append({"from": "michel", "to":"jeffe", "content":"Lets Rage"})

        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})
        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})
        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})
        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})
        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})
        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})
        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})
        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})
        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})
        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})
        self.FauxTransactionList.append({"from": "jeffe", "to":"michel", "content":"yeah lets riot"})

        

    @staticmethod
    def sendTransaction(transactionObject):
        url = "http://127.0.0.1:5000/Transaction"
        data = Serialization.serializeObjToJson(transactionObject)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)
        print("Done Broadcasting new block")


    
    def sendTransactionsEverySoOften(self, secondsBetweenMessages, numberOfMessages):
        counter = 0
        while counter < numberOfMessages:
            counter += 1
            index = counter % (len(self.FauxTransactionList) - 1)
            time.sleep(secondsBetweenMessages)
            ClientSimulator.sendTransaction(self.FauxTransactionList[index])

