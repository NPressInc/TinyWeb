from flask import Flask, request, jsonify
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
        return jsonify({"message": "Node not initialized"})
    
    groups = PBFTNode.node.blockChain.getGroupsByPublicKey(publicKey)

    return jsonify({"groups": groups})


    
