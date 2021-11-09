from Packages.Tests.threading import ThreadingTests

from Packages.FileIO.readLoadBlockChain import BlockChainReadWrite

import threading
import time

from Packages.pBFT.node import PBFTNode

FlaskThread = threading.Thread(target=ThreadingTests.runFlask)
RunNodeThread = threading.Thread(target=PBFTNode.runNode)
FauxClientThread = threading.Thread(target=ThreadingTests.runFauxClient)

RunNodeThread.start()

#FlaskThread.start()


time.sleep(1000)



RunNodeThread.join()

#FlaskThread.join