import datetime
import hashlib,sys
import json
from typing_extensions import Concatenate
import importlib.util

import threading
import time
import brotli


from ..MerkleTree.MerkleTreeNode import MerkleTreeNode

from ..MerkleTree.MerkleTree import MerkleTree

 
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, proposerId, hash=None, merkleTree = None, TransactionIndexMap = None):
        self.index          = index
        self.transactions   = transactions
        self.timestamp      = timestamp
        self.hash           = hash
        self.previous_hash  = previous_hash
        self.proposerId = proposerId
        self.merkleTree     = merkleTree
        if TransactionIndexMap == None:
            self.TransactionIndexMap = self.getDictFromTransactions(transactions)
        else:
            self.TransactionIndexMap = TransactionIndexMap

    @staticmethod
    def getDictFromTransactions(transactions):
        output = {}
        for i in range(len(transactions)):
            output[transactions[i]] = i
        return output

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """

        outputStruct = {}

        if len(self.transactions) > 0:
            rootNode = MerkleTreeNode("")
            rootNode = rootNode.buildTree(self.transactions)
            
            self.merkleTree = MerkleTree(rootNode, len(self.transactions))

            outputStruct = {
                "index": self.index,
                "timestamp": self.timestamp,
                "previousHash": self.previous_hash,
                "merkleRoot": self.merkleTree.rootHash
            }
        else:
            outputStruct = {
                "index": self.index,
                "timestamp": self.timestamp,
                "previousHash": self.previous_hash,
                "merkleRoot": "Empty"
            }
            #print(outputStruct)
            #print("Here2")
        block_string = self.serializeJSONForHashing()

        self.hash = hashlib.sha256(block_string.encode()).hexdigest()
        return self.hash
    
    
    @staticmethod
    def deserializeJSON(jsonString):
        blockDict = json.loads(jsonString)
        if blockDict["merkleTree"] != "Empty":
            blockDict["merkleTree"] = MerkleTree.deserializeJSON(blockDict["merkleTree"])

     
        if type(blockDict["TransactionIndexMap"]) == type.__str__:
            blockDict["TransactionIndexMap"] = json.loads(blockDict["TransactionIndexMap"])
        
        return Block(**blockDict)
        
    def serializeJSONForHashing(self):
        if self.merkleTree != None and self.merkleTree != "Empty":

            outputStruct = {
                    "index": self.index,
                    "transactions": self.transactions,
                    "timestamp": self.timestamp,
                    "previous_hash": self.previous_hash,
                    "proposerId": self.proposerId,
                    "merkleTree": self.merkleTree.serializeJSON(),
                    "TransactionIndexMap": self.TransactionIndexMap
            }
        else:
            outputStruct = {
                    "index": self.index,
                    "transactions": self.transactions,
                    "timestamp": self.timestamp,
                    "previous_hash": self.previous_hash,
                    "proposerId": self.proposerId,
                    "merkleTree": "Empty",
                    "TransactionIndexMap": self.TransactionIndexMap
            }


     

        return json.dumps(outputStruct , indent=0, sort_keys=True)
    
    def serializeJSON(self):
        if self.merkleTree != None and self.merkleTree != "Empty":

            outputStruct = {
                    "index": self.index,
                    "transactions": self.transactions,
                    "timestamp": self.timestamp,
                    "hash": self.hash,
                    "previous_hash": self.previous_hash,
                    "proposerId": self.proposerId,
                    "merkleTree": self.merkleTree.serializeJSON(),
                    "TransactionIndexMap": self.TransactionIndexMap
            }
        else:
            outputStruct = {
                    "index": self.index,
                    "transactions": self.transactions,
                    "timestamp": self.timestamp,
                    "hash": self.hash,
                    "previous_hash": self.previous_hash,
                    "proposerId": self.proposerId,
                    "merkleTree": "Empty",
                    "TransactionIndexMap": self.TransactionIndexMap
            }

        return json.dumps(outputStruct , sort_keys=True)
