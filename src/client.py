from Packages.Client.TinyWebClient import TinyWebClient
from Packages.FileIO.readLoadClient import readLoadClient
from Packages.Serialization.keySerialization import keySerialization
from Packages.Verification.Signing import Signing

from Packages.Client.ApiConnector import apiConnectorMethods

import time

import json


client1 = TinyWebClient.initializeClient("1")

client2 = TinyWebClient.initializeClient("2")

client3 = TinyWebClient.initializeClient("3")


groups = apiConnectorMethods.getAllGroups(client1)


serializedPublicKey = keySerialization.serializePublicKey(client1.publicKey)


for group in groups:
    for entity in group['entities']:
        if entity != serializedPublicKey:
            transaction = {
                "messageType": "SMS",
                "sender": serializedPublicKey,
                "receiver": entity,
                "context": "FirstMessage!"
            }

            apiConnectorMethods.sendTransaction(transaction)

time.sleep(7)

print("Done sending first messages")

print(apiConnectorMethods.getSentMessages(client1))

print("Recieved Messages")

print(apiConnectorMethods.getReceivedMessages(client2))
