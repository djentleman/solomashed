import sqlite3 as lite
import sys 

def generateCursor():
    try:
        con = lite.connect('solomashed.db')
        c = con.cursor()
        return c
    except:
        print "Could not connect"
        sys.exit(1)
    finally:
        if con:
            con.close()
    

def createTables(c):
    c.execute("CREATE TABLE 
    
