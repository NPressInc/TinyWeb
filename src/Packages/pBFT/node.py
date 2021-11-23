
import time
import brotli
import asyncio
from cryptography.hazmat.backends.interfaces import PBKDF2HMACBackend
import requests

import random

from Packages.Serialization.Serialization import Serialization
from Packages.Serialization.keySerialization import keySerialization
from Packages.structures.BlockChain.Parsers.BlockchainParser import BlockchainParser
from ..structures.BlockChain.BlockChain import BlockChain
from ..structures.BlockChain.Block import Block
from ..Verification.BlockVerification import BlockVerification
from ..FileIO.readLoadBlockChain import BlockChainReadWrite
from ..Client.TinyWebClient import TinyWebClient
from ..Verification.Signing import Signing


import sys
nodeId = 0
if len(sys.argv) > 2:
    nodeId = int(sys.argv[2])




class PBFTNode:
    node = None
    @staticmethod
    def runNode():
        blockChain = BlockChainReadWrite.readBlockChainFromFile(nodeId)

        if blockChain == None:
            blockChain = PBFTNode.configureBlockChainForFirstUse()

        counter = 1

        print({"last Block Index": blockChain.last_block().index})

        print({"nodeId": nodeId})

        node = PBFTNode(nodeId, blockChain)

        PBFTNode.node = node

        print({"in Node top, public Key": keySerialization.serializePublicKey(PBFTNode.node.publicKey)})


        #BlockChainReadWrite.saveBlockChainToFile(node.blockChain)


        newPeerList = BlockchainParser.getMostRecentPeerList(node.blockChain)
                #print({"new Peer List, nodee":newPeerList})
        if newPeerList != None:
            newPeers = []
            for peer in newPeerList:
                if not(peer in node.peers):
                    newPeers.append(peer)
            print("Loaded peers from blockchain")
            if len(newPeers) != 0:  
                node.peers = node.peers + newPeers # adds new peers list to node.peers


        blockChainLength =  PBFTNode.node.blockChain.length

        blockChainHasProgressed = True


        while counter < 1000:
            
            #print({"check Length": blockChainLength })
            #print({"actualLength": PBFTNode.node.blockChain.length })
            #print({"blockChainHasProgressed": blockChainHasProgressed})

            blockChainHasProgressed = PBFTNode.node.blockChain.length != blockChainLength

            if counter % 15 == 0:
                
                print({"blockChainHasProgressed": blockChainHasProgressed})
                newPeerList = BlockchainParser.getMostRecentPeerList(node.blockChain)
                print({"new Peer List, nodee":newPeerList})
                if newPeerList != None:
                    newPeers = []
                    for peer in newPeerList:
                        if not(peer in node.peers):
                            newPeers.append(peer)

                    if len(newPeers) != 0:  
                        node.peers = node.peers + newPeers # adds new peers list to node.peers
                        for peer in newPeers:
                            node.broadcastBlockChainToNewNode(peer)
                    else:
                        print("peers havent Changed")
                elif len(node.peers) == 0:
                    print("Creating Block For Self")
                    node.SendBlockCreationSignalForSingularNode()

                print({"peers": PBFTNode.node.peers})
                print({"proposerId": PBFTNode.node.calculateProposerId()})
                if not blockChainHasProgressed:
                    blockChainLength = PBFTNode.node.blockChain.length
                    if PBFTNode.node.calculateProposerId() == PBFTNode.node.id:
                        print("Node script Proposing Block Because of lack of traffic")
                        currentBlock = PBFTNode.node.createBlock("http://127.0.0.1:" + str(5000 + nodeId) + "/")

                        BlockVerification.VerifyBlock(currentBlock)

                        blockHash = currentBlock.getHash()

                        if currentBlock.previous_hash != PBFTNode.node.blockChain.last_block().getHash():
                                raise Exception({"in Transaction, sync error detected":"Chains Out of sync while proposing block"})

                        #print({"Proposed Block previous hash":currentBlock.previous_hash})

                        #print({"Proposed Block blockchais Hashes":PBFTNode.node.blockChain.getListOfBlockHashes()})

                        PBFTNode.node.broadcastBlockToPeers(currentBlock, blockHash)
                    

            if counter % 30 == 0:
                blockChainLength = PBFTNode.node.blockChain.length
                if (not blockChainHasProgressed) and len(PBFTNode.node.peers) != 0:
                    PBFTNode.node.resyncWithLongestBlockChain()



            if counter % 100 == 0:
                if len(PBFTNode.node.peers) != 0:
                    random.shuffle(PBFTNode.node.peers)
                    print({"shuffled Peers": PBFTNode.node.peers})
                print("Saving Blockchain every 100 seconds")
                BlockChainReadWrite.saveBlockChainToFile(node.blockChain, PBFTNode.node.id)

            time.sleep(1)
            counter += 1
            
            #print({"in Node, blockchain state":PBFTNode.node.blockChain.getListOfBlockHashes()})

            

           

    def __init__(self, id, blockChain):
        self.__privateKey = None
        self.publicKey = None

        self.id = id  # id represents the order in which nodes act as the proposer

        self.peers = []

        self.ProposerId = 0

        self.blockChain = blockChain

        self.phase = 0

        self.initializeKeys()

    def initializeKeys(self):
        client = None
        try:
            privateKey = Signing.PrivateKeyMethods.loadPrivateKeyNode(self.id)
            self.publicKey=Signing.PrivateKeyMethods.generatePublicKeyFromPrivate(privateKey)
            print("Loaded Client: " + self.id)
        except:
            self.__privateKey = Signing.PrivateKeyMethods.generatePrivateKey()
            self.publicKey = Signing.PrivateKeyMethods.generatePublicKeyFromPrivate(self.__privateKey)
            Signing.PrivateKeyMethods.savePrivateKeyNode(self.__privateKey, self.id)
            print("Created New Node: " + str(self.id))

        return client


    def getLastBlockHashFromPeers(self):
        import requests
        hashes = {}
        for peer in self.peers:
            url = peer + "BlockChainLastHash"
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                data = Serialization.deserializeObjFromJsonR(r.text)
                lastBlockHash = data['lastHash']

                if not(lastBlockHash in hashes):
                    hashes[lastBlockHash] = 1
                else:
                    hashes[lastBlockHash] += 1
        max = -1
        maxHash = ""

        for key in hashes:
            if hashes[key] > max:
                max = hashes[key]
                maxHash = key

        return maxHash

    def resyncWithLongestBlockChain(self):
        longestChain = 0
        peerWithLongestBlockChain = self.peers[0]
        for peer in self.peers:
            if peer != "http://127.0.0.1:" + str(5000 + nodeId) + "/":
                print("get all the lengths of the blockchains and select the longest one to query")
                peerChainLength = self.getBlockChainLengthOfPeer(peer)
                if  peerChainLength > longestChain:
                    peerWithLongestBlockChain = peer
                    longestChain = peerChainLength
        
        if longestChain > self.blockChain.length:
            self.requestMissingBlocksFromPeer(peerWithLongestBlockChain)

    def getPendingTransactions(self, peer):
        url = peer + "GetPendingTransactions"
        
        r = requests.get(url)

        if r.status_code == requests.codes.ok:

            data = Serialization.deserializeObjFromJsonR(r.text)

            transactions = data["pendingTransactions"]

            return transactions
        return {}
            


    def getBlockChainLengthOfPeer(self, peer):

        try:
            url = peer + "GetBlockChainLength"
        
            r = requests.get(url)

            if r.status_code == requests.codes.ok:

                data = Serialization.deserializeObjFromJsonR(r.text)

                length = data["chainLength"]

                return length
            return 0

        except:
            return 0
        



    def createBlock(self, TransactionSource):
        transactions = []

        transactionDict = PBFTNode.node.getPendingTransactions(TransactionSource)

        for key in transactionDict:
            transactions.append(transactionDict[key])

        newIndex = self.blockChain.length
        timestamp = time.time()

        previousHash = self.blockChain.last_block().getHash()
        proposerId = self.id
        newIndex = self.blockChain.length
        block = Block(newIndex, transactions, timestamp,
                    previousHash, proposerId)
        return block


    def requestMissingBlocksFromPeer(self, peer):
        import requests
        
        print("Missing Blocks Detected, requesting blocks from peers")
        url = peer + "MissingBlockRequeset"
        lastHash = self.blockChain.last_block().getHash()
        signature = Signing.normalSigning(self.__privateKey, lastHash)
        data = {
            "lastHash": lastHash,
            "sender": keySerialization.serializePublicKey(self.publicKey),
            "signature": signature
        }
        data = Serialization.serializeObjToJson(data)
        headers = {'Content-type': 'application/json',
                'Accept': 'text/plain'}
        
        r = requests.post(url, data= data, headers=headers)

        if r.status_code == requests.codes.ok:

            data = Serialization.deserializeObjFromJsonR(r.text)

            missingBlocks = data['response']['missingBlocks']

            print({"# of missing Blocks Found":len(missingBlocks)})

            if len(missingBlocks) > 0:
                for i in range(len(missingBlocks)-1, -1, -1):
                    if BlockVerification.VerifyBlock(missingBlocks[i]) == True:
                        PBFTNode.node.blockChain.add_block( Block.deserializeJSON(missingBlocks[i]))
                    else: 
                        raise Exception("Resync of blockchain failed becuase of invalid block")

            print({"missingBlockResp":data})
        else:
            return None
                

                
        

    
    def SendBlockCreationSignalForSingularNode(self):
        import requests
        try:
            url = "http://127.0.0.1:" + str(5000 + nodeId) + "/AddNewBlockForSingularNode"
            salt = "The Packers Rule"
            signature = Signing.normalSigning(self.__privateKey, salt)
            data = {
                "salt": salt,
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            
            r = requests.post(url, data= data, headers=headers)
            if r.status_code == requests.codes.ok:

                data = Serialization.deserializeObjFromJsonR(r.text)

                return data
            else:
                return None
        except:
            print("Node not found: self")

                
        #print("Done Broadcasting new block")
        
    def reBroadcastMessage(self, data, route):
        from threading import Thread
        #print("rebroadcasting Message " + route)
        if route == "Transaction":
            for peer in self.peers:
                self.reBroadcastSingleMessage(peer,data, route)
        #else:
            #print("Rebroadcasting Disabled")
        #print("Done ReBroadcasting " + route)

    def reBroadcastSingleMessage(self, peer,data, route):
        from threading import Thread
        from requests import post
        import json
        try:
            url = peer + route
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            r = requests.post(url, data= data, headers=headers)
            if r.status_code == requests.codes.ok:

                data = Serialization.deserializeObjFromJsonR(r.text)

                #print({"Re Broadcast " + route:data})
            else:
                return None


            #Thread(target=post, args=(url,), kwargs={"json": json.loads(data)}).start()
        except:
            print("line 213: Node not found at: " + peer)


    def broadcastBlockToPeers(self, block, blockHash):
        
        for peer in self.peers:
            self.broadcastBlockToSinglePeer(peer, block, blockHash)
                
        #print("Done Broadcasting new block")

    def broadcastBlockToSinglePeer(self, peer, block, blockHash):
        try:
            #print("Broadcasting New Block to: " + peer)
            url = peer + "ProposeBlock"
            blockString = block.serializeJSON()
            signature = Signing.normalSigning(self.__privateKey, blockHash)
            data = {
                "blockData":blockString,
                "blockHash": blockHash,
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            
            r = requests.post(url, data= data, headers=headers)
            if r.status_code == requests.codes.ok:

                data = Serialization.deserializeObjFromJsonR(r.text)

                print({"Broadcast Single Block":data})
            else:
                return None
        except:
            print("line 248: Node not found at: " + peer)


    def broadcastBlockChainToNewNode(self, peer):
        import requests
        import hashlib
        try:
            url = peer + "SendNewBlockChain"
            blockChainString = self.blockChain.serializeJSON()
            hash = hashlib.sha256(blockChainString.encode()).hexdigest()
            signature = Signing.normalSigning(self.__privateKey, hash)
            data = {
                "blockChain":blockChainString,
                "blockChainHash": hash,
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            
            r = requests.post(url, data= data, headers=headers)
            if r.status_code == requests.codes.ok:

                data = Serialization.deserializeObjFromJsonR(r.text)
                

                #print({"Broadcast Blockchain to new node":data})
            else:
                return None
        except:
            print("line 279: Node not found at: " + peer)
                
        #print("Done Broadcasting new blockchain")

    def broadcastVerificationVotesToPeers(self, blockHash, blockString):
        for peer in self.peers:
            self.broadcastVerificationVoteToSinglePeer(peer, blockHash, blockString)
            

    def broadcastVerificationVoteToSinglePeer(self, peer,blockHash, blockString):
        try:
            #print("Broadcasting Verification Vote to: " + peer)
            url = peer + "VerificationVote"
            signature = Signing.normalSigning(self.__privateKey, blockHash)
            data = {
                "blockData":blockString,
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature,
                "blockHash": blockHash
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            r = requests.post(url, data=data, headers=headers)
            if r.status_code == requests.codes.ok:

                data = Serialization.deserializeObjFromJsonR(r.text)
                print({"Verifiaction vote resp":data})
        except:
            print("line 307: Node not found at: " + peer)
        
    def broadcastCommitVotesToPeers(self, blockHash, blockString):
        import requests
        for peer in self.peers:
            self.broadcastCommitVoteToSinglePeer(peer, blockHash, blockString)
            
    def broadcastCommitVoteToSinglePeer(self, peer,blockHash, blockString):
        try:
            #print("Broadcasting Commit Vote to: " + peer)
            url = peer + "CommitVote"
            signature = Signing.normalSigning(self.__privateKey, blockHash)
            data = {
                "blockData":blockString,
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature,
                "blockHash": blockHash
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            r = requests.post(url, data=data, headers=headers)
            if r.status_code == requests.codes.ok:

                data = Serialization.deserializeObjFromJsonR(r.text)
                print({"Commit vote resp":data})
        except:
            print("line 333: Node not found at: " + peer)
        
    def broadcastNewRoundVotesToPeers(self, blockHash, blockString):
        import requests
        for peer in self.peers:
            self.broadcastNewRoundVoteToSinglePeer(peer, blockHash, blockString)
            

    def broadcastNewRoundVoteToSinglePeer(self,peer, blockHash, blockString):
        try:
            #print("Broadcasting New Round Vote to: " + peer)
            url = peer + "NewRound"
            signature = Signing.normalSigning(self.__privateKey, blockHash)
            data = {
                "blockData": blockString,
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature,
                "blockHash": blockHash
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            r = requests.post(url, data=data, headers=headers)
            if r.status_code == requests.codes.ok:

                data = Serialization.deserializeObjFromJsonR(r.text)
                print({"New Round vote resp":data})
        except:
            print("line 360: Node not found at: " + peer)
        

    def calculateProposerId(self):
        
        NumberOfPeers = len(self.peers)

        if len(self.peers) < 1 or self.blockChain.chain[-1].proposerId == -1:
            return 0

        index = (self.blockChain.chain[-1].proposerId + 1) % (NumberOfPeers)
        return index

    @staticmethod
    def compressJson(input):
        return brotli.compress(input)

    @staticmethod
    def decompressJson(input):
        return brotli.decompress(input)

    @staticmethod
    def configureBlockChainForFirstUse():

        client1 = TinyWebClient.initializeClient("1")
        client1PublicKeyString = keySerialization.serializePublicKey(client1.publicKey)
        blockChain = BlockChain(creatorPublicKey=client1PublicKeyString)

        return blockChain
