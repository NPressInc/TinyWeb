
import time
import brotli

from Packages.Serialization.Serialization import Serialization
from Packages.Serialization.keySerialization import keySerialization
from Packages.structures.BlockChain.Parsers.BlockchainParser import BlockchainParser
from ..structures.BlockChain.BlockChain import BlockChain
from ..structures.BlockChain.Block import Block
from ..Verification.BlockVerification import BlockVerification
from ..FileIO.readLoadBlockChain import BlockChainReadWrite
from ..Client.TinyWebClient import TinyWebClient
from ..Verification.Signing import Signing


import sys
nodeId = 0
if len(sys.argv) > 2:
    nodeId = int(sys.argv[2])


class PBFTNode:
    node = None
    @staticmethod
    def runNode():
        blockChain = BlockChainReadWrite.readBlockChainFromFile()

        if blockChain == None:
            blockChain = PBFTNode.configureBlockChainForFirstUse()

        

        counter = 0

        print({"last Block Index": blockChain.last_block().index})

        node = PBFTNode(nodeId, blockChain)

        PBFTNode.node = node


        #BlockChainReadWrite.saveBlockChainToFile(node.blockChain)


        while counter < 1000:

            if counter % 10 == 0:
                #BlockChainReadWrite.saveBlockChainToFile(node.blockChain)
                newPeerList = BlockchainParser.getMostRecentPeerList(node.blockChain)
                if newPeerList != None:
                    newPeers = []
                    for peer in newPeerList:
                        if not(peer in node.peers):
                            if peer != "http://127.0.0.1:" + str(5000 + nodeId) +"/": # make sure that the new peer is not itself
                                newPeers.append(peer)

                    print({"newPeers": newPeers})
                    if len(newPeers) != 0:  
                        node.peers = node.peers + newPeers
                        for peer in newPeers:
                            node.broadcastBlockChainToNewNode(peer)
                    else:
                        print("peers havent Changed")

            time.sleep(1)
            counter += 1
            


            #Validating the proposed block, wether it was the block that we proposed or someone else
            
            

            #Wait for the commit votes to come in

           

    def __init__(self, id, blockChain):
        self.__privateKey = None
        self.publicKey = None

        self.id = id  # id represents the order in which nodes act as the proposer

        self.peers = []

        self.ProposerId = 0

        self.blockChain = blockChain

        self.phase = 0

        self.initializeKeys()

    def initializeKeys(self):
        client = None
        try:
            privateKey = Signing.PrivateKeyMethods.loadPrivateKeyNode(self.id)
            self.publicKey=Signing.PrivateKeyMethods.generatePublicKeyFromPrivate(privateKey)
            print("Loaded Client: " + self.id)
        except:
            self.__privateKey = Signing.PrivateKeyMethods.generatePrivateKey()
            self.publicKey = Signing.PrivateKeyMethods.generatePublicKeyFromPrivate(self.__privateKey)
            Signing.PrivateKeyMethods.savePrivateKeyNode(self.__privateKey, self.id)
            print("Created New Node: " + str(self.id))

        return client
        
    
    def reBroadcastMessage(self, data, route):
        import requests
        for peer in self.peers:
            try:
                url = peer + route
                headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
                r = requests.post(url, data=data, headers=headers)
                print(r.status_code)
            except:
                print("Node not found at: " + peer)
                
        print("Done ReBroadcasting " + route)

    def broadcastBlockToPeers(self, block):
        import requests
        for peer in self.peers:
            try:
                url = peer + "ProposeBlock"
                hash = block.getHash()
                blockString = block.serializeJSON()
                signature = Signing.normalSigning(self.__privateKey, hash)
                data = {
                    "blockData":blockString,
                    "blockHash": hash,
                    "sender": keySerialization.serializePublicKey(self.publicKey),
                    "signature": signature
                }
                data = Serialization.serializeObjToJson(data)
                headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
                
                r = requests.post(url, data= data, headers=headers)
                if r.status_code == requests.codes.ok:

                    data = Serialization.deserializeObjFromJsonR(r.text)

                    return data
                else:
                    return None
            except:
                print("Node not found at: " + peer)
        
        if len(self.peers) == 0:
            url = "http://127.0.0.1:" +str(5000 + nodeId) + "/ProposeBlock"
            hash = block.getHash()
            blockString = block.serializeJSON()
            signature = Signing.normalSigning(self.__privateKey, hash)
            data = {
                "blockData":blockString,
                "blockHash": hash,
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            
            r = requests.post(url, data= data, headers=headers)
            if r.status_code == requests.codes.ok:

                data = Serialization.deserializeObjFromJsonR(r.text)

                return data
            else:
                return None

                
        print("Done Broadcasting new block")


    def broadcastBlockChainToNewNode(self, peer):
        import requests
        import hashlib
        try:
            url = peer + "SendNewBlockChain"
            blockChainString = self.blockChain.serializeJSON()
            hash = hashlib.sha256(blockChainString.encode()).hexdigest()
            signature = Signing.normalSigning(self.__privateKey, hash)
            data = {
                "blockChain":blockChainString,
                "blockChainHash": hash,
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            
            r = requests.post(url, data= data, headers=headers)
            if r.status_code == requests.codes.ok:

                data = Serialization.deserializeObjFromJsonR(r.text)
                

                return data
            else:
                return None
        except:
            print("Node not found at: " + peer)
                
        print("Done Broadcasting new blockchain")


    def broadcastVerificationVotesToPeers(self, blockHash):
        import requests
        for peer in self.peers:
            try:
                url = peer + "VerificationVote"
                signature = Signing.normalSigning(self.__privateKey, blockHash)
                data = {
                    "sender": keySerialization.serializePublicKey(self.publicKey),
                    "signature": signature,
                    "blockHash": blockHash
                }
                data = Serialization.serializeObjToJson(data)
                headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
                r = requests.post(url, data=data, headers=headers)
            except:
                print("Node not found at: " + peer)
        if len(self.peers) == 0:
            url = "http://127.0.0.1:" +str(5000 + nodeId) + "/VerificationVote"
            signature = Signing.normalSigning(self.__privateKey, blockHash)
            data = {
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature,
                "blockHash": blockHash
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            r = requests.post(url, data=data, headers=headers)

    def broadcastCommitVotesToPeers(self, blockHash):
        import requests
        for peer in self.peers:
            try:
                url = peer + "CommitVote"
                signature = Signing.normalSigning(self.__privateKey, blockHash)
                data = {
                    "sender": keySerialization.serializePublicKey(self.publicKey),
                    "signature": signature,
                    "blockHash": blockHash
                }
                data = Serialization.serializeObjToJson(data)
                headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
                r = requests.post(url, data=data, headers=headers)
                print(r.status_code)
            except:
                print("Node not found at: " + peer)
        if len(self.peers) == 0:
            url = "http://127.0.0.1:" +str(5000 + nodeId) + "/CommitVote"
            signature = Signing.normalSigning(self.__privateKey, blockHash)
            data = {
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature,
                "blockHash": blockHash
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            r = requests.post(url, data=data, headers=headers)

    def broadcastNewRoundVotesToPeers(self, blockHash):
        import requests
        for peer in self.peers:
            try:
                url = peer + "NewRound"
                signature = Signing.normalSigning(self.__privateKey, blockHash)
                data = {
                    "sender": keySerialization.serializePublicKey(self.publicKey),
                    "signature": signature,
                    "blockHash": blockHash
                }
                data = Serialization.serializeObjToJson(data)
                headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
                r = requests.post(url, data=data, headers=headers)
                print(r.status_code)
            except:
                print("Node not found at: " + peer)
        if len(self.peers) == 0:
            url = "http://127.0.0.1:" +str(5000 + nodeId) + "/NewRound"
            signature = Signing.normalSigning(self.__privateKey, blockHash)
            data = {
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "signature": signature,
                "blockHash": blockHash
            }
            data = Serialization.serializeObjToJson(data)
            headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
            r = requests.post(url, data=data, headers=headers)
            print(r.status_code)

    def calculateProposerId(self):
        
        NumberOfPeers = len(self.peers)

        if len(self.peers) < 1 or self.blockChain.chain[-1].proposerId == -1:
            return 0

        index = (self.blockChain.chain[-1].proposerId + 1) % (NumberOfPeers + 1)
        return index

    @staticmethod
    def compressJson(input):
        return brotli.compress(input)

    @staticmethod
    def decompressJson(input):
        return brotli.decompress(input)

    @staticmethod
    def configureBlockChainForFirstUse():

        client1 = TinyWebClient.initializeClient("1")
        client1PublicKeyString = keySerialization.serializePublicKey(client1.publicKey)
        blockChain = BlockChain(creatorPublicKey=client1PublicKeyString)

        return blockChain
