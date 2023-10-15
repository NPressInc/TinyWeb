#from ....RocksDB.RocksDB import Rocks
import json

from .BlockParser import BlockParser


import sys
nodeId = 0
if len(sys.argv) > 2:
    nodeId = int(sys.argv[2])

class BlockchainParser:


    @staticmethod
    def getAllGroups(blockchain):
        allgroups = []
        for i in range(len(blockchain.chain)):
            groupsInBlock = BlockParser.getAllgroups(blockchain.chain[i])
            if len(groupsInBlock) != 0:
                allgroups = allgroups + groupsInBlock

        return allgroups

    @staticmethod
    def getGroupFromGroupId(groupId, blockchain):
        for i in range(len(blockchain.chain)-1, -1, -1):
            group = BlockParser.getGroupFromGroupId(groupId, blockchain.chain[i])
            if group != None:
                return group
        #if nothing found in the blockchain, the peer is just itself
        return None


    @staticmethod
    def getUserRole(sender, groupId, blockchain):
        for i in range(len(blockchain.chain)-1, -1, -1):
            role = BlockParser.getUserRole(sender, groupId, blockchain.chain[i])
            if role != None:
                return role
        #if nothing found in the blockchain, the peer is just itself
        return None

    @staticmethod
    def getPermissionsFromRole(roleName, blockchain):
        for i in range(len(blockchain.chain)-1, -1, -1):
            permissions = BlockParser.getPermissionsFromRole(roleName, blockchain.chain[i])
            if permissions != None:
                return permissions
        #if nothing found in the blockchain, the peer is just itself
        return None

    @staticmethod
    def printAllPermissionDescriptors(blockchain):
        for i in range(len(blockchain.chain)-1, -1, -1):
            BlockParser.printAllPermissionDescriptors(blockchain.chain[i])

    


    @staticmethod
    def getMostRecentPeerList(blockchain):
        for i in range(len(blockchain.chain)-1, -1, -1):
            peerlist = BlockParser.findPeerList(blockchain.chain[i])
            if peerlist != None:
                return peerlist
        #if nothing found in the blockchain, the peer is just itself
        return None

    @staticmethod
    def printAllMessages(blockchain):
        print("About to print all messages")
        for i in range(len(blockchain.chain)):
            BlockParser.printAllMessages(blockchain.chain[i])


    @staticmethod
    def getAllUsers(blockchain):
        allUsers = []
        for i in range(len(blockchain.chain)):
            usersInBlock = BlockParser.getAllUsers(blockchain.chain[i])
            if len(usersInBlock) != 0:
                allUsers = allUsers + usersInBlock

        genesisBlock = blockchain.chain[0]
        for transaction in genesisBlock.transactions:
            if transaction["messageType"] == "CreatorAssignment":
                allUsers.append(transaction["sender"])
                
        return list(set(allUsers))

    @staticmethod
    def getCreator(blockchain):
        genesisBlock = blockchain.chain[0]
        for transaction in genesisBlock.transactions:
            if transaction["messageType"] == "CreatorAssignment":
                return transaction["sender"]
        return None

    @staticmethod
    def getFledglingPermissions(user ,blockchain):
        allPermissions = []
        for i in range(len(blockchain.chain)):
            permissionsInBlock = BlockParser.getFledglingPermissions(user,blockchain.chain[i])
            if len(permissionsInBlock) != 0:
                allPermissions = allPermissions + permissionsInBlock
        return allPermissions

        

    @staticmethod
    def getGroupByHash(blockchain, hash):
        #outputGroup = outputGroups = Rocks.getGroupFromGroupHash(hash)
        #if outputGroup != None:
            #return outputGroup

        outputGroup = {}

        for block in blockchain.chain:
            group = BlockParser.findGroupFromGroupHash(block, hash)

        #Rocks.setGroupsFromPublicKey(hash, json.dumps(group))
        return outputGroup

    @staticmethod
    def getGroupsByPublicKey(blockchain, publicKeyString):
        #outputGroups = Rocks.getGroupsFromPublicKey(publicKeyString)
        #if outputGroups != None:
            #return outputGroups

        outputGroups = []

        for block in blockchain.chain:
            groups = BlockParser.findGroupsFromPublicKey(
                block, publicKeyString)
            if len(groups) > 0:
                for group in groups:
                    outputGroups.append(group)

        #Rocks.setGroupsFromPublicKey(publicKeyString, json.dumps(outputGroups))
        return outputGroups

    @staticmethod
    def getallMessagesFromPublicKey(blockchain, publicKeyString):
        
        #outputGroups = Rocks.getGroupsFromPublicKey(publicKeyString)
        #if outputGroups != None:
            #return outputGroups

        outputGroups = []

        for block in blockchain.chain:
            groups = BlockParser.findGroupsFromPublicKey(
                block, publicKeyString)
            if len(groups) > 0:
                for group in groups:
                    outputGroups.append(group)

        #Rocks.setGroupsFromPublicKey(publicKeyString, json.dumps(outputGroups))
        return outputGroups

    @staticmethod
    def getRecievedMessagesFromPublicKey(blockchain, publicKeyString):
        #outputMessages = Rocks.getRecievedMessagesFromPublicKey(publicKeyString)
        # if outputMessages != None:
        # return outputMessages

        outputMessages = []

        for block in blockchain.chain:
            groups = BlockParser.findReceivedMessagesFromPublicKey(
                block, publicKeyString)
            if len(groups) > 0:
                for group in groups:
                    outputMessages.append(group)

        #Rocks.setRecievedMessagesFromPublicKey(
            #publicKeyString, json.dumps(outputMessages))
        return outputMessages

    @staticmethod
    def getSentMessagesFromPublicKey(blockchain, publicKeyString):
        #outputMessages = Rocks.getSentMessagesFromPublicKey(publicKeyString)
        # if outputMessages != None:
        # return outputMessages

        outputMessages = []

        for block in blockchain.chain:
            groups = BlockParser.findSentMessagesFromPublicKey(
                block, publicKeyString)
            if len(groups) > 0:
                for group in groups:
                    outputMessages.append(group)

        #Rocks.setSentMessagesFromPublicKey(
            #publicKeyString, json.dumps(outputMessages))
        return outputMessages
    

