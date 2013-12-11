import sqlite3 as lite
import sys 

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
        INSERT INTO Drinks VALUES('vodka', 40);
        """)
    con.commit()

def populateMeasures(con):
    c = con.cursor()
    c.executescript("""
        INSERT INTO Measures VALUES('pint', 568);
        INSERT INTO Measures VALUES('shot', 44);
        INSERT INTO Measures VALUES('litre', 1000);
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
    return queryRows

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

def getCon():
    return con

con = generateConnection()
createTables(con)
populateDrinks(con)
populateUsers(con)
populateMeasures(con)



