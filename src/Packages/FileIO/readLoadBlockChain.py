from os import stat
import json

from brotli.brotli import compress
from ..structures.BlockChain.BlockChain import BlockChain
from ..Serialization.Serialization import Serialization
import brotli

class BlockChainReadWrite:
    @staticmethod
    def testFileWrite():
        f = open("State/demofile.txt","a")
        f.write("this is a blockchain")
        f.close()

    def saveBlockChainToFile(blockChain: BlockChain):
        jsonString = blockChain.serializeJSON()

        #print(jsonString)

        #print("DifferentBytesLength")

        bytess = str.encode(jsonString)
        #print(len(bytess))

        bytess2 = str.encode("asdf")
        #print(len(bytess2))

        compressedBytes = brotli.compress(str.encode(jsonString))

        compressedString2 = brotli.compress(str.encode("asdf"))

        #print(len(compressedBytes))

        #print(len(compressedString2))

        recoveredBytes = brotli.decompress(compressedBytes)

        #print(recoveredBytes.decode())


        f = open("State/currentBlockChain.dat","wb")
        f.write(compressedBytes)
        f.close()
        print("Saved BlockChain To File!")
    
    def readBlockChainFromFile():
        
        f = open("State/currentBlockChain.dat","rb")

        CompressedBlockChainBytes = f.read()

        #print(len(CompressedBlockChainBytes))
        blckChain = {}
        #try:
        BlockChainBytes = brotli.decompress(CompressedBlockChainBytes)

        #print(len(BlockChainBytes))

        decompressedString = BlockChainBytes.decode()

        #print(decompressedString)

        blckChain = BlockChain.deserializeJSON(decompressedString)
        print("Loaded it")

        #except:
            #blckChain = BlockChain()
            #print("Initialized New BlockChain")

        print(blckChain.serializeJSON())

        f.close()

        return blckChain

