

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

        compressedBytes = brotli.compress(str.encode(jsonString))


        f = open("State/currentBlockChain.dat","wb")
        f.write(compressedBytes)
        f.close()
        print("Saved BlockChain To File!")
    
    def readBlockChainFromFile():

        try:
            f = open("State/currentBlockChain.dat","rb")

            CompressedBlockChainBytes = f.read()

            blckChain = {}
        
            BlockChainBytes = brotli.decompress(CompressedBlockChainBytes)

            decompressedString = BlockChainBytes.decode()

            blckChain = BlockChain.deserializeJSON(decompressedString)
            print("Loaded it")

            f.close()

            return blckChain
        except Exception as err:
            print(err)
            return None

        
        

