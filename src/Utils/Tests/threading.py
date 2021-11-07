import time
import threading
import importlib.util
import sys
spec = importlib.util.spec_from_file_location("BlockChain", "structures/BlockChain/BlockChain.py")
BlockChain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BlockChain)

spec = importlib.util.spec_from_file_location("MessageReciever", "Utils/Communication/MessageReciever.py")
MessageReciever = importlib.util.module_from_spec(spec)
spec.loader.exec_module(MessageReciever)


spec = importlib.util.spec_from_file_location("PBFTNode", "Utils/pBFT/node.py")
PBFTNode = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PBFTNode)



class ThreadingTests:
    @staticmethod
    def threadFunc():
        
        blockChain =print(BlockChain.BlockChain())
        time.sleep(5)
        node = PBFTNode(0, blockChain)
        node.peers.append("me")
        node.PeerIpDict["me"] = "http://127.0.0.1:5000/"
        node.proposeNewBlock()

    @staticmethod
    def runFlask():
        MessageReciever.app.run(debug=False)

    @staticmethod
    def threadingTest():
        thServer = threading.Thread(target=ThreadingTests.runFlask)
        th = threading.Thread(target=ThreadingTests.threadFunc)

        th.start()

        #thServer.start()

        time.sleep(30)

        th.join()

        #thServer.join


