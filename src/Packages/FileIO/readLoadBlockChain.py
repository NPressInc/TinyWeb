

from ..Structures.BlockChain.BlockChain import BlockChain
from ..Serialization.Serialization import Serialization
import brotli

class BlockChainReadWrite:
    @staticmethod
    def testFileWrite():
        f = open("State/demofile.txt","a")
        f.write("this is a blockchain")
        f.close()

    def saveBlockChainToFile(blockChain: BlockChain, nodeId):
        jsonString = blockChain.serializeJSON()

        compressedBytes = brotli.compress(str.encode(jsonString))


        f = open("State/currentBlockChain" + str(nodeId)+".dat","wb")
        f.write(compressedBytes)
        f.close()
        print("Saved BlockChain To File!")
    
    def readBlockChainFromFile(nodeId):

        try:
            f = open("State/currentBlockChain"+str(nodeId)+".dat","rb")

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

        
        

