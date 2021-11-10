
import json
from ..Verification.Signing import Signing

class TinyWebClient:
    def __init__(self, privateKey = None, publicKey = None,clientId = None ,LocationOn=None):
        self._privateKey = privateKey
        self.publicKey = publicKey
        self.clientId = clientId
        self.LocationOn = LocationOn

    @staticmethod
    def initializeClient(clientId):
        client = None
        try:
            privateKey = Signing.PrivateKeyMethods.loadPrivateKey(clientId)
            client = TinyWebClient(privateKey=privateKey, publicKey=Signing.PrivateKeyMethods.generatePublicKeyFromPrivate(privateKey), clientId=clientId,LocationOn= True)
            print("Loaded Client: " + clientId)
        except:
            client = TinyWebClient.initializeNewClient(clientId)
            Signing.PrivateKeyMethods.savePrivateKey(client._privateKey, clientId)
            print("Created New Client: " + clientId)

        return client
        

    @staticmethod
    def initializeNewClient(clientId):
        client = TinyWebClient()
        client._privateKey = Signing.PrivateKeyMethods.generatePrivateKey()
        client.publicKey = Signing.PrivateKeyMethods.generatePublicKeyFromPrivate(client._privateKey)
        client.LocationOn = True
        client.clientId = clientId

        return client


    def seriralizeJSON(self):
        outputObject = {
            "_privateKey": Signing.PrivateKeyMethods.serializePrivateKey(self._privateKey),
            "publicKey": Signing.PublicKeyMethods.serializePublicKey(self.publicKey),
            "LocationOn": self.LocationOn,
            "clientId": self.clientId
        }
        return json.dumps(outputObject, sort_keys=True)

    @staticmethod
    def deseriralizeJSON(jsonString):
        jsonDict = json.loads(jsonString)
        return TinyWebClient(**jsonDict)

    def getPeers(self):
        print("TBI")

    def sendTextMessage(self, Reciever, Message):
        print("TBI")
    
    def sendGroupMessage(self, RecievingGroup, Message):
        print("TBI")

    def broadcastGPSLocation(self, Location):
        print("TBI")

    def sendVoiceCallRequest(self, Reciever):
        print("TBI")

    def pollForUpdates(self):
        print("TBI")

    def sendGroupMessage(self, RecievingGroup, Message):
        print("TBI")



