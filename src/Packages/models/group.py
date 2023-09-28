from dataclasses import dataclass
from typing import List



@dataclass
class GroupDef():
    messageType: str
    sender: str
    groupType: str
    entities: List[str]
    description: str
    groupId: str