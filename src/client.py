from Packages.Client.TinyWebClient import TinyWebClient
from Packages.FileIO.readLoadClient import readLoadClient
from Packages.Serialization.keySerialization import keySerialization
from Packages.Verification.Signing import Signing
from Packages.Client.ClientSimulator import ClientSimulator

from Packages.Client.ApiConnector import apiConnectorMethods

import time

import json


client1 = TinyWebClient.initializeClient("1")

client2 = TinyWebClient.initializeClient("2")

client3 = TinyWebClient.initializeClient("3")



serializedPublicKey1 = keySerialization.serializePublicKey(client1.publicKey)
serializedPublicKey2 = keySerialization.serializePublicKey(client2.publicKey)


client1.sendTestMessages(client2)

time.sleep(2)

print("Done sending first messages")

print(apiConnectorMethods.getSentMessages(client1))

print("Recieved Messages")

print(apiConnectorMethods.getReceivedMessages(client2))
