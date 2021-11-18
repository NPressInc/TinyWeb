from time import perf_counter
from flask import Flask, request, jsonify
from os import path

from Packages.Serialization.keySerialization import keySerialization


from ..Serialization.Serialization import Serialization

from ..structures.BlockChain.Block import Block

from ..structures.BlockChain.BlockChain import BlockChain

from ..pBFT.node import PBFTNode

from ..Verification.Signing import Signing

from ..Verification.BlockVerification import BlockVerification

import json

import time

import asyncio

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
    PendingBlockVerificationRecord = {}
    transactionQueue = {}
    PendingBlockDict = {}
    validationVotes = {}
    commitMessages = {}
    newRoundMessages = {}
    transactionQueueLimit = 2
    blockChainParent = ""
    

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

    if transactionHash in MessageQueues.transactionQueue:
        return json.dumps({"response": "Transaction Already Queued"})

    try:
        Signing.verifyingTheSignature(pubKey, signature,transactionHash)
    except:
        return json.dumps({"response": "KeyError"})

    MessageQueues.transactionQueue[transactionHash] = jsn['transaction']

    PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "Transaction")

    time.sleep(1)

    PBFTNode.node.ProposerId = PBFTNode.node.calculateProposerId()

    print({"ProposerId":PBFTNode.node.ProposerId})

    if len(MessageQueues.transactionQueue) > MessageQueues.transactionQueueLimit and PBFTNode.node.ProposerId == PBFTNode.node.id:
        print("about to propose a block!")

        PBFTNode.node.requestMissingBlocks()

        currentBlock = createBlock()
        BlockVerification.VerifyBlock(currentBlock)

        blockHash = currentBlock.getHash()
        

        MessageQueues.PendingBlockDict[blockHash] = currentBlock

        print({"Proposed Block previous hash":currentBlock.previous_hash})

        print({"Proposed Block blockchais Hashes":PBFTNode.node.blockChain.getListOfBlockHashes()})

        PBFTNode.node.broadcastBlockToPeers(currentBlock)

        PBFTNode.node.broadcastVerificationVotesToPeers(blockHash)

    return json.dumps({"status":"ok"})


@app.route("/ProposeBlock", methods=['POST'])
def NewBlock():
    jsn = request.get_json()

    blockjsn = jsn['blockData']

    proposer = jsn['sender']

    signature = jsn['signature']

    recievedHash = jsn['blockHash']

    jsnString = json.dumps(blockjsn, indent=4, sort_keys=True)

    myPublicKey = keySerialization.serializePublicKey(PBFTNode.node.publicKey)
    

    if recievedHash in MessageQueues.PendingBlockDict:
        return json.dumps({"response": "Block Verified by Node"})

    try:
        Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
    except:
        return json.dumps({"response": "KeyError"})

    

    block = Block.deserializeJSON(jsnString)
    hash = block.getHash()

    

    lastHash = PBFTNode.node.blockChain.last_block().getHash()

    if block.previous_hash != lastHash:
        PBFTNode.node.requestMissingBlocks()

    if recievedHash == hash and BlockVerification.VerifyBlock(block):

        print("about to send verification")

        MessageQueues.PendingBlockVerificationRecord[proposer] = recievedHash

        MessageQueues.PendingBlockDict[hash] = block

        PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "ProposeBlock")
        time.sleep(1)

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
            if proposer in MessageQueues.validationVotes[recievedHash]:
                return json.dumps({"response": "Vote Already Counted"})

        try:
            Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
        except:
            return json.dumps({"response": "KeyError"})

        if not(recievedHash in MessageQueues.validationVotes):
            MessageQueues.validationVotes[recievedHash] = []

        MessageQueues.validationVotes[recievedHash].append(proposer)

        PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "VerificationVote")

        reachedThreshold = False

        if len(PBFTNode.node.peers) == 1 or len(PBFTNode.node.peers) == 2:
            print({"Validation Votes: ": MessageQueues.validationVotes[recievedHash]})
            if len(MessageQueues.validationVotes[recievedHash]) == len(PBFTNode.node.peers)+1:
                reachedThreshold = True
            
        elif len(PBFTNode.node.peers) > 2:
            minApprovals = int(2 * (len(PBFTNode.node.peers) / 3) + 1)
            if minApprovals >= len(MessageQueues.validationVotes[recievedHash]):
                reachedThreshold = True

        if reachedThreshold:
            print("about to send commit")
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
            if proposer in MessageQueues.commitMessages[recievedHash]:
                return json.dumps({"response": "Vote Already Counted"})

        try:
            Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
        except:
            return json.dumps({"response": "KeyError"})

        if not(recievedHash in MessageQueues.commitMessages):
            MessageQueues.commitMessages[recievedHash] = []

        print({"in commitVote, recievedHash": recievedHash})
        MessageQueues.commitMessages[recievedHash].append(proposer)

        print({"InCommitVote, commitMessages":MessageQueues.commitMessages[recievedHash] })

        PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "CommitVote")

        reachedThreshold = False

        if len(PBFTNode.node.peers) == 1 or len(PBFTNode.node.peers) == 2:

            if len(MessageQueues.commitMessages[recievedHash]) >= len(PBFTNode.node.peers) + 1:
                reachedThreshold = True
            
        elif len(PBFTNode.node.peers) > 2:
            minApprovals = int(2 * (len(PBFTNode.node.peers) / 3) + 1)
            if minApprovals >= len(MessageQueues.commitMessages[recievedHash]):
                reachedThreshold = True


        if reachedThreshold:

            print({"Proposed Block":MessageQueues.PendingBlockDict[recievedHash].getHash()})

            print({"Proposed Block previous hash":MessageQueues.PendingBlockDict[recievedHash].previous_hash})

            print({"Proposed Block blockchais Hashes":PBFTNode.node.blockChain.getListOfBlockHashes()})

            print("about to send newRound")

            PBFTNode.node.blockChain.add_block(MessageQueues.PendingBlockDict[recievedHash])

            print({"BlockChainLength": len(PBFTNode.node.blockChain.chain)})

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
            if proposer in MessageQueues.newRoundMessages[recievedHash]:
                return json.dumps({"response": "Vote Already Counted"})


        try:
            Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
        except:
            return json.dumps({"response": "KeyError"})

        if not(recievedHash in MessageQueues.newRoundMessages):
            MessageQueues.newRoundMessages[recievedHash] = []

        MessageQueues.newRoundMessages[recievedHash].append(proposer)

        PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "NewRound")

        reachedThreshold = False        

        if len(PBFTNode.node.peers) == 1 or len(PBFTNode.node.peers) == 2:

            if len(MessageQueues.newRoundMessages[recievedHash]) == len(PBFTNode.node.peers) + 1:
                reachedThreshold = True
            
        elif len(PBFTNode.node.peers) > 2:
            minApprovals = int(2 * (len(PBFTNode.node.peers) / 3) + 1)
            if minApprovals >= len(MessageQueues.newRoundMessages[recievedHash]):
                reachedThreshold = True

        if reachedThreshold:
            print("Clearing House")
            if recievedHash in MessageQueues.PendingBlockDict:
                del MessageQueues.PendingBlockDict[recievedHash]
            if recievedHash in MessageQueues.validationVotes:
                del MessageQueues.validationVotes[recievedHash]
            if recievedHash in MessageQueues.commitMessages:
                del MessageQueues.commitMessages[recievedHash]
            if recievedHash in MessageQueues.newRoundMessages:
                del MessageQueues.newRoundMessages[recievedHash]
            MessageQueues.transactionQueue = {}

            return jsonify({"response": "Cleared Queues"})
        
        return jsonify({"response": "Recieved new round but didnt hit threshold to clear"})

    return jsonify({"response": "voting on a non-existent block"})


