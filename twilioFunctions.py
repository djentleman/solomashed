from flask import Flask, request, redirect
import twilio.twiml
import parser
import json
import sqlite3 as lite
import sys 
 
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
    con = generateConnection()
    print "Reply (type): " + str(type(reply))
    print reply
    callback = reply[0]   
    print "callback (type): " + str(type(callback))
    print callback

    if callback == -1:
        return "You have had too much for your input to be parsed. Go home. Do not stop for a kebab."
    elif callback == 0:
        #play mum's spag
        return ""
    elif callback == 1:
        #try:
        # update database
            data = reply[1]
            insertUserDrink(con, str(sender), data[0], data[1])
            return "Your drink has been successfully added."
        #except:
            return "Shit code is shit :("
        #Return the number of units drunk
        #return ""
    elif callback == 2:
        return "I'm bad and that's good. I'll never be good and that's not bad. There's no one I'd rather be than SHREK."
    elif callback == 3:
        return """
            Commands:
            #################
            <drink> <measure> - update the drinks databases
            #################
            stats/statdump - display stats from your night out
            #################
            info - display help page
               """
    elif callback == 4:
        # dump out this nights stats
        drinks = drinksTonight(con, str(sender))
        return str(drinks)
    return ""




def generateConnection():
    try:
        con = lite.connect('solomashed.db')
        print "Successfully Connected"
        return con
    except:
        print "Could not connect"
        sys.exit(1)
    

def createTables(con):
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS Users")
    c.execute("DROP TABLE IF EXISTS Drinks")
    c.execute("DROP TABLE IF EXISTS Measures")
    c.execute("DROP TABLE IF EXISTS UserDrinks")
    c.execute("CREATE TABLE Users(pNumber TEXT, Name TEXT, unitsInSystem INT)")
    c.execute("CREATE TABLE Drinks(Name TEXT, Percentage INT)")
    c.execute("CREATE TABLE Measures(Name TEXT, MeasureMl INT)")
    c.execute("CREATE TABLE UserDrinks(userID TEXT, drinkID INT, measureID INT, timeConsumed DATETIME)")
    con.commit()

def populateDrinks(con):
    c = con.cursor()
    c.executescript("""
        INSERT INTO Drinks VALUES('beer', 4);
        INSERT INTO Drinks VALUES('wine', 13);
        INSERT INTO Drinks VALUES('lager', 4);
        INSERT INTO Drinks VALUES('vodka', 40);
        INSERT INTO Drinks VALUES('cider', 4);
        INSERT INTO Drinks VALUES('whiskey', 40);
        INSERT INTO Drinks VALUES('gin', 40);
        INSERT INTO Drinks VALUES('rum', 40);
        INSERT INTO Drinks VALUES('sake', 20);
        INSERT INTO Drinks VALUES('ragnarok', 10);
        INSERT INTO Drinks VALUES('ethanol', 100);
        INSERT INTO Drinks VALUES('moonshine', 70);
        INSERT INTO Drinks VALUES('absinthe', 60);
        INSERT INTO Drinks VALUES('superstrength', 10);
        INSERT INTO Drinks VALUES('mixer', 8);
        """)
    con.commit()

def populateMeasures(con):
    c = con.cursor()
    c.executescript("""
        INSERT INTO Measures VALUES('pint', 568);
        INSERT INTO Measures VALUES('shot', 25);
        INSERT INTO Measures VALUES('double', 50);
        INSERT INTO Measures VALUES('litre', 1000);
        INSERT INTO Measures VALUES('liter', 1000);
        INSERT INTO Measures VALUES('bottle', 700);
        INSERT INTO Measures VALUES('can', 500);
        INSERT INTO Measures VALUES('stubby', 333);
        INSERT INTO Measures VALUES('halfpint', 230);
        
        """)
    con.commit()

def populateUsers(con):
    c = con.cursor()
    c.executescript("""
        INSERT INTO Users VALUES('09382748293', 'Dave', 0);
        INSERT INTO Users VALUES('8314791794', 'Todd', 0);
        INSERT INTO Users VALUES('3987979175', 'Ben', 0);
        """)
    con.commit()

def getAllDrinks(con):
    c = con.cursor()
    c.execute("SELECT d.rowid, d.* FROM Drinks d")
    rows = c.fetchall()
    return rows
    
def getAllMeasures(con):
    c = con.cursor()
    c.execute("SELECT m.rowid, m.* FROM Measures m")
    rows = c.fetchall()
    return rows

def getAllUsers(con):
    c = con.cursor()
    c.execute("SELECT u.rowid, u.* FROM Users u")
    rows = c.fetchall()
    return rows

def getAllUserDrinks(con):
    c = con.cursor()
    c.execute("SELECT ud.rowid, ud.* FROM UserDrinks ud")
    rows = c.fetchall()
    return rows

