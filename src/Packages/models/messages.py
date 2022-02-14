from dataclasses import dataclass
import datetime


@dataclass
class TinyMessage:
     messageType: str
     sender: str
     receiver: str
     context: str
     groupId:str
     conversationId: str
     dateTime: int

