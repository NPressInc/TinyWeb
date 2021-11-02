#!/usr/bin/python3
import hashlib,sys
import datetime
import hashlib,sys
import json
from typing_extensions import Concatenate
from MessageReciever import Transaction, app
import MessageReciever
import threading
import time
import brotli
from ..MerkleTreeNode.MerkleTreeNode import MerkleTreeNode



class MerkleTree:

    

    def __init__(self,rootNode: MerkleTreeNode,  size = None, rootHash = None, depth=None):
        self.rootNode = rootNode
        self.rootHash = rootNode.hashValue
        self.size = size
        if depth == None:
            self.depth = self.findClosestSquare(self.size)
        else:
            self.depth = depth


    @staticmethod
    def findClosestSquare(size):
        product = 1
        output = 0
        while product < size:
            product = product * 2
            output += 1
        
        return output
        

    

    def getTransactionNodeFromIndex(self, index):

        if index > self.size -1:
            return None

        navigation = ["0"]* self.depth

        binaryRep = bin(index)
        binaryRep = binaryRep[2:]


        for i in range(len(binaryRep)-1, -1, -1):
            #print(i)
            navigation[(len(navigation)) - (len(binaryRep) - i) ] = binaryRep[i]

        currNode = self.rootNode
        for direction in navigation:
            print(currNode.value)
            if direction == "0":
                currNode = currNode.left
            else:
                currNode = currNode.right
        return currNode

    def verifyTransactionHashByIndex(self, index):

        if index > self.size -1:
            return False

        navigation = ["0"]* self.depth

        binaryRep = bin(index)

        binaryRep = binaryRep[2:]

        for i in range(len(binaryRep)-1, -1, -1):
            #print(i)
            navigation[(len(navigation)) - (len(binaryRep) - i) ] = binaryRep[i]
        
        parenthashes = []
        neighborHashes = []
        valuesDebug = []

        currNode = self.rootNode
        print(navigation)
    
        for direction in navigation:
            parenthashes.append(currNode.hashValue)
            valuesDebug.append(currNode.value)
            #print("added Parent")
            if direction == "0":
                neighborHashes.append(currNode.right.hashValue)
                currNode = currNode.left
                #print("added right leaf")
                #print("navigated left")
            else:
                neighborHashes.append(currNode.left.hashValue)
                #print("added left leaf")
                currNode = currNode.right
                #print("nagivated right")
                
                
        
        if hashlib.sha256(currNode.value.encode('utf-8')).hexdigest() != currNode.hashValue:
            return {currNode.value: False}
        
        currentHash = currNode.hashValue

        
        
        #print({"neighbors": neighborHashes})
        #print({"parents": parenthashes})
        #print({"values": valuesDebug})

        for i in range(len(parenthashes)-1, -1, -1):
            
            if navigation[i] == "0":
                #print("here1")
                #print({"currentHash": currentHash})
                #print(i)
                #print({"neighbor": neighborHashes[i]})
                ConcatenatedHashes = currentHash + neighborHashes[i]
                #print({"concatenated": ConcatenatedHashes})
                hashResult = hashlib.sha256(ConcatenatedHashes.encode('utf-8')).hexdigest()
                #print({"hashResult": hashResult})
                if hashResult != parenthashes[i]:
                    return {currNode.value: False}
                currentHash = hashResult

            else:
                #print("here2")
                #print({"currentHash": currentHash})

                ConcatenatedHashes =  neighborHashes[i] + currentHash
                #print({"concatenated": ConcatenatedHashes})
                hashResult = hashlib.sha256(ConcatenatedHashes.encode('utf-8')).hexdigest()
                #print({"hashResult": hashResult})
                if hashResult!= parenthashes[i]:
                    return {currNode.value: False}
                currentHash = hashResult
            print("level:" + str(i) + " validated")


        print(currentHash)
        

        return {currNode.value: True}
    """
    def verifyTransactionByTransactionString(self, transactionString):
        if not(transactionString in self.IndexMap):
            return {transactionString: False}

        index = self.IndexMap[transactionString]

        return self.verifyTransactionHashByIndex(index)
    
    """
    
    
    @staticmethod
    def deserializeJSON(merkleTreeString):
        merkleTreeDict = json.loads(merkleTreeString)

        merkleNodeDict = json.loads(merkleTreeDict["rootNode"])

        merkleTreeDict["rootNode"] = MerkleTreeNode(**merkleNodeDict)

        return MerkleTree(**merkleTreeDict)


    def serializeJSON(self):
        output = {
            "rootNode" : self.rootNode.serializeJSON(),
            "rootHash": self.rootHash,
            "size": self.size,
            "depth": self.depth
        }
        return json.dumps(output, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    """
    def toCustomStringRepresentation(self):
        
            outputString = ""
            visited = []
            queue = []
            
            visited.append(self.rootNode)
            queue.append(self.rootNode)

            while queue:
                currentNode = queue.pop(0) 
                outputString += currentNode.value + " : " + currentNode.hashValue + "||||"

                if currentNode.left not in visited and currentNode.left != None:
                    visited.append(currentNode.left)
                    queue.append(currentNode.left)

                if currentNode.right not in visited and currentNode.right != None:
                    visited.append(currentNode.right )
                    queue.append(currentNode.right )
            return outputString
        
    
    """
    
   
   
   
    
   

"""
transactions = ["a=1", "b=2", "c=3","d=4", "e=5","f=6", "g=7", "h=8", "i=9", "j=10","k=11"]

block = Block(0,transactions,str(datetime.datetime.now()) ,"0", 0)

block.compute_hash()

blockString = block.serializeJSON()

print(blockString)

newBlock = block.deserializeJSON(blockString)

if newBlock.hash == block.hash:
    print("Success!")
else:
    print("failure :(")
"""