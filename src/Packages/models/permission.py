from dataclasses import dataclass

@dataclass
class Permission:
    messageType: str
    name: str
    type: str
    scope: str
    sender: str