

from hashlib import new
from Packages.Client.TinyWebClient import TinyWebClient

from Packages.Serialization.Serialization import Serialization

import requests

from Packages.Verification.PrivateKeyMethods import PrivateKeyMethods

from Structures.PermissionDefinitions import PermissionDefinitions

from Structures.RoleDefinitions import RoleDefinitions

class blockChainInitialization:

    @staticmethod
    def sendInitialTransactionsToBlockchain():
        transactions = []

        daddyClient = TinyWebClient.initializeClient("0")

        numberOfNodes = 2

        readyToSync = True  # This is a manual type of switch that I use to initialize blockchains. First Set to false to create groups on one node. Then sync nodes afterwards by setting to True
        #must start the starter node before the second node
        if readyToSync:
            peerDefTransaction = blockChainInitialization.initializePeerListForTesting(daddyClient, numberOfNodes)
            for i in range(numberOfNodes):
                blockChainInitialization.sendTransaction(peerDefTransaction, i)


        else:
            PermissionDefTransactions = blockChainInitialization.createPermissionsTransactions(PermissionDefinitions, daddyClient)

            #print(PermissionDefTransactions)
            #print("---------------------------------------------")

            transactions += PermissionDefTransactions

            RoleDefinitionsTransactions = blockChainInitialization.createRolesDefTransactions(RoleDefinitions, daddyClient)

            #print(RoleDefinitionsTransactions)
            #print("---------------------------------------------")

            transactions += RoleDefinitionsTransactions

            client1 = TinyWebClient.initializeClient("1")
            client2 = TinyWebClient.initializeClient("2")
            client3 = TinyWebClient.initializeClient("3")
            client4 = TinyWebClient.initializeClient("4")

            baseGroupPublicKeys = []
            client1PublicKeyBytes = client1.publicKey.encode()
            baseGroupPublicKeys.append(client1PublicKeyBytes)

            client2PublicKeyBytes = client2.publicKey.encode()
            baseGroupPublicKeys.append(client2PublicKeyBytes)

            client3PublicKeyBytes = client3.publicKey.encode()
            baseGroupPublicKeys.append(client3PublicKeyBytes)

            client4PublicKeyBytes = client4.publicKey.encode()

            InitialgroupTransaction = blockChainInitialization.createInitialGroupTransaction(baseGroupPublicKeys,daddyClient)

            FledglinggroupTransaction = blockChainInitialization.createFledglingGroupTransaction(client4PublicKeyBytes,daddyClient)

            #print(groupTransaction)
            print("---------------------------------------------")
            transactions.append(FledglinggroupTransaction)

            transactions.append(InitialgroupTransaction)

            RoleDict = {}

            RoleDict[client1PublicKeyBytes] = "SuperMemberRole"

            RoleDict[client2PublicKeyBytes] = "MemberRole"

            RoleDict[client3PublicKeyBytes] = "SubMemberRole"

            

            roleAssignmentTransactions = blockChainInitialization.createRoleAssignmentDefTransactions(RoleDict,InitialgroupTransaction["transaction"]["groupId"], daddyClient)
            transactions += roleAssignmentTransactions


            RoleDictFledglingDict = {}
            RoleDictFledglingDict[client1PublicKeyBytes] = "FledglingCommRole"

            roleAssignmentTransactions = blockChainInitialization.createRoleAssignmentDefTransactions(RoleDictFledglingDict,"fledgling", daddyClient)

            transactions += roleAssignmentTransactions

            #print(roleAssignmentTransactions)

            

            #print("---------------------------------------------")

            #print(transactions)


            

            #print(peerDefTransaction)
            #print("---------------------------------------------")

            


            for ts in transactions:
                blockChainInitialization.sendTransaction(ts, 0)

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
            privateKey = PrivateKeyMethods.loadPrivateKeyNode(i)

            publickey = PrivateKeyMethods.generatePublicKeyFromPrivate(privateKey)
            publicKeyList.append(publickey.encode())

            #print("For node: " + str(i) + " the public key is: " + publickey.encode())
            idList.append(i)

        publicKeyString = daddyClient.publicKey.encode()

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
    def createRolesDefTransactions(RoleDefinitions, daddyClient):
        transactions = []

        publicKeyString = daddyClient.publicKey.encode()

        for RoleDef in RoleDefinitions:
            newRole = {
                "messageType": "RoleDescriptor",
                "name": RoleDef["name"],
                "sender": publicKeyString,
                "permissionNames": RoleDef["permissions"]
            }

            hash = Serialization.hashObject(newRole)

            signature = daddyClient.signData(hash)

            transactions.append({"signature": signature, "transaction": newRole})

        return transactions

    @staticmethod
    def createRoleAssignmentDefTransactions(RoleDict, groupId, daddyClient):
        transactions = []
        publicKeyString = daddyClient.publicKey.encode()
        for key in RoleDict:
            roleAssignment = {
                "messageType": "RoleAssignment",
                "user": key,
                "roleName": RoleDict[key],
                "groupId": groupId,
                "sender": publicKeyString
            }
            hash = Serialization.hashObject(roleAssignment)

            signature = daddyClient.signData(hash)

            transactions.append({"signature": signature, "transaction": roleAssignment})
        return transactions

    @staticmethod
    def createPermissionsTransactions(PermissionDefinitions, daddyClient):

        transactions = []

        publicKeyString = daddyClient.publicKey.encode()

        for Permission in PermissionDefinitions:
            newPermission = {
                "messageType": "PermissionDescriptor",
                "name": Permission["name"],
                "type": Permission["type"],
                "scope": Permission["scope"],
                "sender": publicKeyString
            }
            hash = Serialization.hashObject(newPermission)

            signature = daddyClient.signData(hash)

            transactions.append({"signature": signature, "transaction": newPermission})


        return transactions


    @staticmethod
    def createInitialGroupTransaction(initialGroupMemebers, daddyClient):
        import time
        #groupId = Serialization.hashString(initialGroupMemebers[0] + str(time.time())) #random string to be groupID. Realized that I cant identify via hash becuase groups can change.
        groupId = "number1"
        publicKeyString = daddyClient.publicKey.encode()
        groupDef = {
                "messageType": "GroupDescriptor",
                "sender": publicKeyString,
                "groupType": "People",
                "entities": initialGroupMemebers,
                "description": "Initial Group",
                "groupId": groupId
            }
        hash = Serialization.hashObject(groupDef)

        signature = daddyClient.signData(hash)

        return {"signature": signature, "transaction": groupDef}


    @staticmethod
    def createFledglingGroupTransaction(fledglingClient, daddyClient):
        import time
        groupId = "fledgling"
        publicKeyString = daddyClient.publicKey.encode()
        groupDef = {
                "messageType": "GroupDescriptor",
                "sender": publicKeyString,
                "groupType": "People",
                "entities": [fledglingClient],
                "description": "OutsidersGroup",
                "groupId": groupId
            }
        hash = Serialization.hashObject(groupDef)

        signature = daddyClient.signData(hash)

        return {"signature": signature, "transaction": groupDef}



    @staticmethod
    def testCreateClients():
        client1 = TinyWebClient.initializeClient("1")
        client2 = TinyWebClient.initializeClient("2")
        client3 = TinyWebClient.initializeClient("3")

        baseGroupPublicKeys = []
        client1PublicKeyString = client1.publicKey.encode()
        baseGroupPublicKeys.append(client1PublicKeyString)

        client2PublicKeyString = client2.publicKey.encode()
        baseGroupPublicKeys.append(client2PublicKeyString)

        client3PublicKeyString = client3.publicKey.encode()
        baseGroupPublicKeys.append(client3PublicKeyString)

        



blockChainInitialization.sendInitialTransactionsToBlockchain()