"""
    {
                    "lastHash": lastHash,
                    "sender": keySerialization.serializePublicKey(self.publicKey),
                    "signature": signature
                }
    """


@app.route("/MissingBlockRequeset", methods=['POST'])
def MissingBlockRequeset():

    jsn = request.get_json()

    proposer = jsn['sender']

    signature = jsn['signature']

    lastHash = jsn['lastHash']

    missingBlocks = []

    try:
        Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, lastHash)
    except:
        return json.dumps({"response": "KeyError"})

    for i in range(-1, len(PBFTNode.node.blockChain.chain)-1 ,-1):
        currentHash = PBFTNode.node.blockChain.chain[i].getHash()
        if currentHash != lastHash:
            missingBlocks.append(PBFTNode.node.blockChain.chain[i])

    return json.dumps({"response":{"missingBlocks":missingBlocks}})


@app.route("/SendNewBlockChain", methods=['POST'])
def SendNewBlockChain():

    jsn = request.get_json()

    proposer = jsn['sender']

    signature = jsn['signature']

    print({"remoteIP": request.remote_addr})

    if request.remote_addr in PBFTNode.node.peers:
        return json.dumps({"response":"already synced BLKCHN with node"})
    

    MessageQueues.blockChainParent = proposer

    recievedHash = jsn['blockChainHash']

    blockchainString = jsn['blockChain']

    if keySerialization.serializePublicKey(PBFTNode.node.publicKey) == proposer:
        return json.dumps({"response": "Will "})

    try:
        Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
    except:
        return json.dumps({"response": "KeyError"})

    PBFTNode.node.blockChain = BlockChain.deserializeJSON(blockchainString)

    return json.dumps({"response":"thankyoufor the blockchain"})


@app.route("/AddNewBlockForSingularNode", methods=['POST'])
def AddNewBlockForSingularNode():
    jsn = request.get_json()

    proposer = jsn['sender']

    signature = jsn['signature']

    data = jsn["salt"]

    

    try:
        Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, data)
    except:
        return json.dumps({"response": "KeyError"})

    block = createBlock()

    PBFTNode.node.blockChain.add_block(block)

    MessageQueues.transactionQueue = {}

    print({"BlockChainLength": len(PBFTNode.node.blockChain.chain)})

    print({"transactionLength For Latest block": len(PBFTNode.node.blockChain.chain[-1].transactions)})

    return jsonify({"response": "Added block to chain"})



@app.route("/GetAllGroups", methods=['POST'])
def GetAllGroups():
    jsn = request.get_json()
    publicKey = jsn["PublicKey"]


    return jsonify({"responsedddd": "okddd"})
