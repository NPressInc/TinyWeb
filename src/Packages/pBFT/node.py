
import time
import brotli

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

        node = PBFTNode(0, blockChain)

        PBFTNode.node = node


        BlockChainReadWrite.saveBlockChainToFile(node.blockChain)

        node.peers.append("http://127.0.0.1:"+ str(5000 + nodeId) +"/")

        newPeerList = BlockchainParser.getMostRecentPeerList(node.blockChain)
        if newPeerList != None:
            node.peers = newPeerList


        while counter < 1000:

            if counter % 10 == 0:
                BlockChainReadWrite.saveBlockChainToFile(node.blockChain)
                newPeerList = BlockchainParser.getMostRecentPeerList(node.blockChain)
                if newPeerList != None:
                    node.peers = newPeerList

            time.sleep(5)
            counter += 1
            node.proposeNewBlock()
            while MessageQueues.messageQueues.PendingBlock == None:
                time.sleep(1)
                print("Waiting for block Proposal")
            node.blockChain.add_block(MessageQueues.messageQueues.PendingBlock)
            print("Added new block, to chain with hash" + node.blockChain.last_block().getHash())

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

    def proposeNewBlock(self):
        self.ProposerId = self.calculateProposerId()
        if self.ProposerId == self.id:
            block = self.createBlock()
            self.verifyBlock(block)
            self.broadcastBlockToPeers(block)

        else:
            print("TBI")
            

    def ListenForBlockProposals(self):
        print("TBI")

    def createBlock(self):
        transactions = MessageQueues.messageQueues.transactionQueue
        # print(transactions)
        MessageQueues.messageQueues.transactionQueue = []
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
