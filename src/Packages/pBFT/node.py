
import time
import brotli

from Packages.Serialization.Serialization import Serialization
from Packages.Serialization.keySerialization import keySerialization
from Packages.structures.BlockChain.Parsers.BlockchainParser import BlockchainParser
from ..structures.BlockChain.BlockChain import BlockChain
from ..structures.BlockChain.Block import Block
from ..Verification.BlockVerification import BlockVerification
from ..Communication.NodeFlaskApi import MessageQueues
from ..FileIO.readLoadBlockChain import BlockChainReadWrite
from ..Client.TinyWebClient import TinyWebClient


import sys
nodeId = 0
if len(sys.argv) > 2:
    nodeId = int(sys.argv[2])



class PBFTNode:
    node = None
    @staticmethod
    def runNode():
        blockChain = BlockChainReadWrite.readBlockChainFromFile()

        if blockChain == None:
            blockChain = PBFTNode.configureBlockChainForFirstUse()

        print(blockChain.serializeJSON())

        counter = 0

        print(blockChain.last_block().index)

        node = PBFTNode(nodeId, blockChain)

        PBFTNode.node = node


        BlockChainReadWrite.saveBlockChainToFile(node.blockChain)

        node.peers.append("http://127.0.0.1:"+ str(5000 + nodeId) +"/")

        newPeerList = BlockchainParser.getMostRecentPeerList(node.blockChain)
        if newPeerList != None:
            node.peers = newPeerList


        while counter < 1000:

            currentBlock = None

            if counter % 10 == 0:
                BlockChainReadWrite.saveBlockChainToFile(node.blockChain)
                newPeerList = BlockchainParser.getMostRecentPeerList(node.blockChain)
                if newPeerList != None:
                    node.peers = newPeerList

            time.sleep(5)
            counter += 1
            node.ProposerId = node.calculateProposerId()
            if node.ProposerId == node.id:
                currentBlock = node.createBlock()
                node.verifyBlock(currentBlock)
                node.broadcastBlockToPeers(currentBlock)
                

            else:
                while MessageQueues.PendingBlock == None:
                    time.sleep(1)
                    print("Waiting for block to be proposed")
                MessageQueues.PendingBlock = currentBlock
            
            MessageQueues.PendingBlock = None


            #Validating the proposed block, wether it was the block that we proposed or someone else
            
            ValidateVote = False

            if node.verifyBlock(currentBlock) == True:
                ValidateVote = True

            node.broadcastVerificationVotesToPeers(ValidateVote)


            #Wait for the rest of the validation votes

            while len(MessageQueues.validationVotes) < len(node.peers) - 1:
                time.sleep(1)

            #Count the validation votes from other nodes and myself
            
            votesFor = 0
            for i in range(len(MessageQueues.validationVotes)):
                if MessageQueues.validationVotes[i] == True:
                    votesFor += 1

            faults = len(node.peers)-votesFor

            print({"falts": faults})


            MessageQueues.validationVotes = []

            #Make sure that the number of validation votes is above the threshold and vote accordingly

            commitVote = False

            if votesFor >= 3*faults + 1:
                commitVote = True
            
            node.broadcastCommitVotesToPeers(commitVote)


            #Wait for the commit votes to come in

            while len(MessageQueues.commitMessages) < len(node.peers) - 1:
                time.sleep(1)

            
            commitBlock = False


            #Make sure that the number of commit votes is above the threshold and vote accordingly


            commitMessages = 0
            for i in range(len(MessageQueues.commitMessages)):
                if MessageQueues.commitMessages[i] == True:
                    commitMessages += 1

            faults = len(node.peers)-commitMessages

            if commitMessages >= 3*faults + 1:
                commitBlock = True


            #if the commit votes are above the threshold, then commit the block


            if commitBlock == True:
                node.blockChain.add_block(currentBlock)
                print("Added new block, to chain with hash" + node.blockChain.last_block().getHash())
            else:
                print("Block Didnt pass")



            

        #print("Pre Save")
        # print(blockChain.serializeJSON())

        #BlockChainReadWrite.saveBlockChainToFile(node.blockChain)
        

        time.sleep(2)

        #print("POST Read")
        #blockChainRecovered = BlockChainReadWrite.readBlockChainFromFile()

    def __init__(self, id, blockChain):
        self.__privateKkey = None
        self.publicKey = None

        self.id = id  # id represents the order in which nodes act as the proposer

        self.peers = []

        self.ProposerId = 0

        self.blockChain = blockChain

        self.phase = 0
        


    def createBlock(self):
        transactions = MessageQueues.transactionQueue
        # print(transactions)
        MessageQueues.transactionQueue = []
        newIndex = self.blockChain.length
        timestamp = time.time()
        # print(timestamp)
        previousHash = self.blockChain.last_block().getHash()
        proposerId = self.id
        newIndex = self.blockChain.length
        block = Block(newIndex, transactions, timestamp,
                      previousHash, proposerId)
        
        
        return block

    @staticmethod
    def verifyBlock(block):

        #print("include functionality for sending rejection messages to originators of faulty messages. Do this on a seperate thread.")
       #print("TBI")
        return True

    def broadcastBlockToPeers(self, block):
        import requests
        for peer in self.peers:
            try:
                url = peer + "ProposeBlock"
                data = block.serializeJSON()
                headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
                r = requests.post(url, data=data, headers=headers)
                print(r.status_code)
            except:
                print("Node not found at: " + peer)
                
        print("Done Broadcasting new block")


    def broadcastVerificationVotesToPeers(self, vote):
        import requests
        for peer in self.peers:
            try:
                url = peer + "VerificationVote"
                data = {"vote": vote}
                data = Serialization.serializeObjToJson(data)
                headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
                r = requests.post(url, data=data, headers=headers)
                print(r.status_code)
            except:
                print("Node not found at: " + peer)

    def broadcastCommitVotesToPeers(self, vote):
        import requests
        for peer in self.peers:
            try:
                url = peer + "CommitVote"
                data = {"vote": vote}
                data = Serialization.serializeObjToJson(data)
                headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
                r = requests.post(url, data=data, headers=headers)
                print(r.status_code)
            except:
                print("Node not found at: " + peer)

    def calculateProposerId(self):
        
        NumberOfPeers = len(self.peers)

        if len(self.peers) < 1 or self.blockChain.chain[-1].proposerId == -1:
            return 0

        index = self.blockChain.chain[-1].proposerId + 1 % NumberOfPeers
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
