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


"""

lastHash = '500ee86d269942852a3598a705d11e4fb93652d38cc3d897726592876904b62c'
hashes = ['4226f79fc5ee5d2361b29f8fd84d3ff33ab098d20d27a21c31589465d04bb02a', '500ee86d269942852a3598a705d11e4fb93652d38cc3d897726592876904b62c', 'e3ba15650aee7e667c72949dd763c6684def3e7b23a984ab0150af71a0fc37e3', 'de97f5f27f0f7519642d55a18bbe8547801bf20f63aad780a30e190302282612', '89423dd92007814a93fd9d2727863a95243115f7f9a7abdd5a2e8f8231a41935']

missingHashes = []

for i in range(len(hashes)-1 ,-1,-1):
    print(i)
    currentHash = hashes[i]
    print({"Missing Block Request current Hash Scanned":currentHash})
    if currentHash != lastHash:
        missingHashes.append(currentHash)
    else:
        break

print(missingHashes)

exit()

"""


def runNodeFlask():
    from waitress import serve
    app.run(debug=False, port=5000 + nodeId)
    serve(app, host="127.0.0.1", port=(5000 + nodeId))

def runBlockChainApiFlask():
    BCQapp.run(debug=False, port=5050 + nodeId)

#runBlockChainApiFlask
#BCQAThread = threading.Thread(target=runBlockChainApiFlask)
FlaskThread = threading.Thread(target=runNodeFlask)
RunNodeThread = threading.Thread(target=PBFTNode.runNode)

RunNodeThread.start()

FlaskThread.start()

#BCQAThread.start()


time.sleep(1000)


#BCQAThread.join()

RunNodeThread.join()

FlaskThread.join