from os import stat, terminal_size
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


from ..structures.BlockChain.Parsers.BlockchainParser import BlockchainParser

from ..Verification.PermissionsEditor import PermissionsEditor



class BlockVerification:

    roleHeirarchy = {"SubMemberRole": 0, "MemberRole": 1, "SuperMemberRole": 2, "MegaAdminRole": 3}

    @staticmethod
    def VerifyBlock(block, node):
        validTransactions = []

        for tr in block.transactions:
            if BlockVerification.VerifyTransaction(tr, node):
                validTransactions.append(tr)
            else:
                return False
        
        return True

    @staticmethod
    def RemoveInvalidTransactionsFromBlock(block, node):
        validTransactions = []

        for tr in block.transactions:
            if BlockVerification.VerifyTransaction(tr, node):
                validTransactions.append(tr)
        
        block.transactions = validTransactions
        
        return block

    @staticmethod
    def VerifyTransaction(transaction, node):

        if node != None:
            blockChain = node.blockChain

        myPublicKey = node.publicKey
        
        creator = BlockchainParser.getCreator(blockChain)

        #print({"creator": creator})

        #print({"sender": transaction["sender"]})

        if transaction["sender"] == creator:
            return True

        allPeers = BlockchainParser.getMostRecentPeerList(blockChain)

        if allPeers != None and transaction["sender"] in allPeers["publicKeys"]:
            if transaction["messageType"] == "PermissionDescriptor":
                return True

        elif transaction["sender"] == myPublicKey:
            return True


        


        
        """
        if transaction["messageType"] == "PeerList":
            if not "AddPeer" in permissions:
                return False
            return True
        """
        

        if transaction["messageType"] == "SMS":

            print("--------------------------------")

            print({"transaction": transaction})

            print({"groupId": transaction["groupId"]})
            userRole = BlockchainParser.getUserRole(transaction["sender"],transaction["groupId"], blockChain)
            print({"userRole":userRole})
            permissions = []

            if userRole != None:
                permissions = BlockchainParser.getPermissionsFromRole(userRole, blockChain)
            print({"permissions":permissions})

            group = BlockchainParser.getGroupFromGroupId(transaction["groupId"], blockChain)
            print({"group":group})
        
            if transaction["groupId"] == "fledgling":
                if userRole == None: #fledgelings dont have roles, only certain permissions so this checks if this is a fledgeling sender or a grouped sender

                    permissions = BlockchainParser.getFledglingPermissions(transaction["sender"], blockChain)

                    for p in permissions:
                        if p["type"] == "SMS" and p["scope"] == transaction["receiver"]:
                            return True
                    return False # this triggers if no permissions matched the receiver of the message
                
                else:
                    if not "SendMessagesToFledgling" in permissions:
                        return False #user doesnt have permission to send to fledgelings

                    if node != None:
                        from threading import Thread
                        Thread(target=PermissionsEditor.addSendPermissionToFledgling, args=(transaction["receiver"], transaction["sender"], transaction["messageType"], node)).start()
                    return True


                

            else:
                if not transaction["sender"] in group["entities"]:
                    return False #user used a group id for a group that he is not apart of

                if not transaction["receiver"] in group["entities"]:
                    return False # recipient was not in the group
                
                if "SendMessagesToGroup" in permissions:
                    return True
                
                receiverRole = BlockchainParser.getUserRole(transaction["sender"],transaction["groupId"])
                if "SendMessagesToSuper" in permissions and BlockVerification.roleHeirarchy[receiverRole] > 1:
                    return True # they had the send Super permission and the recipient was either Super or Mega Member

                return False #they did not have group send permission and if they did have toSuper sending ability, the recipient did not qualify

    
        return False

    def addressHasPermissionToContact(pubKey, Action, RecievingParty):
        print("TBI")

    def addressHasPermissionToSeeFile(pubKey, Action, FileHash):
        print("TBI")

    def addressHasPermissionToVote(pubKey, Action, electionId):
        print("TBI")

    def addressHasPermissionToProposeVote(pubKey, Action):
        print("TBI")

    def addressHasPermissionToCreateGroup(pubKey, Action):
        print("TBI")

    def addressHasPermissionToModifyGroup(pubKey, Action):
        print("TBI")

    def addressHasPermissionToModifyRole(pubKey, Action):
        print("TBI")

    def addressHasPermissionToCreateRole(pubKey, Action):
        print("TBI")

    def addressHasPermissionToCreateRole(pubKey, Action):
        print("TBI")
        
    def getPermissionsFromRole(roleName):
        print("TBI")

    


    