def insertMeasure(con, name, measureMl):
    c = con.cursor()
    c.execute("INSERT INTO Measures VALUES(:name, :measureMl)", {"name": name, "measureMl" : measureMl})
    con.commit()

def insertDrink(con, name, percentage):
    c = con.cursor()
    c.execute("INSERT INTO Drinks VALUES(:name, :percentage)", {"name": name, "percentage" : percentage})
    con.commit()

def insertUser(con, pNumber, name):
    c = con.cursor()
    c.execute("INSERT INTO Users VALUES(:pNumber, :name, 0)", {"pNumber": pNumber, "name" : name})
    con.commit()

def drinksTonight(con, pNumber):
    c = con.cursor()
    c.execute("SELECT d.name, m.name from Drinks d, userDrinks ud, Measures m WHERE m.rowid = ud.measureID AND d.rowid = ud.drinkID AND ud.timeConsumed > datetime('now') - ('12:00:00')")
    queryRows = c.fetchall()
    con.commit()
    message = "Drinks Tonight: \n" + str(queryRows)
    message = message + "\n Total Units Dranks: \n" + str(averageUnitsInSystem(con, pNumber))
    message = message + "\n Current Blood Alchohol Units: \n" + str(getCurrentUnits(con, pNumber))
    drunkness = int(getCurrentUnits(con, pNumber))
    if drunkness <= 2:
        message = message + "You are Sober!"
    elif drunkness <= 4:
        message = message + "You got stuff to do today!"
    elif drunkness <= 6:
        message = message + "You are Tipsy!"    
    elif drunkness <= 8:
        message = message + "You are Wobbly!" 
    elif drunkness <= 10:
        message = message + "You are Merry!" 
    elif drunkness <= 12:
        message = message + "You are Drunk!"
    elif drunkness <= 14:
        message = message + "You are Pissed!" 
    elif drunkness <= 16:
        message = message + "You are Smashed!"
    elif drunkness <= 18:
        message = message + "You are Paraletic!"
    else:
        message = message + "You are SOLOSMASHED!"

    return message

def getCurrentUnits(con, pNumber):
    c = con.cursor()
    c.execute("SELECT u.unitsInSystem FROM Users u WHERE u.pNumber = :pNumber", {"pNumber" : pNumber})
    queryRows = c.fetchall()
    if len(queryRows) == 0:
        insertUser(con, pNumber, None)
    currentUnits = queryRows[0][0]
    con.commit()
    return currentUnits

def averageUnitsInSystem(con, pNumber):
    c = con.cursor()
    c.execute("SELECT ud.measureID, ud.drinkID FROM userDrinks ud where ud.userID = :pNumber", {"pNumber" : pNumber})
    queryRows = c.fetchall()
    drinks = []
    measures = []
    totalUnits = 0
    for row in queryRows:
        drinkID = row[1]
        c.execute("SELECT d.percentage FROM Drinks d where d.rowID = :drinkID", {"drinkID" : drinkID})
        drink = c.fetchall()[0][0]
        drinks.append(drink)
        measureID = row[0]
        c.execute("SELECT m.measureMl FROM Measures m where m.rowID = :measureID", {"measureID" : measureID})
        measure = c.fetchall()[0][0]
        measures.append(measure)
    for i in range(len(drinks)):
        totalUnits = totalUnits + ( int(drinks[i] * (float(measures[i])/float(1000))))
    print totalUnits

def insertUserDrink(con, pNumber, drinkName, measureName):
   
    c = con.cursor()

    c.execute("SELECT u.name FROM Users u WHERE u.pNumber = :pNumber", {"pNumber": pNumber})

    queryRows = c.fetchall()
    if len(queryRows) == 0:
        insertUser(con, pNumber, None)
    c.execute("SELECT d.percentage, d.rowid FROM Drinks d WHERE d.name = :drinkName", {"drinkName": drinkName})

    queryRows = c.fetchall()
    if len(queryRows) == 0:
        return ("No such drink as " + drinkName)
    drinkPercentage = queryRows[0][0]
    drinkID = queryRows[0][1]
    
    c.execute("SELECT m.measureMl, m.rowid FROM Measures m WHERE m.name = :measureName", {"measureName": measureName})
    queryRows = c.fetchall()
    if len(queryRows) == 0:
        return ("No such measure as " + drinkName)
    drinkMeasure = queryRows[0][0]
    measureID = queryRows[0][1]
    drinkUnits = int(drinkPercentage * (float(drinkMeasure)/float(1000)))
    c.execute("INSERT INTO UserDrinks VALUES(:pNumber, :drinkID, :measureID, datetime('now'))", {"pNumber": pNumber, "drinkID" : drinkID, "measureID" : measureID})    
    c.execute("UPDATE Users SET UnitsInSystem = UnitsInSystem + :drinkUnits WHERE pNumber = :pNumber", {"drinkUnits" : drinkUnits, "pNumber" : pNumber})
    con.commit()
    return "success"

con = generateConnection()
populateDrinks(con)
populateMeasures(con)

