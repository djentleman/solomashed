from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def processRequest():
	#Useful vars
    resp = twilio.twiml.Response()
    reply = "blank"
    sender = request.form["From"]
    message = request.form["Body"]

    #Debug output to console
    for formItem in request.form:
    	line = formItem + ": " + request.form[formItem] + "\n"
    print message

    #####Your function######
    #reply = someFunction(from,message)

    resp.message(reply)
    return str(resp)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
