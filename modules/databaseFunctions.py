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
    c.execute("CREATE TABLE Users(pNumber TEXT, Name TEXT)")
    c.execute("CREATE TABLE Drinks(DrinkID INT, Name TEXT, Percentage INT)")
    c.execute("CREATE TABLE Measures(measureID INT, Name TEXT, MeasureMl INT)")
    con.commit()

con = generateConnection()
createTables(con)


