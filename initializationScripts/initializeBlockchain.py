

from hashlib import new
from Packages.Client.TinyWebClient import TinyWebClient

from Packages.Serialization.keySerialization import keySerialization

from Packages.Serialization.Serialization import Serialization

import requests

from Packages.Verification.Signing import Signing

from Structures.PermissionDefinitions import PermissionDefinitions

from Structures.RoleDefinitions import RoleDefinitions

import time



class blockChainInitialization:

    @staticmethod
    def sendInitialTransactionsToBlockchain():
        transactions = []

        daddyClient = TinyWebClient.initializeClient("0")

        numberOfNodes = 2

        readyToSync = True

        if readyToSync:
            peerDefTransaction = blockChainInitialization.initializePeerListForTesting(daddyClient, numberOfNodes)
            for i in range(numberOfNodes):
                blockChainInitialization.sendTransaction(peerDefTransaction, i)

            print("Waiting for blockchains to sync")

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
            client1PublicKeyString = keySerialization.serializePublicKey(client1.publicKey)
            baseGroupPublicKeys.append(client1PublicKeyString)

            client2PublicKeyString = keySerialization.serializePublicKey(client2.publicKey)
            baseGroupPublicKeys.append(client2PublicKeyString)

            client3PublicKeyString = keySerialization.serializePublicKey(client3.publicKey)
            baseGroupPublicKeys.append(client3PublicKeyString)

            client4PublicKeyString = keySerialization.serializePublicKey(client4.publicKey)

            InitialgroupTransaction = blockChainInitialization.createInitialGroupTransaction(baseGroupPublicKeys,daddyClient)

            FledglinggroupTransaction = blockChainInitialization.createFledglingGroupTransaction(client4PublicKeyString,daddyClient)

            #print(groupTransaction)
            #print("---------------------------------------------")
            transactions.append(FledglinggroupTransaction)

            transactions.append(InitialgroupTransaction)

            RoleDict = {}

            RoleDict[client1PublicKeyString] = "SuperMemberRole"

            RoleDict[client2PublicKeyString] = "MemberRole"

            RoleDict[client3PublicKeyString] = "SubMemberRole"

            

            roleAssignmentTransactions = blockChainInitialization.createRoleAssignmentDefTransactions(RoleDict,InitialgroupTransaction["transaction"]["groupId"], daddyClient)
            transactions += roleAssignmentTransactions


            RoleDictFledglingDict = {}
            RoleDictFledglingDict[client1PublicKeyString] = "FledglingCommRole"

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
            privateKey = Signing.PrivateKeyMethods.loadPrivateKeyNode(i)

            #print({"The private key":keySerialization.serializePrivateKey(privateKey)})
            publickey = privateKey.public_key()
            publicKeyList.append(keySerialization.serializePublicKey(publickey))

            #print("For node: " + str(i) + " the public key is: " + keySerialization.serializePublicKey(publickey))
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
    def createRolesDefTransactions(RoleDefinitions, daddyClient):
        transactions = []

        publicKeyString = keySerialization.serializePublicKey(daddyClient.publicKey)

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
        publicKeyString = keySerialization.serializePublicKey(daddyClient.publicKey)
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

        publicKeyString = keySerialization.serializePublicKey(daddyClient.publicKey)

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
        publicKeyString = keySerialization.serializePublicKey(daddyClient.publicKey)
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
        publicKeyString = keySerialization.serializePublicKey(daddyClient.publicKey)
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
        client1PublicKeyString = keySerialization.serializePublicKey(
            client1.publicKey)
        baseGroupPublicKeys.append(client1PublicKeyString)

        client2PublicKeyString = keySerialization.serializePublicKey(
            client2.publicKey)
        baseGroupPublicKeys.append(client2PublicKeyString)

        client3PublicKeyString = keySerialization.serializePublicKey(
            client3.publicKey)
        baseGroupPublicKeys.append(client3PublicKeyString)

        



blockChainInitialization.sendInitialTransactionsToBlockchain()