from time import perf_counter
from flask import Flask, request, jsonify
from os import path


from ..Serialization.Serialization import Serialization

from ..structures.BlockChain.Block import Block

import json


class MessageQueues:
    messageQueues = None
    transactionQueue = []
    PendingBlock = None
    validationVotes = []
    commitMessages = []




app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/ProposeBlock", methods=['POST'])
def NewBlock():
    jsn = request.get_json()

    jsnString = json.dumps(jsn, indent=4, sort_keys=True)

    block = Block.deserializeJSON(jsnString)
    MessageQueues.PendingBlock = block

    return "<p>Thank you for proposing your new block!</p>"


@app.route("/VerificationVote", methods=['POST'])
def VerificationVote():
    
    voteJson = request.get_json()
    print(voteJson)
    MessageQueues.validationVotes.append(voteJson['vote'])
    print(MessageQueues.validationVotes)

    return jsonify({"response": "ok"})



@app.route("/CommitVote", methods=['POST'])
def CommitVote():
    voteJson = request.get_json()
    print(voteJson)
    MessageQueues.commitMessages.append(voteJson['vote'])

    print(MessageQueues.commitMessages)

    return jsonify({"response": "ok"})


@app.route("/CheckBlockChain")
def CheckBlockChain():
    return "<p>Hello, World!</p>"


@app.route("/Transaction", methods=['POST'])
def Transaction():
    chainMessage = request.get_json()
    print(chainMessage)
    MessageQueues.transactionQueue.append(chainMessage)
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
