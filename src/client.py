from Packages.Client.TinyWebClient import TinyWebClient
from Packages.FileIO.readLoadClient import readLoadClient
from Packages.Serialization.keySerialization import keySerialization
from Packages.Verification.Signing import Signing
from Packages.Client.ClientSimulator import ClientSimulator

from Packages.Client.ApiConnector import apiConnectorMethods

from Packages.structures.BlockChain.Parsers.BlockchainParser import BlockchainParser

from Packages.Encryption.Encryption import Encryption

import time

import sys

import json

client0 = TinyWebClient.initializeClient("0")

client1 = TinyWebClient.initializeClient("1")

client2 = TinyWebClient.initializeClient("2")

client3 = TinyWebClient.initializeClient("3")

client4 = TinyWebClient.initializeClient("4")

client5 = TinyWebClient.initializeClient("5")


print(client1.sendTextMessage(client2, "I am not giving up. She doesnt love you, she is marrying me"))

print(client2.sendTextMessage(client3, "Angela Bernard"))

print(client3.sendTextMessage(client4, "Will never be her name"))

print(client4.sendTextMessage(client1, "Yes it will"))

print(client1.sendTextMessage(client4, "Fight me"))

time.sleep(15)

print(client4.sendTextMessage(client1, "Fighting is not allowed in the office"))


def testMultiEncrypt():

    clientsWithAccess = [
        keySerialization.serializePublicKey(client2.publicKey),
        keySerialization.serializePublicKey(client3.publicKey),
        keySerialization.serializePublicKey(client4.publicKey),
        keySerialization.serializePublicKey(client1.publicKey),
    ]


    encryptedData = client1.encryptDataForMultiplePublicKeys(clientsWithAccess, b"Hello")
    print(encryptedData)

    decryptedData = client1.dencryptDataFromMultiEncryptedData(keySerialization.serializePublicKey(client1.publicKey),encryptedData["EncryptedKeys"], encryptedData["EncryptedData"])


    print( decryptedData.decode("utf-8") )

    decryptedData = client2.dencryptDataFromMultiEncryptedData(keySerialization.serializePublicKey(client1.publicKey),encryptedData["EncryptedKeys"], encryptedData["EncryptedData"])


    print( decryptedData.decode("utf-8") )

    decryptedData = client3.dencryptDataFromMultiEncryptedData(keySerialization.serializePublicKey(client1.publicKey),encryptedData["EncryptedKeys"], encryptedData["EncryptedData"])


    print( decryptedData.decode("utf-8") )

    decryptedData = client4.dencryptDataFromMultiEncryptedData(keySerialization.serializePublicKey(client1.publicKey),encryptedData["EncryptedKeys"], encryptedData["EncryptedData"])

    print( decryptedData.decode("utf-8") )

    decryptedData = client5.dencryptDataFromMultiEncryptedData(keySerialization.serializePublicKey(client1.publicKey),encryptedData["EncryptedKeys"], encryptedData["EncryptedData"])

    print( decryptedData.decode("utf-8") )



    sys.exit()



def creatGroup():
    serializedPublicKey1 = keySerialization.serializePublicKey(client1.publicKey)
    serializedPublicKey2 = keySerialization.serializePublicKey(client2.publicKey)
    serializedPublicKey3 = keySerialization.serializePublicKey(client3.publicKey)
    serializedPublicKey4 = keySerialization.serializePublicKey(client4.publicKey)

    publicKeys = []

    publicKeys.append(serializedPublicKey1)
    publicKeys.append(serializedPublicKey2)
    publicKeys.append(serializedPublicKey3)
    publicKeys.append(serializedPublicKey4)

    for key in publicKeys:
        print(key)


    client1.createGroup(publicKeys, "testGroup1")




#print("Done sending first messages")

#print(apiConnectorMethods.getSentMessages(client1))

#print("Recieved Messages")

#print(apiConnectorMethods.getReceivedMessages(client2))
