from Packages.Encryption.Encryption import Encryption
from flask import Flask, request
import json
import base64
from Packages.structures.BlockChain.Parsers.BlockParser import BlockParser
from Packages.structures.BlockChain.Parsers.BlockchainParser import BlockchainParser
from ..Serialization.Serialization import Serialization

from ..pBFT.node import PBFTNode

BCQapp = Flask(__name__)


@BCQapp.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@BCQapp.route("/CheckBlockChain")
def CheckBlockChain():
    return "<p>Hello, World!</p>"



@BCQapp.route("/GetAllGroups", methods=['POST'])
def GetAllGroups():
    jsn = request.get_json()

    print(jsn)

    publicKey = jsn["publicKey"]

    print(publicKey)

    print(PBFTNode.node)

    if PBFTNode.node == None:
        return json.dumps({"message": "Node not initialized"})

    groups = BlockchainParser.getGroupsByPublicKey(PBFTNode.node.blockChain,publicKey)

    return json.dumps(groups)


@BCQapp.route("/GetSentMessages", methods=['POST'])
def GetSentMessages():
    jsn = request.get_json()

    print(jsn)

    publicKey = jsn["publicKey"]

    print(publicKey)

    print(PBFTNode.node)

    if PBFTNode.node == None:
        return json.dumps({"message": "Node not initialized"})

    messages = BlockchainParser.getSentMessagesFromPublicKey(PBFTNode.node.blockChain,publicKey)

    return json.dumps(messages)

@BCQapp.route("/GetReceivedMessages", methods=['POST'])
def GetReceivedMessages():
    jsn = request.get_json()

    print(jsn)

    publicKey = jsn["publicKey"]

    print(publicKey)

    print(PBFTNode.node)

    if PBFTNode.node == None:
        return json.dumps({"message": "Node not initialized"})

    messages = BlockchainParser.getRecievedMessagesFromPublicKey(PBFTNode.node.blockChain,publicKey)

    return json.dumps(messages)


@BCQapp.route("/SendMessage", methods=['POST']) #Test Only, delete for production
def SendMessage():
    jsn = request.get_json()
    print(jsn)

    digest = Encryption.getDigest("mySecretKey".encode("utf-8"))

    iv = Serialization.getOriginalBytesFromBase64String(jsn["iv"])

    cipher = Serialization.getOriginalBytesFromBase64String(jsn["message"])

    print({"iv": iv})

    print({"cipher": cipher})

    print(Encryption.AESDecrypt(digest, iv, cipher).decode())

    return "ok"




@BCQapp.route("/CheckDigestParity", methods=['POST']) #Test Only, delete for production
def CheckDigestParity():
    jsn = request.get_json()
    print(jsn)

    print(Serialization.getOriginalBytesFromBase64String(jsn["publicKey"]))

    digest = Encryption.getDigest("mySecretKey".encode("utf-8"))

    print({"type2": type(digest)})

    res = Serialization.getBase64String(digest)

    output = {"data": res, "source": "python Digest checker"}

    return json.dumps(output)