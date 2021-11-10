
from typing_extensions import Concatenate

import json

import time

from Packages.Serialization.Serialization import Serialization

from .Block import Block


class BlockChain:

    #initialGroupMembers = list
    #RoleDefinitions = List of Dict
    #PermissionDefinitions = List of Dict
    # RoleDict = Dict of lists
    def __init__(self, chain = None, length = None, initialGroupMemebers = None, RoleDefinitions = None, PermissionDefinitions = None, RoleDict = None):


        if length != None:
            self.length = length
        else:
            self.length = 0
        if chain != None:
            self.chain = chain
        else:
            self.chain = []
            self.create_genesis_block(initialGroupMemebers, RoleDefinitions, PermissionDefinitions, RoleDict)


    def create_genesis_block(self, initialGroupMemebers, RoleDefinitions, PermissionDefinitions, RoleDict):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        transactions = []

        groupDef = {
            "messageType": "GroupDef",
            "hash": "",
            "creator": "-1",
            "groupType": "People",
            "entities": initialGroupMemebers,
            "description": "Initial Group"
        }

        groupHash = Serialization.hashGroupDef(groupDef)

        groupDef["hash"] = groupHash

        transactions.append(groupDef)

        permissionNameHashDict = {}

        for Permission in PermissionDefinitions:

            newPermission = {
                "messageType": "PermissionDescriptor",
                "name": Permission["name"],
                "type": Permission["type"],
                "scope": Permission["scope"],
                "hash": "",
                "creator": "-1"
            }
            hash = Serialization.hashPermissionDef(newPermission)

            newPermission["hash"] = hash

            permissionNameHashDict[newPermission["name"]] = hash

            transactions.append(newPermission)


        roleHashDict = {}

        for RoleDef in RoleDefinitions:
            newRole = {
                "messageType": "RoleDescriptor",
                "name": RoleDef["name"],
                "hash": "",
                "creator": "-1",
                "permissionHashes": RoleDef["permissionHashes"]
            }
            for i in range(len(RoleDef["permissionHashes"])):
                
                newRole["permissionHashes"][i] = permissionNameHashDict[newRole["permissionHashes"][i]]

            hash = Serialization.hashRoleDef(newRole)

            roleHashDict[newRole["name"]] = hash

            newRole["hash"] = hash

            transactions.append(newRole)


        for key in RoleDict:
            roleAssignment = {
                "messageType": "RoleAssignment",
                "user": key,
                "roleHash": roleHashDict[RoleDict[key]],
                "groupHash": groupHash
            }
            transactions.append(roleAssignment)



        #for tr in transactions:
           #print("----------")
            #print(tr)

        genesis_block = Block(index=0,transactions= transactions, timestamp = time.time(), previous_hash="0",proposerId=-1)
        genesis_block.hash = genesis_block.getHash()
        self.length += 1
        self.chain.append(genesis_block)

    # @property
    def last_block(self):
        return self.chain[-1]


    def add_block(self, block):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block().getHash()

        if previous_hash != block.previous_hash:
            raise Exception('block.previous_hash not equal to last_block_hash')
            return
        # else:
        #     print(str(previous_hash)+' == '+str(block.previous_hash))
        # print( 'New Hash : '+str(block.hash)+'\n\n')
        self.length += 1
        self.chain.append(block)
    
    def serializeJSON(self):
        outputStructure = {
            "length": self.length,
            "chain": []
        }

        for block in self.chain:
            outputStructure["chain"].append(block.serializeJSON())

        return json.dumps(outputStructure , sort_keys=True)

    @staticmethod
    def deserializeJSON(BlockChainString):

        blockChainDict = json.loads(BlockChainString)

        blockArray = []

        for blockString in blockChainDict["chain"]:
            #print({"blockString":blockString})
            #print({"deserializedBlock":Block.deserializeJSON(blockString)})
            blockArray.append(Block.deserializeJSON(blockString))

        blockChainDict["chain"] = blockArray

        return BlockChain(**blockChainDict)

    @staticmethod
    def getGroupById():
        print("TBI")


    def getGroupsByPublicKey(self, publicKeyString):
        outputGroups = []
        for block in self.chain:
            groups = block.findGroupsFromPublicKey(publicKeyString)
            if len(groups) > 0:
                for group in groups:
                    outputGroups.append(group)
        
        return outputGroups



