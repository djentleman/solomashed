## parser

# takes in a string of words, runs a function call

import spell_check as spell
import json

"""
commands:
<drink> <amount>
stats/statdump
help
## easter eggs ##
shrek
spaghetti <amount>
#################
"""
# stuff that doesn't pass the spell check will get a -1 callback

# need to intellegently allocate stack depth

def removeDelimiters(strIn, delimiters):
    for pattern in delimiters:
        strIn = strIn.replace(pattern, " ")
    return strIn

getStackDepth = lambda: 2 # needs to be replaced with database query function

def spellCheck(strIn):
    stackDepth = getStackDepth()
    # remove any delimiters and stuff
    strIn = removeDelimiters(strIn, [",", ";", "_", "-"])
    words = [word for word in strIn.split(" ") if word != ""]
    spelledStr = ""
    for word in words:
        current = spell.correct(word, stackDepth)
        if current == "":
            return ""
        spelledStr+= (current + " ")
    
    return spelledStr[:-1]

def parse(strIn):
    strIn = spellCheck(strIn)
    if strIn == "":
        return json.dumps(-1, "") # cannot deciper spelling
    callback = -1
    if " " in strIn:
        if "spaghetti" in strIn:
            callback = 0#"play mom's spaghetti.mp3"
        else:
            callback = 1# "update database with: " + strIn.split(" ")[0] \
                  #+ ", " + strIn.split(" ")[1]
    else:
        if strIn == "shrek":
            callback = 2# "\"Therses Noone I'd Rather Be, Than Shrek\""
        elif strIn == "info":
            callback = 3# "run help system"
        elif strIn == "stats" or strIn == "statdump":
            callback = 4# "dump status [units in system, total units ever, etc...]"
    return json.dumps((callback, strIn.split(" ")))






