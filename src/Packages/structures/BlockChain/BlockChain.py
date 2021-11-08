
from typing_extensions import Concatenate

import json

from .Block import Block


class BlockChain:
    def __init__(self, chain = None, length = None):


        if length != None:
            self.length = length
        else:
            self.length = 0
        if chain != None:
            self.chain = chain
        else:
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


    def add_block(self, block):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block().hash

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
            print({"blockString":blockString})
            print({"deserializedBlock":Block.deserializeJSON(blockString)})
            blockArray.append(Block.deserializeJSON(blockString))

        blockChainDict["chain"] = blockArray

        return BlockChain(**blockChainDict)

