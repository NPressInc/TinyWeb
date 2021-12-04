import rocksdb

class Rocks:
    db = rocksdb.DB("blockChainDB.db", rocksdb.Options(create_if_missing=True))

    def getGroupsFromPublicKey(publicKeyString):
        key = (publicKeyString + "Groups").encode()
        return Rocks.db.get(key).decode()

    def setGroupsFromPublicKey(publicKeyString, GroupsString):
        key = (publicKeyString + "Groups").encode()
        Rocks.db.put(key, GroupsString.encode())

    def getGroupFromGroupHash(groupHash):
        key = (groupHash).encode()
        return Rocks.db.get(key).decode()

    def setGroupFromGroupHash(groupHash, GroupString):
        key = (groupHash).encode()
        Rocks.db.put(key, GroupString.encode())
    

    def getTransactionFromHash(hash):
        key = (hash).encode()
        return Rocks.db.get(key).decode()





    def getSentMessagesFromPublicKey(publicKeyString):
        key = (publicKeyString + "Sent").encode()
        return Rocks.db.get(key).decode()

    def setSentMessagesFromPublicKey(publicKeyString, GroupsString):
        key = (publicKeyString + "Sent").encode()
        Rocks.db.put(key, GroupsString.encode())


    def getRecievedMessagesFromPublicKey(publicKeyString):
        key = (publicKeyString + "Recieved").encode()
        return Rocks.db.get(key).decode()

    def setRecievedMessagesFromPublicKey(publicKeyString, GroupsString):
        key = (publicKeyString + "Recieved").encode()
        Rocks.db.put(key, GroupsString.encode())












"""
what does a user need access to to be able to send 
"""