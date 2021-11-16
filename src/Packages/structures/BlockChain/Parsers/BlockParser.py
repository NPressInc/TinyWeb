
from Packages.Serialization.Serialization import Serialization


class BlockParser:
    @staticmethod
    def findPeerList(block):
        peersTransaction = None
        for tr in block.transactions:
            if tr["messageType"] == "PeerList":
                peersTransaction = tr

        return peersTransaction 

    @staticmethod
    def findGroupsFromPublicKey(block, PublicKeyString):
        groups = []

        for tr in block.transactions:
            if tr["messageType"] == "GroupDef":
                if PublicKeyString in tr["entities"]:
                    groups.append(tr)
        return groups       
        
    @staticmethod
    def findGroupFromGroupHash(block, groupHash):
        group = None
        for tr in block.transactions:
            if groupHash == Serialization.hashObject(tr):
                group = tr
        return group   

    @staticmethod
    def findSentMessagesFromPublicKey(block, PublicKeyString):

        messages = []

        for tr in block.transactions:
            if tr["messageType"] == "SMS":
                if PublicKeyString == tr["sender"]:
                    messages.append(tr)
        return messages   

    @staticmethod
    def findReceivedMessagesFromPublicKey(block, PublicKeyString):

        messages = []

        for tr in block.transactions:
            if tr["messageType"] == "SMS":
                if PublicKeyString == tr["receiver"]:
                    messages.append(tr)
        return messages    

        