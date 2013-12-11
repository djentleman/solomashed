## parser

# takes in a string of words, runs a function call

import spell_check as spell

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
    pass

def spellCheck(strIn):
    # remove any delimiters and stuff
    strIn = strIn.replace(",", "").replace(";", "

def parse(strIn):
    strIn = spellCheck(strIn)
    callback = -1
    if " " in strIn:
        if "spaghetti" in strIn:
            callback = 0#"play mom's spaghetti.mp3"
        else:
            callback = 1#print("update database with: " + strIn.split(" ")[0] \
                  #+ ", " + strIn.split(" ")[1])
    else:
        if strIn == "shrek":
            callback = 2#print("\"Theres Noone I'd Rather Be, Than Shrek\"")
        elif strIn == "help":
            callback = 3#print("run help system")
        elif strIn == "stats" or strIn == "statdump":
            callback = 4#print("dump status [units in system, total units ever, etc...]")
    return callback






