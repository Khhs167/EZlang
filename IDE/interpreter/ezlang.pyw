import importlib
import sys
import os
from inspect import *

### SYSTEM DEFINITION ###

# VARIABLES #

#Because i use C# a lot
Null = None
null = None
true = True
false = False

variables = {}
linepos = 0
filename = sys.argv[1] if len(sys.argv) > 1 else ""

# CLASSES #

class Container:
    content = ""

class Function:
    content = ""
    parameters = []

class Library:
    module = None
    used = False

# FUNCTIONS #

def paraSplit(string):

    stringSplit = []

    layers = []
    currentLayer = ""

    lastComma = 0
    i = 0
    while (i < len(string)):
        c = string[i]
        if (c == "(" and currentLayer != "str"):
            currentLayer = "func"
            layers.append("func")
        if (c == ")" and currentLayer == "func"):
            layers.pop()
            currentLayer = layers[len(layers)-1] if len(layers) > 0 else ""
        if (c == "\"" and currentLayer != "str"):
            layers.append("str")
            currentLayer = "str"
        if (c == "\"" and currentLayer == "str"):
            layers.pop()
            currentLayer = layers[len(layers)-1] if len(layers) > 0 else ""
        if (c == "," and currentLayer == ""):
            stringSplit.append(string[lastComma:i])
            lastComma = i
        i += 1
    if (string[1] == ","):
        string = string[1:]
    stringSplit.append(string[lastComma:i])


    return stringSplit

def RunLine(line):
    line = str(line)
    commands = line.split(" ")
    if (len(commands) == 0):
        return null
    elif (commands[0] == "set"):
        if (len(commands) < 3):
            print("Faulty operation!")
            return null
        variables[commands[1]] = RunLine(commands[3])
        return null
    elif (line.isnumeric()):
        return float(line)
    elif (commands[0] == "include"):
        if (len(commands) < 2):
            print("Missing library.")
            return null
        mod = importlib.import_module(commands[1])
        lib = Library()
        lib.module = mod
        variables[commands[1]] = lib
        return null
    elif (commands[0] == "use"):
        if (len(commands) < 2):
            print("Missing library.")
            return null
        if (not commands[1] in variables.keys()):
            print("No imported library called '" + commands[1] + "'")
            return null
        if (not type(variables[commands[1]]) == Function()):
            print("'" + commands[1] + "' is not a library")
        variables[commands[1]].used = True
    elif (line in variables):
        return variables[line]
    elif (commands[0].split(".", 1)[0] in variables):
        #print("." + commands[0].split(".", 1)[1].split("(", 1)[0] + ".")
        if (hasattr(variables[commands[0].split(".", 1)[0]].module, commands[0].split(".", 1)[1].split("(", 1)[0])):
            func = getattr(variables[commands[0].split(".", 1)[0]].module, commands[0].split(".", 1)[1].split("(", 1)[0])
            if (not callable(func)):
                print("The function is not callable")
                return null
            params = paraSplit(commands[0].split(".", 1)[1].split("(", 1)[1].split(")", 1)[0])
            #print(commands[0].split(".", 1)[1].split("(", 1)[1].split(")", 1)[0])
            executedParams = []
            for param in params:
                #print(param)
                executedParams.append(RunLine(param))
            funcParams = signature(func).parameters
            for param in params:
                executedParams.append(RunLine(param))
            if (len(funcParams) == 0):
                return func()
            func(*executedParams[1:])
        else:
            print(commands[0].split(".")[0] + " does not have the attribute " + commands[0].split(".")[1].split("(")[0])
            return null
    elif (line.startswith("\"")):
        return line.replace("\\\"", "`").split("\"")[1].replace("`", "\"")
    else:
        print(line + " is not valid!")