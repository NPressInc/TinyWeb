MegaAdminRole = {
    "name": "MegaAdminRole",
    "permissions": [
        "ReadMessagesFromGroup", 
        "SendMessagesToGroup", 
        "RecieveCallsFromGroup",
        "MakeCallsToGroup",
        "ReadLocationDataGroup"
    ]
}

SuperMemberRole = {
    "name": "SuperMemberRole",
    "permissions": [
        "ReadMessagesFromGroup",
        "SendMessagesToGroup",
        "RecieveCallsFromGroup", 
        "MakeCallsToGroup",
        "ReadLocationDataMember"
    ]
}

MemberRole = {
    "name": "MemberRole",
    "permissions": [
        "ReadMessagesFromGroup", 
        "SendMessagesToGroup", 
        "RecieveCallsFromGroup", 
        "MakeCallsToGroup",
        "ReadLocationDataSelf"
    ]
}

SubMemberRole = {
    "name": "SubMemberRole",
    "permissions": [
        "ReadMessagesFromSuper",
        "SendMessagesToSuper",
        "RecieveCallsFromSuper",
        "MakeCallsToSuper",
        "ReadLocationDataSelf"
    ]
}


FledglingCommRole = {
    "name": "FledglingCommRole",
    "permissions": [
        "ReadMessagesFromFledgling",
        "SendMessagesToFledgling",
        "RecieveCallsFromFledgling",
        "MakeCallsToFledgling"
    ]
}

RoleDefinitions = [MegaAdminRole, SuperMemberRole, MemberRole, SubMemberRole, FledglingCommRole]