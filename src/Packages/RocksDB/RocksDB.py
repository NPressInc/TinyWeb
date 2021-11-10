import rocksdb

class Rocks:
    db = rocksdb.DB("blockChainDB.db", rocksdb.Options(create_if_missing=True))


def getGroupsFromPublicKey(publicKeyString):
    key = (publicKeyString + "Groups").encode()
    return Rocks.db.get(key)

def writeGroupsFromPublicKey(publicKeyString, GroupsString):
    key = (publicKeyString + "Groups").encode()
    Rocks.db.put(key, GroupsString.encode())

def getGroupFromGroupHash():
    print("TBI")

def getTransactionFromHash():
    print("TBI")

res = getGroupsFromPublicKey("asdf")
print(res)
if res == None:
    writeGroupsFromPublicKey("asdf", "{groups; all the peoples}")




"""
what does a user need access to to be able to send 
"""