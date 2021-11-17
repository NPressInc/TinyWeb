from time import perf_counter
from flask import Flask, request, jsonify
from os import path

from Packages.Serialization.keySerialization import keySerialization


from ..Serialization.Serialization import Serialization

from ..structures.BlockChain.Block import Block

from ..pBFT.node import PBFTNode

from ..Verification.Signing import Signing

from ..Verification.BlockVerification import BlockVerification

import json

import time


def createBlock():
    transactions = []
    for tr in MessageQueues.transactionQueue.values():
        transactions.append(tr)

    newIndex = PBFTNode.node.blockChain.length
    timestamp = time.time()
    # print(timestamp)
    previousHash = PBFTNode.node.blockChain.last_block().getHash()
    proposerId = PBFTNode.node.id
    newIndex = PBFTNode.node.blockChain.length
    block = Block(newIndex, transactions, timestamp,
                previousHash, proposerId)
    
    
    return block

class MessageQueues:
    transactionQueue = {}
    PendingBlockDict = {}
    validationVotes = {}
    commitMessages = {}
    newRoundMessages = {}
    transactionQueueLimit = 5

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/Transaction", methods=['POST'])
def Transaction():
    jsn = request.get_json()

    proposer = jsn['transaction']['sender']

    #print(type(proposer))

    #print(proposer)

    signature = jsn['signature']


    transactionHash = Serialization.hashObject(jsn['transaction'])
    pubKey = keySerialization.deserializePublicKey(proposer)


    try:
        Signing.verifyingTheSignature(pubKey, signature,transactionHash)
    except:
        return json.dumps({"response": "KeyError"})

    if transactionHash in MessageQueues.transactionQueue:
        return json.dumps({"response": "Transaction Already Queued"})

    MessageQueues.transactionQueue[transactionHash] = jsn['transaction']

    PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "Transaction")

    PBFTNode.node.ProposerId = PBFTNode.node.calculateProposerId()

    print({"ProposerId":PBFTNode.node.ProposerId})

    if len(MessageQueues.transactionQueue) > MessageQueues.transactionQueueLimit and PBFTNode.node.ProposerId == PBFTNode.node.id:
        print("about to propose a block!")
        currentBlock = createBlock()
        BlockVerification.VerifyBlock(currentBlock)
        print(PBFTNode.node.broadcastBlockToPeers(currentBlock))

    return json.dumps({"status":"ok"})


@app.route("/ProposeBlock", methods=['POST'])
def NewBlock():
    jsn = request.get_json()

    blockjsn = jsn['blockData']

    proposer = jsn['sender']

    signature = jsn['signature']

    recievedHash = jsn['blockHash']

    jsnString = json.dumps(blockjsn, indent=4, sort_keys=True)

    if recievedHash in MessageQueues.PendingBlockDict:
        return json.dumps({"response": "Block Already Proposed"})

    try:
        Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
    except:
        return json.dumps({"response": "KeyError"})

    

    block = Block.deserializeJSON(jsnString)
    hash = block.getHash()
    if recievedHash == hash and BlockVerification.VerifyBlock(block):

        PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "ProposeBlock")

        MessageQueues.PendingBlockDict[hash] = block

        PBFTNode.node.broadcastVerificationVotesToPeers(recievedHash)

        return json.dumps({"response": "ok"})

    return json.dumps({"response": "hash/validation error"})
        

    



@app.route("/VerificationVote", methods=['POST'])
def VerificationVote():
    
    jsn = request.get_json()

    proposer = jsn['sender']

    signature = jsn['signature']

    recievedHash = jsn['blockHash']

    if recievedHash in MessageQueues.PendingBlockDict:
        if recievedHash in MessageQueues.validationVotes:
            if proposer in MessageQueues.PendingBlockDict[recievedHash]:
                return json.dumps({"response": "Vote Already Counted"})

        try:
            Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
        except:
            return json.dumps({"response": "KeyError"})

        if not(recievedHash in MessageQueues.validationVotes):
            MessageQueues.validationVotes[recievedHash] = []

        MessageQueues.validationVotes[recievedHash].append(proposer)

        PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "VerificationVote")

        faults = len(PBFTNode.node.peers) - len(MessageQueues.validationVotes[recievedHash])

        if len(MessageQueues.validationVotes[recievedHash]) >= 2*faults + 1:
            PBFTNode.node.broadcastCommitVotesToPeers(recievedHash)

            return jsonify({"response": "Broadcasted Commit"})
        
        return jsonify({"response": "Recieved verification but didnt hit threshold"})

    return json.dumps({"response": "voting on a non-existent block"})





