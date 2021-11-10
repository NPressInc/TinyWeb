from Packages.Tests.threading import ThreadingTests
from Packages.pBFT.node import PBFTNode

import threading
import time

#runBlockChainApiFlask
BCQAThread = threading.Thread(target=ThreadingTests.runBlockChainApiFlask)
FlaskThread = threading.Thread(target=ThreadingTests.runNodeFlask)
RunNodeThread = threading.Thread(target=PBFTNode.runNode)
FauxClientThread = threading.Thread(target=ThreadingTests.runFauxClient)

RunNodeThread.start()

FlaskThread.start()

BCQAThread.start()


time.sleep(1000)


BCQAThread.join()

RunNodeThread.join()

FlaskThread.join