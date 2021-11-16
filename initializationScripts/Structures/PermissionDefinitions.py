PermissionDefinitions = [
    #the user can read messages that they sent and recieve from their groups
    {
        "name": "ReadMessagesFromGroup",
        "type": "SMS",
        "scope": "group"
    },
    #the user can send messages to everyone in their group
    {
        "name": "SendMessagesToGroup",
        "type": "SMS",
        "scope": "group"
    },

    #the user can read messages that they sent and recieve from superMembers
    {
        "name": "ReadMessagesFromSuper",
        "type": "SMS",
        "scope": "super"
    },
    #the user can send messages to superMembers in their group
    {
        "name": "SendMessagesToSuper",
        "type": "SMS",
        "scope": "super"
    },
    #the user can recieve class directed towards them
    {
        "name": "RecieveCallsFromGroup",
        "type": "Voice",
        "scope": "group"
    },
    #the user can voice call anyone in their group
    {
        "name": "MakeCallsToGroup",
        "type": "Voice",
        "scope": "group"
    },
    {
        "name": "RecieveCallsFromSuper",
        "type": "Voice",
        "scope": "super"
    },
    #the user can voice call anyone in their group
    {
        "name": "MakeCallsToSuper",
        "type": "Voice",
        "scope": "super"
    },
    #the user can see their own Location data
    {
        "name": "ReadLocationDataSelf",
        "type": "GPS",
        "scope": "self"
    },
    #the user can see all the groups Location data 
    {
        "name": "ReadLocationDataGroup",
        "type": "GPS",
        "scope": "group"
    },
    #the user can see the location of users with role"Member", will be included in superMember
    {
        "name": "ReadLocationDataMember",
        "type": "GPS",
        "scope": "groupMember"
    }
]