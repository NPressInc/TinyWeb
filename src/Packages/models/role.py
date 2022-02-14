from dataclasses import dataclass
from typing import List


@dataclass
class RoleDef:
    messageType: str
    name: str
    sender: str
    permissionNames: List[str]


class RoleAssignment:
    messageType: str
    user: str
    roleName: str
    groupId: str
    sender: str


