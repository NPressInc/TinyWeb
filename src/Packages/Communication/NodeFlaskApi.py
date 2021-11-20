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
    PendingBlockDict = {}
    CommitedBlockDict = {}
    transactionQueue = {}
    validationVotes = {}
    commitMessages = {}
    newRoundMessages = {}
    transactionQueueLimit = 3
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

    print({"Proposer Id":PBFTNode.node.ProposerId})

    if len(MessageQueues.transactionQueue) > MessageQueues.transactionQueueLimit and PBFTNode.node.ProposerId == PBFTNode.node.id:
        print("about to propose a block!")

        #PBFTNode.node.requestMissingBlocks()

        currentBlock = createBlock()
        BlockVerification.VerifyBlock(currentBlock)

        blockHash = currentBlock.getHash()

        if currentBlock.previous_hash != PBFTNode.node.blockChain.last_block().getHash():
                raise Exception({"in Transaction, sync error detected":"Chains Out of sync while proposing block"})

        #print({"Proposed Block previous hash":currentBlock.previous_hash})

        #print({"Proposed Block blockchais Hashes":PBFTNode.node.blockChain.getListOfBlockHashes()})

        PBFTNode.node.broadcastBlockToPeers(currentBlock, blockHash)

        #PBFTNode.node.broadcastVerificationVotesToPeers(blockHash)

    return json.dumps({"status":"ok"})


@app.route("/ProposeBlock", methods=['POST'])
def NewBlock():
    jsn = request.get_json()

    blockjsn = jsn['blockData']

    proposer = jsn['sender']

    signature = jsn['signature']

    recievedHash = jsn['blockHash']

    blockString = json.dumps(blockjsn, indent=4, sort_keys=True)

    myPublicKey = keySerialization.serializePublicKey(PBFTNode.node.publicKey)
    

    if recievedHash in MessageQueues.PendingBlockDict or recievedHash in MessageQueues.CommitedBlockDict:
        return json.dumps({"response": "Block already Processed"})

    

    try:
        Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
    except:
        return json.dumps({"response": "KeyError"})

    block = Block.deserializeJSON(blockString)
    blockHash = block.getHash()


    if recievedHash == blockHash and BlockVerification.VerifyBlock(block):

        #print("about to send verification")

        #PBFTNode.node.requestMissingBlocks()

        if block.previous_hash != PBFTNode.node.blockChain.last_block().getHash():
                raise Exception({"in commit, sync error detected":"Chains Out of sync while recieving poposed block"})

        MessageQueues.PendingBlockDict[recievedHash]  = block

        PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "ProposeBlock")
        time.sleep(1)

        PBFTNode.node.broadcastVerificationVotesToPeers(recievedHash, blockString)

        return json.dumps({"response": "ok"})

    return json.dumps({"response": "hash/validation error"})
        

    



@app.route("/VerificationVote", methods=['POST'])
def VerificationVote():
    
    jsn = request.get_json()

    proposer = jsn['sender']

    signature = jsn['signature']

    recievedHash = jsn['blockHash']

    blockjsn = jsn['blockData']

    blockString = json.dumps(blockjsn, indent=4, sort_keys=True)

    block = Block.deserializeJSON(blockString)
    blockHash = block.getHash()

    if recievedHash == blockHash:
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
        time.sleep(1)

        reachedThreshold = False

        #if len(PBFTNode.node.peers) == 1 or len(PBFTNode.node.peers) == 1:
            #if recievedHash in MessageQueues.validationVotes and len(MessageQueues.validationVotes[recievedHash]) == len(PBFTNode.node.peers)+1:
                #reachedThreshold = True
        
        #elif len(PBFTNode.node.peers) >= 2:

        minApprovals = int(2 * (len(PBFTNode.node.peers) / 3) + 1)
        print({"min approvals": minApprovals})
        if recievedHash in MessageQueues.validationVotes:
            if len(MessageQueues.validationVotes[recievedHash]) >= minApprovals:
                reachedThreshold = True

        if reachedThreshold:
            #print("about to send commit")
            PBFTNode.node.broadcastCommitVotesToPeers(recievedHash, blockString)

            return jsonify({"response": "Broadcasted Commit"})
        
        return jsonify({"response": "Recieved verification but didnt hit threshold"})

    return json.dumps({"response": "hashes didnt match"})





