from Packages.structures.TinyWebClient import TinyWebClient
from Packages.FileIO.readLoadClient import readLoadClient
from Packages.Verification.Signing import Signing



TinyWebClient


client1 = TinyWebClient.initClient("1")


client2 = TinyWebClient.initClient("2")


print(client1.seriralizeJSON())


print(client2.seriralizeJSON())










