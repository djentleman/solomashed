from flask import Flask, request, redirect
import twilio.twiml
import parser
import json
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def processRequestText():
	#Useful vars
    resp = twilio.twiml.Response()
    reply = "Nothing at the moment"
    sender = request.form["From"]
    message = request.form["Body"]
    debug = ""

    #Debug output to console
    for formItem in request.form:
    	line = formItem + ": " + request.form[formItem] + "\n"
    	debug += line
    print "##########\n" + debug + "##########"

    print message

    #####Your function######
    reply = handleMessage(sender,message)

    print reply
    resp.message(reply)
    return str(resp)

@app.route("/voice", methods=['GET', 'POST'])
def processRequestVoice():
    pass
 

def start():
    app.run(host='0.0.0.0',debug=True)

def handleMessage(sender, message):
    reply = json.loads(parser.parse(message))
    print reply[0]

    return ""
