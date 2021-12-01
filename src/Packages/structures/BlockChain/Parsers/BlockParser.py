
from Packages.Serialization.Serialization import Serialization

#getAllUsers
class BlockParser:
    @staticmethod
    def findPeerList(block):
        peersTransaction = None
        for i in range(len(block.transactions)-1, -1, -1):
            tr = block.transactions[i]
            if tr["messageType"] == "PeerList":
                peersTransaction = tr
                break

        return peersTransaction 

    @staticmethod
    def getAllUsers(block):
        users = []
        for tr in block.transactions:
            if tr["messageType"] == "GroupDef" and tr["groupType"] == "People":
                users = users + tr["entities"]
        return users  

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
                break
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

        for i in range(len(block.transactions)-1, -1, -1):
            tr = block.transactions[i]
            if tr["messageType"] == "SMS":
                if PublicKeyString == tr["receiver"]:
                    messages.append(tr)
        return messages    

        