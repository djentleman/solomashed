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
    c.execute("CREATE TABLE Drinks(Name TEXT, Percentage INT)")
    c.execute("CREATE TABLE Measures(Name TEXT, MeasureMl INT)")
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



def getAllDrinks(con):
    c = con.cursor()
    c.execute("SELECT d.rowid, d.* FROM Drinks d")
    rows = c.fetchall()
    return rows
    


con = generateConnection()
createTables(con)
populateDrinks(con)






