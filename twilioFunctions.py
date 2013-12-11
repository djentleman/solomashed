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
    print "Reply (type): " + type(reply)
    print reply
    callback = reply[0]   
    print "callback (type): " + type(callback)
    print callback

    if callback == -1:
        return "You have had too much for your input to be parsed. Go home. Do not stop for a kebab."
    elif callback == 0:
        #play mum's spag
        return ""
    elif callback == 1:
        #Return the number of units drunk
        return ""
    elif callback == 2:
        return "I'm bad and that's good. I'll never be good and that's not bad. There's no one I'd rather be than SHREK."
    elif callback == 3:
        return "Commands:\n stats/statdump\n help"
    return ""
