from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def processRequest():
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
    #reply = someFunction(from,message)

    print reply
    resp.message(reply)
    return str(resp)
 
 def start():
    if __name__ == "__main__":
        app.run(host='0.0.0.0',debug=True)