from Packages.Tests.threading import ThreadingTests
from Packages.pBFT.node import PBFTNode
from Packages.Communication.NodeFlaskApi import app
from Packages.Communication.BlockChainQueryApi import BCQapp

import threading
import time

import sys
nodeId = 0

if len(sys.argv) > 2:
    nodeId = int(sys.argv[2])

def runNodeFlask():
    app.run(debug=False, port=5000 + nodeId)

def runBlockChainApiFlask():
    BCQapp.run(debug=False, port=5050 + nodeId)

#runBlockChainApiFlask
BCQAThread = threading.Thread(target=runBlockChainApiFlask)
FlaskThread = threading.Thread(target=runNodeFlask)
RunNodeThread = threading.Thread(target=PBFTNode.runNode)

RunNodeThread.start()

FlaskThread.start()

BCQAThread.start()


time.sleep(1000)


BCQAThread.join()

RunNodeThread.join()

FlaskThread.join