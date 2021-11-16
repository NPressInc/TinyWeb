from time import perf_counter
from flask import Flask, request, jsonify
from os import path


from ..Serialization.Serialization import Serialization

from ..structures.BlockChain.Block import Block

import json


class MessageQueues:
    messageQueues = None
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

MessageQueues.messageQueues = MessageQueues()


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/ProposeBlock", methods=['POST'])
def NewBlock():
    jsn = request.get_json()

    jsnString = json.dumps(jsn, indent=4, sort_keys=True)

    block = Block.deserializeJSON(jsnString)
    MessageQueues.messageQueues.PendingBlock = block

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
    chainMessage = request.get_json()
    print(chainMessage)
    MessageQueues.messageQueues.transactionQueue.append(chainMessage)
    return json.dumps({"status":"ok"})
    """
     except Exception as e: 
        print(e)
        return json.dumps({"status":str(e)})
    """
   


@app.route("/GetAllGroups", methods=['POST'])
def GetAllGroups():
    jsn = request.get_json()
    publicKey = jsn["PublicKey"]

    print(publicKey)

    return jsonify({"responsedddd": "okddd"})
