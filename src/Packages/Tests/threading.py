import time
import threading
import importlib.util
import sys
from typing import Counter

from ..Communication.MessageReciever import app
from ..structures.BlockChain.BlockChain import BlockChain
from ..pBFT.node import PBFTNode

from ..FileIO.readLoadBlockChain import BlockChainReadWrite

from ..Communication.MessageReciever import messageQueues

from ..Tests.ClientSimulator import ClientSimulator



class ThreadingTests:
    @staticmethod
    def NodeTestFunc():
        
        blockChain = BlockChainReadWrite.readBlockChainFromFile()

        print(blockChain.serializeJSON())

        counter = 0
        
        while counter < 4:
            time.sleep(3)
            counter += 1
            node = PBFTNode(0, blockChain)
            node.peers.append("me")
            node.PeerIpDict["me"] = "http://127.0.0.1:5000/"
            node.proposeNewBlock()
            node.blockChain.add_block(messageQueues.PendingBlock)

        #print("Pre Save")
        #print(blockChain.serializeJSON())
        BlockChainReadWrite.saveBlockChainToFile(node.blockChain)


        time.sleep(2)

        #print("POST Read")
        blockChainRecovered = BlockChainReadWrite.readBlockChainFromFile()
        #print(blockChainRecovered.serializeJSON())

    @staticmethod
    def runFlask():
        app.run(debug=False)

    @staticmethod
    def runFauxClient():
        CS = ClientSimulator()
        CS.sendTransactionsEverySoOften(1, 12)
        

    @staticmethod
    def threadingTest():
        FlaskThread = threading.Thread(target=ThreadingTests.runFlask)
        nodeTestThread = threading.Thread(target=ThreadingTests.NodeTestFunc)
        FauxClientThread = threading.Thread(target=ThreadingTests.runFauxClient)

        nodeTestThread.start()

        FlaskThread.start()

        FauxClientThread.start()



        time.sleep(1000)



        FauxClientThread.join()

        nodeTestThread.join()

        FlaskThread.join