@app.route("/CommitVote", methods=['POST'])
def CommitVote():
    jsn = request.get_json()

    proposer = jsn['sender']

    signature = jsn['signature']

    recievedHash = jsn['blockHash']


    blockjsn = jsn['blockData']

    blockString = json.dumps(blockjsn, indent=4, sort_keys=True)

    block = Block.deserializeJSON(blockString)
    blockHash = block.getHash()

    if recievedHash == blockHash:
        if recievedHash in MessageQueues.commitMessages:
            if proposer in MessageQueues.commitMessages[recievedHash]:
                return json.dumps({"response": "Vote Already Counted"})

        try:
            Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, recievedHash)
        except:
            return json.dumps({"response": "KeyError"})

        if not(recievedHash in MessageQueues.commitMessages):
            MessageQueues.commitMessages[recievedHash] = []

        #print({"in commitVote, recievedHash": recievedHash})
        MessageQueues.commitMessages[recievedHash].append(proposer)

        #print({"InCommitVote, commitMessages":MessageQueues.commitMessages[recievedHash] })

        PBFTNode.node.reBroadcastMessage(Serialization.serializeObjToJson(jsn), "CommitVote")
        time.sleep(1)

        reachedThreshold = False

        #if len(PBFTNode.node.peers) == 1 or len(PBFTNode.node.peers) == 1:

            #if recievedHash in MessageQueues.commitMessages and len(MessageQueues.commitMessages[recievedHash]) >= len(PBFTNode.node.peers) + 1:
                #reachedThreshold = True
            
        #elif len(PBFTNode.node.peers) >= 2:
        minApprovals = int(2 * (len(PBFTNode.node.peers) / 3) + 1)
        if recievedHash in MessageQueues.commitMessages:
            if len(MessageQueues.commitMessages[recievedHash]) >= minApprovals:
                reachedThreshold = True


        if reachedThreshold:

            print({"Proposed Block":block.getHash()})

            print({"Proposed Block previous hash":block.previous_hash})

            print({"Proposed Block blockchais Hashes":PBFTNode.node.blockChain.getListOfBlockHashes()})

            #print("about to send newRound")

            

            if block.previous_hash != PBFTNode.node.blockChain.last_block().getHash():
                raise Exception({"in commit, sync error detected":"While Committing, chain out of sync"})
                
                PBFTNode.node.requestMissingBlocks()

            if not(blockHash in MessageQueues.CommitedBlockDict):

                block.previous_hash = PBFTNode.node.blockChain.last_block().getHash()

                #PBFTNode.node.requestMissingBlocks()

                PBFTNode.node.blockChain.add_block(block)

                MessageQueues.CommitedBlockDict[blockHash] = blockHash

                print({"Block Committed, BlockChainLength": len(PBFTNode.node.blockChain.chain)})

            PBFTNode.node.broadcastNewRoundVotesToPeers(recievedHash, blockString)

            return jsonify({"response": "Broadcasted New Round and Added block to chain"})
        
        return jsonify({"response": "Recieved commit but didnt hit threshold"})

    return json.dumps({"response": "hashes dont match"})

  



@app.route("/NewRound", methods=['POST'])
def NewRound():
    jsn = request.get_json()

    proposer = jsn['sender']

    signature = jsn['signature']

    recievedHash = jsn['blockHash']

    blockjsn = jsn['blockData']

    blockString = json.dumps(blockjsn, indent=4, sort_keys=True)

    block = Block.deserializeJSON(blockString)
    blockHash = block.getHash()

    if recievedHash == blockHash:
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
        time.sleep(1)

        reachedThreshold = False        

        #if len(PBFTNode.node.peers) == 1 or len(PBFTNode.node.peers) == 1:
            #if recievedHash in MessageQueues.newRoundMessages:
                #if len(MessageQueues.newRoundMessages[recievedHash]) == len(PBFTNode.node.peers) + 1:
                    #reachedThreshold = True
            
        #elif len(PBFTNode.node.peers) >= 2:
        minApprovals = int(2 * (len(PBFTNode.node.peers) / 3) + 1)
        if recievedHash in MessageQueues.newRoundMessages:
            if len(MessageQueues.newRoundMessages[recievedHash]) >= minApprovals:
                reachedThreshold = True

        if reachedThreshold:
            if block.previous_hash == PBFTNode.node.blockChain.chain[-1].getHash():

                print("----------------------- \nNode was not needed in voting, catching up to make sure that it stays in the loop \n -----------------------")

                print({"Proposed Block":block.getHash()})

                print({"Proposed Block previous hash":block.previous_hash})

                print({"Proposed Block blockchais Hashes":PBFTNode.node.blockChain.getListOfBlockHashes()})

                PBFTNode.node.blockChain.add_block(block)

                MessageQueues.CommitedBlockDict[blockHash] = blockHash

                print({"Block Committed, BlockChainLength": len(PBFTNode.node.blockChain.chain)})


            print("Clearing House")
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

    print({"Missing Block Requets: last Hash": lastHash})

    missingBlocks = []

    missingHashes = []

    try:
        Signing.verifyingTheSignature(keySerialization.deserializePublicKey(proposer), signature, lastHash)
    except:
        return json.dumps({"response": "KeyError"})

    for i in range(len(PBFTNode.node.blockChain.chain)-1 ,-1,-1):
        
        currentHash = PBFTNode.node.blockChain.chain[i].getHash()
        print({"Missing Block Request current Hash Scanned":currentHash})
        if currentHash != lastHash:
            missingBlocks.append(PBFTNode.node.blockChain.chain[i].serializeJSON())
            missingHashes.append(PBFTNode.node.blockChain.chain[i].getHash())
        elif currentHash == lastHash:
            return json.dumps({"response":{"missingBlocks":missingBlocks}})

    print({"Proposed Block blockchais Hashes":PBFTNode.node.blockChain.getListOfBlockHashes()})

    print({"Missing Block Hashes":missingHashes})

    if len(missingHashes) != 0:
        raise Exception("Blockchains shared no hashes, completely out of sync")

    return json.dumps({"response":{"missingBlocks":[]}})


@app.route("/SendNewBlockChain", methods=['POST'])
def SendNewBlockChain():

    jsn = request.get_json()

    proposer = jsn['sender']

    signature = jsn['signature']

    #print({"remoteIP": request.remote_addr})

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
