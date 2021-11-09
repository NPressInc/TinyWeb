import datetime
import hashlib,sys
import json
from typing_extensions import Concatenate
import threading
import time
import brotli

from Packages.Serialization.Serialization import Serialization
from ..structures.BlockChain.BlockChain import BlockChain
from ..structures.BlockChain.Block import Block
from ..Verification.BlockVerification import BlockVerification
from ..Communication.MessageReciever import messageQueues
from ..FileIO.readLoadBlockChain import BlockChainReadWrite
from ..structures.Client.TinyWebClient import TinyWebClient
from ..Verification.Signing import Signing
from ..structures.RolesAndPermissions.RoleDefinitions import MegaAdminRole, RoleDefinitions
from ..structures.RolesAndPermissions.PermissionDefinitions import PermissionDefinitions



class PBFTNode:

    @staticmethod 
    def configureBlockChainForFirstUse():
        client1 = TinyWebClient.initializeClient("1")
        client2 = TinyWebClient.initializeClient("2")
        client3 = TinyWebClient.initializeClient("3")

        baseGroupPublicKeys = []
        client1PublicKeyString = Signing.PublicKeyMethods.serializePublicKey(client1.publicKey)
        baseGroupPublicKeys.append(client1PublicKeyString)

        client2PublicKeyString = Signing.PublicKeyMethods.serializePublicKey(client2.publicKey)
        baseGroupPublicKeys.append(client2PublicKeyString)

        client3PublicKeyString = Signing.PublicKeyMethods.serializePublicKey(client3.publicKey)
        baseGroupPublicKeys.append(client3PublicKeyString)


        print(RoleDefinitions)

        print(PermissionDefinitions)


        RoleDict = {}

        RoleDict[client1PublicKeyString] = ["SuperMemberRole"]

        RoleDict[client2PublicKeyString] = ["MemberRole"]

        RoleDict[client3PublicKeyString] = ["SubMemberRole"]
        

        blockChain = BlockChain(initialGroupMemebers= baseGroupPublicKeys, RoleDefinitions=RoleDefinitions, PermissionDefinitions=PermissionDefinitions,RoleDict=RoleDict )

        print(blockChain.serializeJSON())

        return blockChain

        


    @staticmethod
    def runNode():
        blockChain = PBFTNode.configureBlockChainForFirstUse()

        counter = 0
        
        while counter < 4:
            time.sleep(3)
            counter += 1
            node = PBFTNode(0, blockChain)
            node.peers.append("me")
            node.PeerIpDict["me"] = "http://127.0.0.1:5000/"
            node.proposeNewBlock()
            node.blockChain.add_block(messageQueues.PendingBlock)

        #print("Pre Save")
        #print(blockChain.serializeJSON())
        BlockChainReadWrite.saveBlockChainToFile(node.blockChain)


        time.sleep(2)

        #print("POST Read")
        blockChainRecovered = BlockChainReadWrite.readBlockChainFromFile()

    
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
        transactions = messageQueues.transactionQueue
        #print(transactions)
        messageQueues.transactionQueue = []
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









