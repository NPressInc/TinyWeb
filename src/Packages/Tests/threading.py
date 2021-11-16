import time
import threading
import importlib.util
import sys
from typing import Counter


from ..structures.BlockChain.BlockChain import BlockChain
from ..pBFT.node import PBFTNode

from ..FileIO.readLoadBlockChain import BlockChainReadWrite



from ..Client.ClientSimulator import ClientSimulator



class ThreadingTests:


    @staticmethod
    def runFauxClient():
        CS = ClientSimulator()
        CS.sendTransactionsEverySoOften(1, 12)
        

    @staticmethod
    def threadingTest():
        FlaskThread = threading.Thread(target=ThreadingTests.runNodeFlask)
        nodeTestThread = threading.Thread(target=ThreadingTests.NodeTestFunc)
        FauxClientThread = threading.Thread(target=ThreadingTests.runFauxClient)

        nodeTestThread.start()

        FlaskThread.start()

        FauxClientThread.start()



        time.sleep(1000)



        FauxClientThread.join()

        nodeTestThread.join()

        FlaskThread.join


