from Packages.Client.TinyWebClient import TinyWebClient
from Packages.FileIO.readLoadClient import readLoadClient
from Packages.Serialization.keySerialization import keySerialization
from Packages.Verification.Signing import Signing
from Packages.Client.ClientSimulator import ClientSimulator

from Packages.Client.ApiConnector import apiConnectorMethods

import time

import json

client0 = TinyWebClient.initializeClient("0")

client1 = TinyWebClient.initializeClient("1")

client2 = TinyWebClient.initializeClient("2")

client3 = TinyWebClient.initializeClient("3")

client4 = TinyWebClient.initializeClient("4")

client5 = TinyWebClient.initializeClient("5")

client1.sendTextMessage(client2, "I am not giving up. She doesnt love you, she is marrying me")



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


    client1.createGroup(publicKeys)




#print("Done sending first messages")

#print(apiConnectorMethods.getSentMessages(client1))

#print("Recieved Messages")

#print(apiConnectorMethods.getReceivedMessages(client2))
