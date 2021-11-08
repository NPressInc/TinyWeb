from time import perf_counter
from flask import Flask, request
from os import path

from ..Serialization.Serialization import Serialization

from ..structures.BlockChain.Block import Block

import json

class MessageQueues:
    def __init__(self):
        self.transactionQueue = []
        self.PendingBlock = None
        self.validationVotes = []
        self.commitVotes = []
    
    def getPendingBlock(self):
        return self.PendingBlock

    def setPendingBlock(self, PendingBlock):
        self.PendingBlock = PendingBlock

    def getPtransactionQueue(self):
        return self.transactionQueue

    def setTransactionQueue(self, transactionQueue):
        self.transactionQueue = transactionQueue

messageQueues = MessageQueues()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/ProposeBlock", methods=['POST'])
def NewBlock():
    jsn = request.get_json()
    print({"JSn we are working with ": jsn})
    jsn["TransactionIndexMap"] = json.dumps(jsn["TransactionIndexMap"] , indent=4, sort_keys=True)

    jsnString = json.dumps(jsn , indent=4, sort_keys=True)
    print({"request": request})
    print({"should be a json string": jsnString})
    block = Block.deserializeJSON(jsnString)
    messageQueues.PendingBlock = block



    return "<p>Thank you for proposing your new block!</p>"

@app.route("/BlockVerified")
def BlockVerified():
    return "<p>Hello, World!</p>"

@app.route("/BlockCommitted")
def BlockCommitted():
    return "<p>Hello, World!</p>"

@app.route("/CheckBlockChain")
def CheckBlockChain():
    return "<p>Hello, World!</p>"

@app.route("/Transaction", methods=['POST'])
def Transaction():
    jsn = request.get_json()
    try:
        chainMessage = {
            "Address1": jsn["from"],
            "Type": "SMS",
            "Address2": jsn["to"],
            "Content": jsn["content"]
        }
        chainMessageString = Serialization.serializeObjToJson(chainMessage)
        print({"chainMessageString": chainMessageString})
        messageQueues.transactionQueue.append(chainMessageString)

        return "<p>Message Queued!</p>"

    except:
        return "<p>Something Went Wrong</p>"

    
    

