from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def processRequest():
    """Respond to incoming texts"""
    resp = twilio.twiml.Response()
    resp.message = (str(request))
    mesg = twilio.twiml.Message()
    return str(resp)

@app.route("/hi", methods=['GET', 'POST'])
def shit():
	resp = twilio.twiml.Response()
	mesg = twilio.twiml.Message()
	resp.message("Foloffle")	
	return str(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
