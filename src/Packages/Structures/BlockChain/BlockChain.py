
from typing_extensions import Concatenate

import hashlib

import json

import time

from Packages.Structures.BlockChain.Transaction import Transaction
from nacl.public import PublicKey
from .Block import Block


class BlockChain:

    #initialGroupMembers = list
    #RoleDefinitions = List of Dict
    #PermissionDefinitions = List of Dict
    # RoleDict = Dict of lists
    def __init__(self, chain = None, length = None, creatorPublicKey: PublicKey = None):


        if length != None:
            self.length = length
        else:
            self.length = 0
        if chain != None:
            self.chain = chain
        else:
            self.chain = []
            self.create_genesis_block(creatorPublicKey)


    def create_genesis_block(self, creatorPublicKey):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        transactions = []

        transactions.append(Transaction(
            messageType="CreatorAssignment",
            sender=creatorPublicKey,
            peers=[],
            publicKeys=[creatorPublicKey],
            ids=[0]
        ))

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

        #print({"blockchain before adding":self.getListOfBlockHashes()})


        previous_hash = self.last_block().getHash()

        #print({"adding block, last hash": previous_hash})

        #print({"adding block, proposed block previous hash": block.previous_hash})

        if previous_hash != block.previous_hash:
            raise Exception('block.previous_hash not equal to last_block_hash')
            return
        # else:
        #     print(str(previous_hash)+' == '+str(block.previous_hash))
        # print( 'New Hash : '+str(block.hash)+'\n\n')
        self.length += 1
        self.chain.append(block)

        #print({"blockchain after adding":self.getListOfBlockHashes()})
    
    def serializeJSON(self):
        outputStructure = {
            "length": self.length,
            "chain": []
        }

        for block in self.chain:
            outputStructure["chain"].append(block.serializeJSON())

        return json.dumps(outputStructure , sort_keys=True)

    def getHash(self):
        BCString = self.serializeJSON()
        hash = hashlib.sha256(BCString.encode()).hexdigest()
        return hash

    def getListOfBlockHashes(self):
        output = []
        for block in self.chain:
            output.append(block.getHash())
        return output


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

    



