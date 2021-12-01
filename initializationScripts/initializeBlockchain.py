

from Packages.Client.TinyWebClient import TinyWebClient

from Packages.Serialization.keySerialization import keySerialization

from Packages.Serialization.Serialization import Serialization

import requests

from Packages.Verification.Signing import Signing



class blockChainInitialization:

    @staticmethod
    def sendTransactionsToBlockchain():
        transactions = []

        daddyClient = TinyWebClient.initializeClient("1")

        numberOfNodes = 2

        peerDefTransaction = blockChainInitialization.initializePeerListForTesting(daddyClient, numberOfNodes)

        transactions.append(peerDefTransaction)

        for ts in transactions:
            for i in range(numberOfNodes):
                blockChainInitialization.sendTransaction(ts, i)



    @staticmethod
    def sendTransaction(transactionObject, nodeId):
        url = "http://127.0.0.1:"+ str(5000 + nodeId) +"/Transaction"
        data = Serialization.serializeObjToJson(transactionObject)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)
        if r.status_code == requests.codes.ok:
            print({"response from entire blockchain request": r.text})
        print("sent Transaction")



    @staticmethod   
    def initializePeerListForTesting(daddyClient, numberOfPeers):
        peerList = []
        publicKeyList = []
        idList = []
        for i in range(0, numberOfPeers):
            peerList.append("http://127.0.0.1:" + str(5000 + i) +"/")
            privateKey = Signing.PrivateKeyMethods.loadPrivateKeyNode(i)

            print({"The private key":keySerialization.serializePrivateKey(privateKey)})
            publickey = privateKey.public_key()
            publicKeyList.append(keySerialization.serializePublicKey(publickey))

            print("For node: " + str(i) + " the public key is: " + keySerialization.serializePublicKey(publickey))
            idList.append(i)

        publicKeyString = keySerialization.serializePublicKey(daddyClient.publicKey)

        transaction = {
            "messageType": "PeerList",
            "peers": peerList,
            "publicKeys": publicKeyList,
            "ids": idList,
            "sender": publicKeyString
        }

        hash = Serialization.hashObject(transaction)

        signature = daddyClient.signData(hash)

        data = {
            "signature": signature,
            "transaction": transaction
        }

        
        return data

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