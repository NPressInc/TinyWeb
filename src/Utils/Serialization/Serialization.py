import json



class Serialization:

    @staticmethod
    def serializeObjToJson(obj):
        return json.dumps(obj, default=lambda o: o.__dict__,sort_keys=True, indent=4)