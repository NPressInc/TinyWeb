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
    def threadingTest():
        FlaskThread = threading.Thread(target=ThreadingTests.runNodeFlask)
        nodeTestThread = threading.Thread(target=ThreadingTests.NodeTestFunc)

        nodeTestThread.start()

        FlaskThread.start()




        time.sleep(1000)




        nodeTestThread.join()

        FlaskThread.join


