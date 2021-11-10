from flask import Flask, request
import json

from Packages.structures.BlockChain.BlockParser import BlockParser
from Packages.structures.BlockChain.BlockchainParser import BlockchainParser
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

