MegaAdminRole = {
    "name": "MegaAdminRole",
    "permissionHashes": [
        "ReadMessagesFromGroup", 
        "SendMessagesToGroup", 
        "RecieveCallsFromGroup",
        "MakeCallsToGroup",
        "ReadLocationDataGroup"
    ]
}

SuperMemberRole = {
    "name": "SuperMemberRole",
    "permissionHashes": [
        "ReadMessagesFromGroup", 
        "SendMessagesToGroup", 
        "RecieveCallsFromGroup", 
        "MakeCallsToGroup",
        "ReadLocationDataMember"
    ]

}

MemberRole = {
    "name": "MemberRole",
    "permissionHashes": [
        "ReadMessagesFromGroup", 
        "SendMessagesToGroup", 
        "RecieveCallsFromGroup", 
        "MakeCallsToGroup",
        "ReadLocationDataSelf",
    ]
    

}

SubMemberRole = {
    "name": "SubMemberRole",
    "permissionHashes": [
        "ReadMessagesFromSuper",
        "SendMessagesToSuper",
        "RecieveCallsFromSuper",
        "MakeCallsToSuper",
        "ReadLocationDataSelf"
    ]
}

RoleDefinitions = [MegaAdminRole, SuperMemberRole, MemberRole, SubMemberRole]