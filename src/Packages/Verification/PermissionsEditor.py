
from Packages.Serialization.keySerialization import keySerialization
from Packages.structures.BlockChain.Parsers.BlockchainParser import BlockchainParser
from ..Serialization.Serialization import Serialization
import requests

from ..Verification.Signing import Signing



class PermissionsEditor():

    @staticmethod
    def addSendPermissionToFledgling(fledgling, scope, type, node):

        permissions = BlockchainParser.getFledglingPermissions(fledgling, node.blockChain)

        for p in permissions:
            if p["scope"] == scope:
                print("Permissions Already Existed for")
                return 0

        permissionDescriptor = {
            "messageType": "PermissionDescriptor",
            "type": type,
            "scope": scope,
            "user": fledgling,
            "sender": keySerialization.serializePublicKey(node.publicKey)
        }

        if type == "SMS":
            permissionDescriptor["name"] = "SendMessageToGroupMemberFledgling"
        elif type == "Voice":
            permissionDescriptor["name"] = "MakeCallsToGroupFledgling"

        hash = Serialization.hashObject(permissionDescriptor)

        signature = node.signData(hash)

        data = {"signature": signature, "transaction":permissionDescriptor}

        PermissionsEditor.sendTransaction(data, node.id)

        print("Updated permission for " + fledgling)



    @staticmethod
    def sendTransaction(transactionObject, nodeId):
        try:

            url = "http://127.0.0.1:"+ str(5000 + nodeId) +"/TransactionInternal"
            data = Serialization.serializeObjToJson(transactionObject)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=data, headers=headers)
            if r.status_code == requests.codes.ok:
                print({"response from internal transaction": r.text})
                print("sent Transaction")
            else:
                print({"internal Transaction Error Code":r.status_code})
        except:
            print({"Internal Transaction Request": "Error"})



        """
            Fledgling Permission data format
            {
                "messageType": "PermissionDescriptor"
                "name": "SendMessageToGroupMember",
                "type": "SMS",
                "scope": "MemberPublicKey",
                "user": "FledglingKey"
            }
        """

