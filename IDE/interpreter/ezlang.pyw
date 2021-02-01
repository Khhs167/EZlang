import importlib
import sys

variables = {}
functions = {}
statements = {}
libraries = {}
usedlibs = []
linepos = 0
returnVal = None
filename = sys.argv[1]
def RunLine(line):
    global returnVal
    global linepos
    global filename
    if("//" in line):
        return
    if ("set" in line):
        if ("string" in line):
            variables[line.split(" to ")[0][len("set string "):]] = string()
            variables[line.split(" to ")[0][len("set string "):]].value = line.split(" to ")[1].split("\"")[1]
        elif ("num" in line):
            #print(int(line.split(" to ")[1]))
            variables[line.split(" to ")[0][len("set int "):]] = num()
            variables[line.split(" to ")[0][len("set int "):]].value = int(line.split(" to ")[1])
        elif("return" in line):
            RunFunc(line.split(" to ")[1])
            if (type(returnVal) == int or type(returnVal) == float):
                variables[line.split(" to ")[0][len("set return "):]] = num()
            if (type(returnVal) == str):
                variables[line.split(" to ")[0][len("set return "):]] = string()
            variables[line.split(" to ")[0][len("set return "):]].value = returnVal
            returnVal = None
        else:
            if (line.split(" ")[1].split(" to ")[0] in variables.keys()):
                if (type(variables[line.split(" ")[1].split("")[0]]) == num):
                    variables[line.split(" to ")[0][len("set "):]].value = int(line.split(" to ")[1])
                if (type(variables[line.split(" ")[1].split(" to ")[0]]) == string):
                    variables[line.split(" to ")[0][len("set "):]].value = line.split(" to ")[1].split("\"")[1]
    elif ("use " == line[:len("use ")]):
        libraries[line[len("use "):]] = importlib.import_module(line[len("use "):])
    elif ("include " == line[:len("include ")]):
        #print("included lib: " + line[len("include "):])
        usedlibs.append(libraries[line[len("include "):]])
    elif("(" in line):
        RunFunc(line)
    elif ("return " in line):
        returnVal = variables[line[len("return "):]]
    else:
        if (line != ""):
            print("Error at line: " + str(linepos) + ". " + line + " is not a valid command, in file " + filename + ", assuming it is ok")


def RunProgram(program):  
    for definition in program.keys():  
        if(definition == "program"):
            for line in program[definition].split(";"):
                if not ("//" in line):
                    RunLine(line)

def DefineFunctions(program):
    for func in program.keys():
        if ("function " == func[:len("function ")]):
            newFunc = function()
            for line in program[func].split(";"):
                if not ("//" in line):
                    newFunc.value.append(line)
            for param in func.split("(")[1].split(")")[0].replace(", ", ",").replace(" ,", ",").split(","):
                newFunc.params.append(param)
            functions[func[len("function "):].split("(")[0]] = newFunc

def DefineStatements(program):
    for state in program.keys():
        if ("statement" == state[:len("statement")]):
            newState = statement
            for line in program[state].split(";"):
                if not ("//" in line):
                    newState.value.append(line)
            statements[state[len("statement "):].split("(")[0]] = newState

def RunFunc(function):
    global returnVal
    global variables
    if(function.split("(")[0] in functions.keys()):
        oldVars = variables
        params = function.split("(")[1].split(")")[0].replace(", ", ",").replace(" ,", ",").split(",")
        for i in range(len(params)):
            variables[functions[function.split("(")[0]].params[i]] = params[i]
        for line in functions[function.split("(")[0]].value:
            RunLine(line)
        variables = oldVars
    elif (function.split("(")[0] in statements):
        comparisons = function.split("(")[1].split(")")[0].split(",")
        if (comparisons[1] == "="):
            if(variables[comparisons[0]].value == variables[comparisons[2]].value):
                for line in statements[function.split("(")[0]].value:
                    RunLine(line)
        if (comparisons[1] == ">"):
            if(variables[comparisons[0]].value > variables[comparisons[2]].value):
                for line in statements[function.split("(")[0]].value:
                    RunLine(line)
        if (comparisons[1] == "<"):
            if(variables[comparisons[0]].value < variables[comparisons[2]].value):
                for line in statements[function.split("(")[0]].value:
                    RunLine(line)
        if (comparisons[1] == "!="):
            if(variables[comparisons[0]].value != variables[comparisons[2]].value):
                for line in statements[function.split("(")[0]].value:
                    RunLine(line)
    elif (function.split(".")[0] in libraries.keys()):
        funcToExec = getattr(libraries[function.split(".")[0]], function.split(".")[1].split("(")[0])
        params = function.split("(")[1].split(")")[0].replace(", ", ",").replace(" ,", ",").split(",")
        if (params[0] != ""):
            newParams = []
            for param in params:
                if (param in variables.keys()):
                    newParams.append(variables[param].value)
                elif("\"" in param):
                    newParams.append(param.replace("\"", "").replace("\\c", ",").replace("\\n", "\n").replace("\\t", "\t"))
                elif(param.isnumeric()):
                    newParams.append(int(param))
                else:
                    RunFunc(param)
                    newParams.append(returnVal)
            params = newParams
        if(params[0] != ""):
            possibleRet = funcToExec(*params)
        else:
            possibleRet = funcToExec()
        if possibleRet != None:
            returnVal = possibleRet
    elif (isValid(function.split("(")[0])):
        funcToExec = getattr(getLib(function.split("(")[0]), function.split("(")[0])
        params = function.split("(")[1].split(")")[0].replace(", ", ",").replace(" ,", ",").split(",")
        if (params[0] != ""):
            newParams = []
            for param in params:
                if (param in variables.keys()):
                    newParams.append(variables[param].value)
                elif("\"" in param):
                    newParams.append(param.replace("\"", "").replace("\\c", ",").replace("\\n", "\n").replace("\\t", "\t"))
                elif(param.isnumeric()):
                    newParams.append(int(param))
                else:
                    RunFunc(param)
                    newParams.append(returnVal)
            params = newParams
        if(params[0] != ""):
            possibleRet = funcToExec(*params)
        else:
            possibleRet = funcToExec()
        if possibleRet != None:
            returnVal = possibleRet
    else:
        print(function + " is not valid")

def isValid(func):
    for mod in usedlibs:
        if (hasattr(mod, func)):
            return True
    return False

def getLib(func):
    for mod in usedlibs:
        if (hasattr(mod, func)):
            return mod
class Container:
    surroundIdentifier = ""
    typeOfContainer = 0
    children = []

class num:
    value = 0

class string:
    value = ""


class function:
    value = []
    params = []

class statement:
    value = []

program = open(filename, "r").read().replace("\t", "").replace("\n", "").replace("  ", "").split("}")
newProgram = {}
for cmd in program[:len(program)-1]:
    newProgram[cmd.split("{")[0]] = cmd.split("{")[1]
program = newProgram
#print(program)
DefineFunctions(program)
DefineStatements(program)
RunProgram(program)

#print(variables["hie"].value)
#print(functions["hi()"].value)
