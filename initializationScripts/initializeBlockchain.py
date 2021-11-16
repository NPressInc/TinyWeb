

from Packages.Client.TinyWebClient import TinyWebClient

from Packages.Serialization.keySerialization import keySerialization

from Packages.Serialization.Serialization import Serialization

import requests



class blockChainInitialization:

    @staticmethod
    def sendTransactionsToBlockchain():
        transactions = []
        peerDefTransaction = blockChainInitialization.initializePeerIpDictForTesting()

        transactions.append(peerDefTransaction)

        for ts in transactions:
            for i in range(0,1):
                blockChainInitialization.sendTransaction(ts, i)



    @staticmethod
    def sendTransaction(transactionObject, nodeId):
        url = "http://127.0.0.1:"+ str(5000 + nodeId) +"/Transaction"
        data = Serialization.serializeObjToJson(transactionObject)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)
        print("sent Transaction")



    @staticmethod   
    def initializePeerIpDictForTesting():
        peerList = []
        for i in range(0,4):
            peerList.append("http://127.0.0.1:" + str(5000 + i) +"/")

        transaction = {
            "messageType": "PeerList",
            "peers": peerList

        }

        return transaction

    @staticmethod
    def createRolesDefTransactions(RoleDefinitions, permissionNameHashDict):
        roleHashDict = {}
        transactions = []

        for RoleDef in RoleDefinitions:
            newRole = {
                "messageType": "RoleDescriptor",
                "name": RoleDef["name"],
                "creator": "-1",
                "permissionHashes": RoleDef["permissionHashes"]
            }
            for i in range(len(RoleDef["permissionHashes"])):
                
                newRole["permissionHashes"][i] = permissionNameHashDict[newRole["permissionHashes"][i]]

            hash = Serialization.hashRoleDef(newRole)

            roleHashDict[newRole["name"]] = hash

            transactions.append(newRole)

        return [transactions, roleHashDict]

    @staticmethod
    def createRoleAssignmentDefTransactions(RoleDict, roleHashDict, groupHash):
        transactions = []
        for key in RoleDict:
                roleAssignment = {
                    "messageType": "RoleAssignment",
                    "user": key,
                    "roleHash": roleHashDict[RoleDict[key]],
                    "groupHash": groupHash
                }
                transactions.append(roleAssignment)
        return transactions

    @staticmethod
    def createPermissionsTransactions(PermissionDefinitions):
        permissionNameHashDict = {}

        transactions = []

        for Permission in PermissionDefinitions:

            newPermission = {
                "messageType": "PermissionDescriptor",
                "name": Permission["name"],
                "type": Permission["type"],
                "scope": Permission["scope"],
                "creator": "-1"
            }
            hash = Serialization.hashPermissionDef(newPermission)

            permissionNameHashDict[newPermission["name"]] = hash

            transactions.append(newPermission)

        return [transactions, permissionNameHashDict]


    @staticmethod
    def createGroupsTransactions(initialGroupMemebers):
        groupDef = {
                "messageType": "GroupDef",
                "creator": "-1",
                "groupType": "People",
                "entities": initialGroupMemebers,
                "description": "Initial Group"
            }

        groupHash = Serialization.hashGroupDef(groupDef)

        return groupHash




    @staticmethod
    def testCreateClients():
        client1 = TinyWebClient.initializeClient("1")
        client2 = TinyWebClient.initializeClient("2")
        client3 = TinyWebClient.initializeClient("3")

        baseGroupPublicKeys = []
        client1PublicKeyString = keySerialization.serializePublicKey(
            client1.publicKey)
        baseGroupPublicKeys.append(client1PublicKeyString)

        client2PublicKeyString = keySerialization.serializePublicKey(
            client2.publicKey)
        baseGroupPublicKeys.append(client2PublicKeyString)

        client3PublicKeyString = keySerialization.serializePublicKey(
            client3.publicKey)
        baseGroupPublicKeys.append(client3PublicKeyString)

        RoleDict = {}

        RoleDict[client1PublicKeyString] = "SuperMemberRole"

        RoleDict[client2PublicKeyString] = "MemberRole"

        RoleDict[client3PublicKeyString] = "SubMemberRole"





blockChainInitialization.sendTransactionsToBlockchain()