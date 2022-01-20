
import json

from Packages.Client.ApiConnector import apiConnectorMethods

from Packages.Serialization.Serialization import Serialization
from ..Verification.Signing import Signing

from ..Serialization.keySerialization import keySerialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from Packages.Serialization.Serialization import Serialization
from Packages.Serialization.keySerialization import keySerialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

import base64

import time

import sys
nodeId = 0
if len(sys.argv) > 2:
    nodeId = int(sys.argv[2])

class TinyWebClient:
    def __init__(self, privateKey = None, publicKey = None,clientId = None ,LocationOn=None):
        self.__privateKey = privateKey
        self.publicKey = publicKey
        self.clientId = clientId
        self.LocationOn = LocationOn
    

    def signData(self, data):
        return Signing.normalSigning(self.__privateKey, data)

    def sendTextMessage(self, recipient, message):
        senderPublicKeyString = keySerialization.serializePublicKey(self.publicKey)
        recipientKeyString = keySerialization.serializePublicKey(recipient.publicKey)
        groupId = ""
        if recipient.clientId == "4" or self.clientId == "4":
            
            groupId = "fledgling"
        else:
            groupId = "number1"
            


        transaction = {"messageType": "SMS","sender": senderPublicKeyString, "receiver":recipientKeyString, "context":message,"groupId":groupId, "dateTime": time.time()}

        signature = Signing.normalSigning(self.__privateKey, Serialization.hashObject(transaction))

        TinyWebClient.sendTransaction({"transaction":transaction, "signature": signature})


    def sendTestMessages(self, recipient):
        message1 = "Lets Rage"
        message2 = "No, lets age"

        senderPublicKeyString = keySerialization.serializePublicKey(self.publicKey)
        recipientKeyString = keySerialization.serializePublicKey(recipient.publicKey)

        FauxTransactionList = []

        for i in range(0,1000):
            transaction1 = {"messageType": "SMS","sender": senderPublicKeyString, "receiver":recipientKeyString, "context":message1, "dateTime": time.time() + i}
            transaction2 = {"messageType": "SMS","sender": senderPublicKeyString, "receiver":recipientKeyString, "context":message2, "dateTime": time.time() + i}
            signature1 = Signing.normalSigning(self.__privateKey, Serialization.hashObject(transaction1))
            signature2 = Signing.normalSigning(self.__privateKey, Serialization.hashObject(transaction2))
            FauxTransactionList.append({"transaction":transaction1,"signature": signature1})
            FauxTransactionList.append({"transaction":transaction2, "signature": signature2})
            
        
        counter = 0
        numberOfMessages = 200
        secondsBetweenMessages = 0.5

        while counter < numberOfMessages:
            counter += 1
            index = counter % (len(FauxTransactionList) - 1)
            time.sleep(secondsBetweenMessages)
            TinyWebClient.sendTransaction(FauxTransactionList[index])

    @staticmethod
    def sendTransaction(transactionObject):
        import requests
        print("about to send transaction")
        url = "http://127.0.0.1:"+ str(5000 + nodeId) +"/Transaction"
        data = Serialization.serializeObjToJson(transactionObject)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data, headers=headers)
        if r.status_code == requests.codes.ok:
            data = Serialization.deserializeObjFromJsonR(r.text)
            print(data)

        print("sent Transaction")

    @staticmethod
    def initializeClient(clientId):
        client = None
        try:
            __privateKey = Signing.PrivateKeyMethods.loadPrivateKeyClient(clientId)
            client = TinyWebClient(privateKey=__privateKey, publicKey=Signing.PrivateKeyMethods.generatePublicKeyFromPrivate(__privateKey), clientId=clientId,LocationOn= True)
            print("Loaded Client: " + clientId)
        except:
            client = TinyWebClient.initializeNewClient(clientId)
            Signing.PrivateKeyMethods.savePrivateKeyClient(client.__privateKey, clientId)
            print("Created New Client: " + clientId)

        return client
        

    @staticmethod
    def initializeNewClient(clientId):
        client = TinyWebClient()
        client.__privateKey = Signing.PrivateKeyMethods.generatePrivateKey()
        client.publicKey = Signing.PrivateKeyMethods.generatePublicKeyFromPrivate(client.__privateKey)
        client.LocationOn = True
        client.clientId = clientId

        return client


    def seriralizeJSON(self):
        outputObject = {
            "_privateKey": keySerialization.serializePrivateKey(self.__privateKey),
            "publicKey": keySerialization.serializePublicKey(self.publicKey),
            "LocationOn": self.LocationOn,
            "clientId": self.clientId
        }
        return json.dumps(outputObject, sort_keys=True)


    @staticmethod
    def deseriralizeJSON(jsonString):
        jsonDict = json.loads(jsonString)
        return TinyWebClient(**jsonDict)




    def createGroup(self, groupMembers, groupDesctiption):
        groupId = Serialization.hashString(groupMembers[0] + str(time.time())) #random string to be groupID. Realized that I cant identify via hash becuase groups can change.
        groupDef = {
                "messageType": "GroupDescriptor",
                "sender": keySerialization.serializePublicKey(self.publicKey),
                "groupType": "People",
                "entities": groupMembers,
                "description": groupDesctiption,
                "groupId": groupId
            }
        groupHash = Serialization.hashObject(groupDef)

        signature = Signing.normalSigning(self.__privateKey, groupHash)

        data = {
            "transaction":groupDef,
            "signature":signature
        }

        apiConnectorMethods.sendTransaction(data)

    def encryptDataForMultiplePublicKeys(self, recipientPublicKeyStrings, data):

        encryptedKeys = []

        generatedKey = Fernet.generate_key()

        f = Fernet(generatedKey)

        encryptedData  = f.encrypt(data)
        

        for recipientPublicKeyString in recipientPublicKeyStrings:

            recipientPublicKey = keySerialization.deserializePublicKey(recipientPublicKeyString)
            shared_key = self.__privateKey.exchange(
                ec.ECDH(), recipientPublicKey)
            # Perform key derivation.
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'handshake data',
            ).derive(shared_key)

            password = derived_key
            salt = None
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b"randomSalt",
                iterations=390000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))

            f2 = Fernet(key)
            
            encryptedKeys.append(f2.encrypt(generatedKey))

        
        return {"EncryptedData": encryptedData, "EncryptedKeys": encryptedKeys}


    def dencryptDataFromMultiEncryptedData(self, senderPublicKeyString, encryptedKeys,data):

        senderPublicKey = keySerialization.deserializePublicKey(senderPublicKeyString)
        shared_key = self.__privateKey.exchange(
            ec.ECDH(), senderPublicKey)
        # Perform key derivation.
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)

        password = derived_key
        salt = None
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"randomSalt",
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        f = Fernet(key)

        decryptedKey = None

        for encKey in encryptedKeys:
            try:
                decryptedKey = f.decrypt(encKey)
                break
            except:
                continue

        if decryptedKey == None:
            raise Exception("No Encrypted Keys Matched. No access given")

        f2 = Fernet(decryptedKey)

        return f2.decrypt(data)



    def encryptDataForPublicKey(self, recipientPublicKeyString, data):

        recipientPublicKey = keySerialization.deserializePublicKey(recipientPublicKeyString)

        shared_key = self.__privateKey.exchange(
            ec.ECDH(), recipientPublicKey)
        # Perform key derivation.
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)

        print(type(derived_key))
        print(derived_key)


        password = derived_key
        salt = None
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"randomSalt",
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        f = Fernet(key)

        return f.encrypt(data)



    def decryptdata(self, SenderPublicKeyString, data):

        SenderPublicKey = keySerialization.deserializePublicKey(SenderPublicKeyString)

        same_shared_key = self.__privateKey.exchange(
            ec.ECDH(), SenderPublicKey)
        # Perform key derivation.
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(same_shared_key)

        print(type(derived_key))
        print(derived_key)

        password = derived_key
        salt = None
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"randomSalt",
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        try:
            f = Fernet(key)

            return f.decrypt(data)

        except:
            print("Invalid Key")

        


    def getPeers(self):
        print("TBI")
    
    def sendGroupMessage(self, RecievingGroup, Message):
        print("TBI")

    def broadcastGPSLocation(self, Location):
        print("TBI")

    def sendVoiceCallRequest(self, Receiver):
        print("TBI")

    def pollForUpdates(self):
        print("TBI")

    def sendGroupMessage(self, RecievingGroup, Message):
        print("TBI")



