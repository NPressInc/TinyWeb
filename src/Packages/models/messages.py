from dataclasses import dataclass
import datetime
import dataclasses
import json

class EnhancedJSONEncoder(json.JSONEncoder):
     def default(self, o):
          if dataclasses.is_dataclass(o):
               return dataclasses.asdict(o)
          return super().default(o)

@dataclass
class TinyMessage:
     
     messageType: str
     sender: str
     receiver: str
     context: str
     groupId:str
     conversationId: str
     dateTime: int
     def toJson(self):
          return json.dumps(self, cls=EnhancedJSONEncoder)


