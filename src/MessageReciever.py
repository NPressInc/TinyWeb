from flask import Flask, request


transactionQueue = []
PendingBlock = None
validationVotes = []
commitVotes = []

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/ProposeBlock", methods=['POST'])
def NewBlock():
    jsn = request.get_json()
    print(jsn)
    return "<p>Thank you for proposing your new block!</p>"

@app.route("/BlockVerified")
def BlockVerified():
    return "<p>Hello, World!</p>"

@app.route("/BlockCommitted")
def BlockCommitted():
    return "<p>Hello, World!</p>"

@app.route("/CheckBlockChain")
def CheckBlockChain():
    return "<p>Hello, World!</p>"

@app.route("/Transaction", methods=['POST'])
def Transaction():
    jsn = request.get_json()
    try:
        chainMessage = {
            "Address1": jsn["from"],
            "Type": "SMS",
            "Address2": jsn["to"],
            "Content": jsn["content"]
        }
        print("hi")
        print(chainMessage)
        transactionQueue.append(chainMessage)

        return "<p>Message Queued!</p>"

    except:
        return "<p>Something Went Wrong</p>"

    
    

