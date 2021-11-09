




class readLoadClient():
    @staticmethod
    def saveClientKeys(clientKeysString, clientId):
        byteRep = clientKeysString.encode()
        f = open("State/ClientKeys" + clientId +".dat","Wb")
        f.write(byteRep)
        f.close()

    @staticmethod
    def loadClientKeysString(clientId):
        try:
            f = open("State/ClientKeys" + clientId +".dat","rb")
            resultBytes = f.read()
            f.close()
            return resultBytes.decode()
        except:
            return "LoadError"

        
        