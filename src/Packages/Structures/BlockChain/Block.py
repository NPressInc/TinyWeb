
import hashlib
import json

from Packages.Serialization.Serialization import Serialization
from ..MerkleTree.MerkleTreeNode import MerkleTreeNode
from ..MerkleTree.MerkleTree import MerkleTree
from Packages.Structures.BlockChain.Transaction import Transaction

 
class Block:
    def __init__(self, index, transactions: list[Transaction], timestamp, previous_hash, proposerId, merkleTree = None, TransactionHashIndexMap = None):
        self.index          = index
        self.transactions   = transactions
        self.timestamp      = timestamp
        self.previous_hash  = previous_hash
        self.proposerId = proposerId
        self.merkleTree     = merkleTree
        if merkleTree == None:
            self.buildMerkleTree()
        if TransactionHashIndexMap == None:
            self.TransactionHashIndexMap = self.getDictFromTransactions(transactions)
        else:
            self.TransactionHashIndexMap = TransactionHashIndexMap

    @staticmethod
    def getDictFromTransactions(transactions: list[Transaction]):
        output = {}
        for i in range(len(transactions)):
            output[transactions[i].hash()] = i
        return output

    def buildMerkleTree(self):
        """
        A function that return the hash of the block contents.
        """
        if len(self.transactions) > 0:
            rootNode = MerkleTreeNode("")
            transactionStrings = []
            for tr in self.transactions:
                transactionStrings.append(tr.serializeJson())


            rootNode = rootNode.buildTree(transactionStrings)
            
            self.merkleTree = MerkleTree(rootNode, len(self.transactions))
        else:
            self.merkleTree = "Empty"

    def getHash(self):
        block_string = self.serializeJSONForHashing()
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    
    @staticmethod
    def deserializeJSON(jsonString):
        blockDict = Serialization.deserializeObjFromJsonR(jsonString)
        if blockDict["merkleTree"] != "Empty":
            blockDict["merkleTree"] = MerkleTree.deserializeJSON(blockDict["merkleTree"])

        dictTransactions = []

        
        for tr in blockDict["transactions"]:
            data = tr

            while isinstance(data, str):
                data = json.loads(data)

            
            dictTransactions.append(data)

        blockDict["transactions"] = dictTransactions
        
        
        return Block(**blockDict)


        
    def serializeJSONForHashing(self):
        if self.merkleTree != None and self.merkleTree != "Empty":

            transactionStrings = []
            for tr in self.transactions:
                transactionStrings.append(tr.serializeJson())

            outputStruct = {
                    "index": self.index,
                    "transactions": transactionStrings,
                    "timestamp": self.timestamp,
                    "previous_hash": self.previous_hash,
                    "proposerId": self.proposerId,
                    "merkleTree": self.merkleTree.serializeJSON()
            }
        else:
            outputStruct = {
                    "index": self.index,
                    "transactions": [],
                    "timestamp": self.timestamp,
                    "previous_hash": self.previous_hash,
                    "proposerId": self.proposerId,
                    "merkleTree": "Empty"
            }
        

     

        return json.dumps(outputStruct , sort_keys=True)
    
    def serializeJSON(self):

        if self.merkleTree != None and self.merkleTree != "Empty":

            transactionStrings = []
            for tr in self.transactions:
                transactionStrings.append(tr.serializeJson())

            outputStruct = {
                    "index": self.index,
                    "transactions": transactionStrings,
                    "timestamp": self.timestamp,
                    "previous_hash": self.previous_hash,
                    "proposerId": self.proposerId,
                    "merkleTree": self.merkleTree.serializeJSON()
            }
        else:
            outputStruct = {
                    "index": self.index,
                    "transactions": [],
                    "timestamp": self.timestamp,
                    "previous_hash": self.previous_hash,
                    "proposerId": self.proposerId,
                    "merkleTree": "Empty"
            }

           

        return json.dumps(outputStruct , sort_keys=True)
