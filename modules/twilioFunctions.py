from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def processRequest():
    """Respond to incoming calls with a simple text message."""
 
    resp = twilio.twiml.Response()
    resp.message("Hello!")

    for formItem in request.form:
    	print formItem + ": " + request.form[formItem]

    return str(resp)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)