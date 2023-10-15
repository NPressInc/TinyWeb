
import hashlib,sys
import json

from ...Serialization.Serialization import Serialization

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
            sort_keys=True)


    