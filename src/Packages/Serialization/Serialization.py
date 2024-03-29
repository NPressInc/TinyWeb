import json
import brotli
import hashlib

class Serialization:

    @staticmethod
    def serializeObjToJson(obj):
        return json.dumps(obj, default=lambda o: o.__dict__,sort_keys=True)

    @staticmethod
    def deserializeObjFromJsonR(obj):
        counter = 0
        data = obj
        while isinstance(data, str):
            counter += 1
            data = json.loads(data)
            if counter > 30:
                break
        return data

    @staticmethod
    def hashObject(obj):
        objString = json.dumps(obj, sort_keys=True)
        return hashlib.sha256(objString.encode()).hexdigest()

    @staticmethod
    def hashString(strToHash):
        return hashlib.sha256(strToHash.encode()).hexdigest()

    @staticmethod
    def compressJsonString(input):
        return brotli.compress(input)

    @staticmethod
    def decompressJsonString(brotliData):
        return brotli.decompress(brotliData)



    @staticmethod
    def serializeRoleAssignment(inputData):

        RoleDefString = json.dumps(inputData, sort_keys=True)

        return RoleDefString


    @staticmethod
    def serializeRoleDef(inputData):

        RoleDefString = json.dumps(inputData, sort_keys=True)

        return RoleDefString

    @staticmethod
    def hashRoleDef(inputData):
        """
        "messageType": "RoleDescriptor",
                "name": RoleDef["name"],
                "hash": "",
                "creator": "-1",
                "permissionHashes": RoleDef["permissionHashes"]
        """
        roleDef = {
            "messageType": inputData["messageType"],
            "name": inputData["name"],
            "creator": inputData["creator"],
            "permissionHashes": inputData["permissionHashes"]
        }
        RoleDefString = json.dumps(roleDef, sort_keys=True)

        hash = hashlib.sha256(RoleDefString.encode()).hexdigest()

        return hash

    @staticmethod
    def serializePermissionDef(inputData):

        PermissionDefString = json.dumps(inputData, sort_keys=True)

        return PermissionDefString


    """
    newPermission = {
                "messageType": "PermissionDescriptor",
                "type": Permission["type"],
                "scope": Permission["scope"],
                "hash": "",
                "creator": "-1"
            }
    """

    @staticmethod
    def hashPermissionDef(inputData):
        groupDef = {
            "messageType": inputData["messageType"],
            "name": inputData["name"],
            "type": inputData["type"],
            "scope": inputData["scope"],
            "sender": inputData["sender"]
        }
        PermissionDefString = json.dumps(groupDef, sort_keys=True)

        hash = hashlib.sha256(PermissionDefString.encode()).hexdigest()

        return hash


    @staticmethod
    def serializeGroupDef(inputData):

        GroupDefString = json.dumps(inputData, sort_keys=True)

        return GroupDefString

    @staticmethod
    def hashGroupDef(inputData):
        groupDef = {
            "messageType": inputData["messageType"],
            "creator": inputData["creator"],
            "groupType": inputData["groupType"],
            "entities": inputData["entities"],
            "description": inputData["description"]
        }
        
        GroupDefString = json.dumps(groupDef, sort_keys=True)

        hash = hashlib.sha256(GroupDefString.encode()).hexdigest()

        return hash
        

    @staticmethod
    def getBase64String(inputBytes):
        import base64
        return base64.b64encode(inputBytes).decode("utf-8")

    @staticmethod
    def getOriginalBytesFromBase64String(inputBase64String):
        import base64
        return base64.b64decode(inputBase64String.encode("utf-8"))