@app.route("/CommitVote", methods=['POST'])
def CommitVote():
    jsn = request.get_json()

    proposer = jsn['sender']

    signature = jsn['signature']

    recievedHash = jsn['blockHash']

    if recievedHash in MessageQueues.PendingBlockDict:
        if recievedHash in MessageQueues.commitMessages:
            if proposer in MessageQueues.PendingBlockDict[recievedHash]:
                return json.dumps({"response": "Vote Already Counted"})

        try:
            Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
        except:
            return json.dumps({"response": "KeyError"})

        if not(recievedHash in MessageQueues.commitMessages):
            MessageQueues.commitMessages[recievedHash] = []

        MessageQueues.commitMessages[recievedHash].append(proposer)

        PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "CommitVote")

        faults = len(PBFTNode.node.peers) - len(MessageQueues.commitMessages[recievedHash])

        if len(MessageQueues.commitMessages[recievedHash]) >= 2*faults + 1:

            PBFTNode.node.blockChain.add_block(MessageQueues.PendingBlockDict[recievedHash])

            print(len(PBFTNode.node.blockChain.chain))

            PBFTNode.node.broadcastNewRoundVotesToPeers(recievedHash)

            return jsonify({"response": "Broadcasted New Round and Added block to chain"})
        
        return jsonify({"response": "Recieved commit but didnt hit threshold"})

    return json.dumps({"response": "voting on a non-existent block"})

  



@app.route("/NewRound", methods=['POST'])
def NewRound():
    jsn = request.get_json()

    proposer = jsn['sender']

    signature = jsn['signature']

    recievedHash = jsn['blockHash']

    if recievedHash in MessageQueues.PendingBlockDict:
        if recievedHash in MessageQueues.newRoundMessages:
            if proposer in MessageQueues.PendingBlockDict[recievedHash]:
                return json.dumps({"response": "Vote Already Counted"})


        try:
            Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
        except:
            return json.dumps({"response": "KeyError"})

        if not(recievedHash in MessageQueues.newRoundMessages):
            MessageQueues.newRoundMessages[recievedHash] = []

        MessageQueues.newRoundMessages[recievedHash].append(proposer)

        PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "NewRound")

        faults = len(PBFTNode.node.peers) - len(MessageQueues.newRoundMessages[recievedHash])

        if len(MessageQueues.newRoundMessages[recievedHash]) >= 2*faults + 1:
            del MessageQueues.PendingBlockDict[recievedHash]
            del MessageQueues.validationVotes[recievedHash]
            del MessageQueues.commitMessages[recievedHash]
            del MessageQueues.newRoundMessages[recievedHash]
            MessageQueues.transactionQueue = {}

            print(MessageQueues.PendingBlockDict)
            print(MessageQueues.validationVotes)
            print(MessageQueues.commitMessages)
            print(MessageQueues.newRoundMessages)

            return jsonify({"response": "Cleared Queues"})
        
        return jsonify({"response": "Recieved new round but didnt hit threshold to clear"})

    return jsonify({"response": "voting on a non-existent block"})



@app.route("/CheckBlockChain")
def CheckBlockChain():
    return "<p>Hello, World!</p>"



@app.route("/GetAllGroups", methods=['POST'])
def GetAllGroups():
    jsn = request.get_json()
    publicKey = jsn["PublicKey"]

    print(publicKey)

    return jsonify({"responsedddd": "okddd"})
