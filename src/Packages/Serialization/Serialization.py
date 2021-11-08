import json
import brotli

class Serialization:

    @staticmethod
    def serializeObjToJson(obj):
        return json.dumps(obj, default=lambda o: o.__dict__,sort_keys=True)

    @staticmethod
    def compressJsonString(input):
        return brotli.compress(input)

    @staticmethod
    def decompressJsonString(brotliData):
        return brotli.decompress(brotliData)