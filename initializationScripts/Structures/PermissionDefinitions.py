PermissionDefinitions = [
    #the user can read messages that they sent and recieve from their groups
    {
        "name": "ReadMessagesFromGroup",
        "type": "SMS",
        "scope": "group"
    },
    #the user can read messages from everyone in the fledgling group
    {
        "name": "ReadMessagesFromFledgling",
        "type": "SMS",
        "scope": "Fledglings"
    },
    #the user can send messages to everyone in their group
    {
        "name": "SendMessagesToGroup",
        "type": "SMS",
        "scope": "group"
    },

    #the user can send messages to everyone in the fledgling group
    {
        "name": "SendMessagesToFledgling",
        "type": "SMS",
        "scope": "Fledglings"
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
    #the user can recieve calls directed towards them from their group
    {
        "name": "RecieveCallsFromGroup",
        "type": "Voice",
        "scope": "group"
    },

    #the user can recieve calls directed towards them from the fledgling group
    {
        "name": "RecieveCallsFromFledgling",
        "type": "Voice",
        "scope": "Fledglings"
    },
    #the user can voice call anyone in their group
    {
        "name": "MakeCallsToGroup",
        "type": "Voice",
        "scope": "group"
    },
    #the user can voice call users in the fledgling group
    {
        "name": "MakeCallsToFledgling",
        "type": "Voice",
        "scope": "Fledglings"
    },
    #can recieveCalls from super members
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