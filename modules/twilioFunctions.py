from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def processRequest():
    """Respond to incoming calls with a simple text message."""
 
    resp = twilio.twiml.Response()
    message = ""

    for formItem in request.form:
    	line = formItem + ": " + request.form[formItem] + "\n"
    	message += line

    resp.message(message)
    print message

    return str(resp)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
