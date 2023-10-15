
from os import stat
from Packages.Serialization.Serialization import Serialization
from ....models.messages import TinyMessage

#getAllUsers
class BlockParser:


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
    @staticmethod
    def getGroupFromGroupId(groupId, block):
        for tr in block.transactions:
            if tr["messageType"] == "GroupDescriptor" and tr["groupId"] == groupId:
                return tr
        return None


    @staticmethod
    def getPermissionsFromRole(roleName, block):
        for tr in block.transactions:
            if tr["messageType"] == "RoleDescriptor" and tr["name"] == roleName:
                return tr["permissionNames"]
        return None


    @staticmethod
    def printAllPermissionDescriptors(block):
        for tr in block.transactions:
            if tr["messageType"] == "PermissionDescriptor":
                print({"permission": tr})


    @staticmethod
    def getUserRole(sender, groupId, block):
        for tr in block.transactions:
            if tr["messageType"] == "RoleAssignment" and tr["user"] == sender and tr["groupId"] == groupId:
                return tr["roleName"]
        return None

    @staticmethod
    def printAllMessages(block):
        for tr in block.transactions:
            if tr["messageType"] == "SMS":
                print(tr)
                print("----------------")

    @staticmethod
    def getFledglingPermissions(user,block):
        users = []
        for tr in block.transactions:
            if tr["messageType"] == "PermissionDescriptor" and "user" in tr and tr["user"] == user:
                users.append(tr)
        return users

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
    def getAllgroups(block):
        groups = []
        for tr in block.transactions:
            if tr["messageType"] == "GroupDescriptor" and tr["groupType"] == "People":
                groups.append(tr)
        return groups  
        

    @staticmethod
    def getAllUsers(block):
        users = []
        for tr in block.transactions:
            if tr["messageType"] == "GroupDescriptor" and tr["groupType"] == "People":
                users = users + tr["entities"]
        return users  

    @staticmethod
    def findGroupsFromPublicKey(block, PublicKeyString):
        groups = []

        for tr in block.transactions:
            if tr["messageType"] == "GroupDescriptor":
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
                    parsedMessage = TinyMessage(**tr)
                    messages.append(parsedMessage.toJson())
        return messages    

        