from Packages.Client.TinyWebClient import TinyWebClient
from Packages.FileIO.readLoadClient import readLoadClient
from Packages.Verification.Signing import Signing

from Packages.Client.ApiConnector import apiConnectorMethods




client1 = TinyWebClient.initializeClient("1")

client2 = TinyWebClient.initializeClient("2")

client3 = TinyWebClient.initializeClient("3")


apiConnectorMethods.getAllGroups(client1)















