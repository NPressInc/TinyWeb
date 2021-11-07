import time
import threading
import importlib.util
import sys

from ..Communication.MessageReciever import app
from ..structures.BlockChain.BlockChain import BlockChain
from ..pBFT.node import PBFTNode



class ThreadingTests:
    @staticmethod
    def threadFunc():
        
        blockChain = BlockChain()
        time.sleep(5)
        node = PBFTNode(0, blockChain)
        node.peers.append("me")
        node.PeerIpDict["me"] = "http://127.0.0.1:5000/"
        node.proposeNewBlock()

    @staticmethod
    def runFlask():
        app.run(debug=False)

    @staticmethod
    def threadingTest():
        thServer = threading.Thread(target=ThreadingTests.runFlask)
        th = threading.Thread(target=ThreadingTests.threadFunc)

        th.start()

        thServer.start()

        time.sleep(30)

        th.join()

        thServer.join


