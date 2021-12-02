MegaAdminRole = {
    "name": "MegaAdminRole",
    "permissions": [
        "ReadMessagesFromGroup", 
        "SendMessagesToGroup", 
        "RecieveCallsFromGroup",
        "MakeCallsToGroup",
        "ReadLocationDataGroup",
        "ReadMessagesFromFledgling",
        "SendMessagesToFledgling",
        "RecieveCallsFromFledgling",
        "MakeCallsToFledgling"
    ]
}

SuperMemberRole = {
    "name": "SuperMemberRole",
    "permissions": [
        "ReadMessagesFromGroup",
        "SendMessagesToGroup",
        "RecieveCallsFromGroup", 
        "MakeCallsToGroup",
        "ReadLocationDataMember",
        "ReadMessagesFromFledgling",
        "SendMessagesToFledgling",
        "RecieveCallsFromFledgling",
        "MakeCallsToFledgling"
    ]
}

MemberRole = {
    "name": "MemberRole",
    "permissions": [
        "ReadMessagesFromGroup", 
        "SendMessagesToGroup", 
        "RecieveCallsFromGroup", 
        "MakeCallsToGroup",
        "ReadLocationDataSelf",
        "ReadMessagesFromFledgling",
        "SendMessagesToFledgling",
        "RecieveCallsFromFledgling",
        "MakeCallsToFledgling"
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

RoleDefinitions = [MegaAdminRole, SuperMemberRole, MemberRole, SubMemberRole]