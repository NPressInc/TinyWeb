import datetime
import hashlib,sys
import json
from typing_extensions import Concatenate
import threading
import time
import brotli
from structures.BlockChain.BlockChain import BlockChain
from structures.BlockChain.Block import Block
from Utils.Verification.BlockVerification import BlockVerification




class PBFTNode:
    
    def __init__(self, id, blockChain):
        self.__privateKkey = None
        self.publicKey = None

        self.id = id #id represents the order in which nodes act as the proposer

        self.peers = []

        self.ProposerId = 0

        self.blockChain = blockChain

        self.PeerIpDict = {}



    def proposeNewBlock(self):
        self.ProposerId = self.calculateProposerId()
        print(self.ProposerId)
        print(self.id)
        if  self.ProposerId == self.id:
            block = self.createBlock()
            self.verifyBlock(block)
            self.broadcastBlockToPeers(block)
        
        else:
            print("Listen for block proposals")

    def ListenForBlockProposals(self):
        print("TBI")


    def createBlock(self):
        transactions = MessageReciever.transactionQueue
        #print(transactions)
        MessageReciever.transactionQueue = []
        newIndex = self.blockChain.length
        timestamp = time.time()
        #print(timestamp)
        previousHash = self.blockChain.chain[-1].hash
        proposerId = self.id
        newIndex = self.blockChain.length
        block = Block(newIndex, transactions, timestamp, previousHash,proposerId)
        block.compute_hash()
        return block

    

    @staticmethod
    def verifyBlock(block):

        print("include functionality for sending rejection messages to originators of faulty messages. Do this on a seperate thread.")
        print("TBI")
        return True

    def  broadcastBlockToPeers(self, block):
        import requests

        for peer in self.peers:
            #print(block.serializeJSON())
            url = self.PeerIpDict[peer] + "ProposeBlock"
            data = block.serializeJSON()
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=data, headers=headers)
            print(r.status_code)
            #print(r)

        print("Done Broadcasting new block")


    def calculateProposerId(self):
        print("TBI: returns 0 every time")
        print("algo: take the previous block proposerId and add 1 % len(peers)")
        NumberOfPeers = len(self.peers) 

        if len(self.peers) < 1:
            return 0

        index = self.blockChain.chain[-1].proposerId + 1 % NumberOfPeers
        return index
    
    @staticmethod
    def compressJson(input):
        return brotli.compress(input)

    @staticmethod
    def decompressJson(input):
        return brotli.decompress(input)









