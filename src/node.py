import datetime
import hashlib,sys
import json
from typing_extensions import Concatenate
from MessageReciever import Transaction, app
import MessageReciever
import threading
import time
import brotli





class MerkleTreeNode:
    
    def __init__(self,value, hashValue = None, left = None, right = None):
        self.left = left
        self.right = right
        self.value = value
        if hashValue == None:
            self.hashValue = hashlib.sha256(value.encode('utf-8')).hexdigest()
        else:
            self.hashValue = hashValue
    
    def buildTree(self, transactions):
        nodes = []
        for value in transactions:
            nodes.append(MerkleTreeNode(value))

        while len(nodes)!=1:
            temp = []
            for i in range(0,len(nodes),2):
                node1 = nodes[i]
                if i+1 < len(nodes):
                    node2 = nodes[i+1]
                else:
                    node2 = nodes[i]
                #f.write("Left child : "+ node1.value + " | Hash : " + node1.hashValue +" \n")
                #f.write("Right child : "+ node2.value + " | Hash : " + node2.hashValue +" \n")
                concatenatedHash = node1.hashValue + node2.hashValue
                parent = MerkleTreeNode(concatenatedHash)
                parent.left = node1
                parent.right = node2
                #f.write("Parent(concatenation of "+ node1.value + " and " + node2.value + ") : " +parent.value + " | Hash : " + parent.hashValue +" \n")
                temp.append(parent)
            nodes = temp
        return nodes[0]


    def testTree(self):
        inputString = sys.argv[1]
        leavesString = inputString[1:len(inputString)-1]
        leaves = leavesString.split(",")
        f = open("merkle.tree", "w")
        root = self.buildTree(leaves,f)
        f.close()
    
    @staticmethod
    def DeserializeJSON(SerializedTreeNode):
        merkleTreeNodeDict = json.loads(SerializedTreeNode)
        return MerkleTreeNode(**merkleTreeNodeDict)


    def serializeJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


    


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
            print()
        else:
            outputStruct = {
                "index": self.index,
                "timestamp": self.timestamp,
                "previousHash": self.previous_hash,
                "merkleRoot": "Empty"
            }
        block_string = json.dumps(outputStruct, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    
    @staticmethod
    def deserializeJSON(jsonString):
        blockDict = json.loads(jsonString)
        blockDict["merkleTree"] = MerkleTree.deserializeJSON(blockDict["merkleTree"])
        return Block(**blockDict)
        
    
    def serializeJSON(self):
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

        """
        self.index          = index
        self.transactions   = transactions
        self.timestamp      = timestamp
        self.hash           = ''
        self.previous_hash  = previous_hash
        self.proposerId = proposerId
        self.merkleTree     = merkleTree
        """

        return json.dumps(outputStruct , indent=4, sort_keys=True)


class Blockchain:
    def __init__(self):
        self.commit_counter = 0
        self.length = 0
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, ["Genenesis Block"], 0, "0", 0)
        genesis_block.hash = genesis_block.compute_hash()
        self.length += 1
        self.chain.append(genesis_block)

    # @property
    def last_block(self):
        return self.chain[-1]

    def last_block_hash(self):
        tail = self.chain[-1]

        # print(tail.transactions)

        return tail.hash

    def update_commit_counter(self):
        self.commit_counter += 1

    def add_block(self, block):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block_hash()

        if previous_hash != block.previous_hash:
            raise Exception('block.previous_hash not equal to last_block_hash')
            # print('block.previous_hash not equal to last_block_hash')
            return
        # else:
        #     print(str(previous_hash)+' == '+str(block.previous_hash))


        block.hash = block.compute_hash()
        # print( 'New Hash : '+str(block.hash)+'\n\n')
        self.length += 1
        self.chain.append(block)

    
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





#block.get_json()




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
        MessageReciever.transactionQueue = []
        #index, transactions, timestamp, previous_hash, proposerId
        newIndex = self.blockChain.length
        timestamp = datetime.datetime.now
        previousHash = self.blockChain.chain[-1].hash
        proposerId = self.id
        newIndex = self.blockChain.length
        block = Block(newIndex, transactions, timestamp, previousHash,proposerId)
        return block

    

    @staticmethod
    def verifyBlock(block):
        print("include functionality for sending rejection messages to originators of faulty messages. Do this on a seperate thread.")
        print("TBI")
        return True

    def  broadcastBlockToPeers(self, block):
        import requests
        import json 

        for peer in self.peers:
            print(block.toJSON())
            r = requests.post(self.PeerIpDict[peer], json.dumps(block.__dict__))
            print(r.status_code)
            print(r.json())

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


def threadFunc():
    blockChain =Blockchain()
    time.sleep(5)
    node = PBFTNode(0, blockChain)
    node.peers.append("me")
    node.PeerIpDict["me"] = "http://127.0.0.1:5000/"
    node.proposeNewBlock()

def runFlask():
    app.run(debug=False)

"""

thServer = threading.Thread(target=runFlask)


th = threading.Thread(target=threadFunc)

th.start()

thServer.start()

time.sleep(30)

th.join()

thServer.join

"""





