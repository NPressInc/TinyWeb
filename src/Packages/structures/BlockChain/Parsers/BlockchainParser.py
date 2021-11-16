from ....RocksDB.RocksDB import Rocks
import json

from .BlockParser import BlockParser

class BlockchainParser:

    @staticmethod
    def getMostRecentPeerList(blockchain):
        for i in range(len(blockchain.chain)-1, -1, -1):
            peerlist = BlockParser.findPeerList(blockchain.chain[i])
            if peerlist != None:
                return peerlist['peers']
        return None

    @staticmethod
    def getGroupByHash(blockchain, hash):
        outputGroup = outputGroups = Rocks.getGroupFromGroupHash(hash)
        if outputGroup != None:
            return outputGroup

        outputGroup = {}

        for block in blockchain.chain:
            group = BlockParser.findGroupFromGroupHash(block, hash)

        Rocks.setGroupsFromPublicKey(hash, json.dumps(group))
        return outputGroups

    @staticmethod
    def getGroupsByPublicKey(blockchain, publicKeyString):
        outputGroups = Rocks.getGroupsFromPublicKey(publicKeyString)
        if outputGroups != None:
            return outputGroups

        outputGroups = []

        for block in blockchain.chain:
            groups = BlockParser.findGroupsFromPublicKey(
                block, publicKeyString)
            if len(groups) > 0:
                for group in groups:
                    outputGroups.append(group)

        Rocks.setGroupsFromPublicKey(publicKeyString, json.dumps(outputGroups))
        return outputGroups

    @staticmethod
    def getallMessagesFromPublicKey(blockchain, publicKeyString):
        print("TBI")
        return None
        outputGroups = Rocks.getGroupsFromPublicKey(publicKeyString)
        if outputGroups != None:
            return outputGroups

        outputGroups = []

        for block in blockchain.chain:
            groups = BlockParser.findGroupsFromPublicKey(
                block, publicKeyString)
            if len(groups) > 0:
                for group in groups:
                    outputGroups.append(group)

        Rocks.setGroupsFromPublicKey(publicKeyString, json.dumps(outputGroups))
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

        Rocks.setRecievedMessagesFromPublicKey(
            publicKeyString, json.dumps(outputMessages))
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

        Rocks.setSentMessagesFromPublicKey(
            publicKeyString, json.dumps(outputMessages))
        return outputMessages
