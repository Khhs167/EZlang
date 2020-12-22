### Startup variables, only alivalable here
debug = True


### Imports
import sys
import tkinter
from tkinter import filedialog

### IMPORTANT VARIABLES

recursion = 100
variables = {} #The variable list, contains different types
code = [] #The script to debug

### Layer system

layer = 0
layers = []
inFuncDef = False

### Open file
noa = len(sys.argv)
args = sys.argv
root = tkinter.Tk()
root.withdraw()
if debug:
    compilefile = "test.ez"
elif noa == 1:
    compilefile = filedialog.askopenfilename()
else:
    #print(args[1])
    compilefile = args[1]

if not (compilefile == ""):
    code = open(compilefile, "r").read()
else:
    code = 'Write("No file specified!");\n'

### Remove newlines and split at semicolons

code2  = code.split("\n")
newCode = []
for p in code2:
    newCode.append(p.lstrip())
code2 = newCode
code = ''.join(code2).split(";")
code = code[:len(code)-1]


### Define some important functions

def noNewLine(string):
    code2  = string.split("\n")
    newCode = []
    for p in code2:
        newCode.append(p.lstrip())
    code2 = newCode
    code = ''.join(code2).split(";")
    return code[:len(code)-1]

def execLine(line):
    global recursion
    global code
    global i
    global inFuncDef
    global layer
    global layers
    sys.setrecursionlimit(recursion)
    recursion += 1

    if(line[0] == "#"):
        return
    if line[:len("function ")] == "function ":
        inFuncDef = True
        layer+=1
        layers.insert(layer, "function")
        variables[line[len("function "):].split("{")[0]] = []
        variables[line[len("function "):].split("{")[0]].append("Function")
        variables[line[len("function "):].split("{")[0]].append(line[len("function "):].split("{")[1].split("}")[0].split(":"))
    elif line[:len("Write(")] == "Write(":
        if (line[len("Write("):len(line)-1] in variables):
            print(variables[line[len("Write("):len(line)-1]][0])
        elif (line[len("Write("):][0] == "\""):
            print(line[len("Write(") + 1:len(line)-2])
    elif line[:len("if[")] == "if[":
        comparison = line[len("if["):].split("]")[0].split(",")[0]
        if ("==" in comparison):
            if (variables[comparison.split("==")[0]] == variables[comparison.split("==")[1]]):
                execLine(line[len("if["):].split("]")[0].split(",")[1])
        elif (">" in comparison):
            if (variables[comparison.split(">")[0]] > variables[comparison.split(">")[1]]):
                execLine(line[len("if["):].split("]")[0].split(",")[1])
        elif ("<" in comparison):
            if (variables[comparison.split("<")[0]] < variables[comparison.split("<")[1]]):
                execLine(line[len("if["):].split("]")[0].split(",")[1])
        elif ("!=" in comparison):
            if (variables[comparison.split("!=")[0]] != variables[comparison.split("!=")[1]]):
                execLine(line[len("if["):].split("]")[0].split(",")[1])
    elif line.split("(")[0] in variables:
        func = line.split("(")[0]
        if (variables[func][0] == "Function"):
            for funcLine in variables[func][1]:
                execLine(funcLine)
    elif "<-" in line:
        if (not "Input()" in line):
            try:
                variables[line.split("<-")[0]] = [int(line.split("<-")[1])]
            except:
                variables[line.split("<-")[0]] = [line.split("<-")[1]]
        else:
            variables[line.split("<-")[0]] = [input()]
    elif line[:len(line)-2] in variables and "++" in line:
        variables[line[:len(line)-2]] = [int(variables[line[:len(line)-2]][0]) + 1]
    elif line[:len(line)-2] in variables and "--" in line:
        variables[line[:len(line)-2]] = [int(variables[line[:len(line)-2]][0]) - 1]
    elif line[:len("python ")] == "python ":
        eval(line[len("python "):])
    elif line == "Stop()":
        print("Stopping program...")
        quit()
    elif line[:len("use ")] == "use ":
        for b in range(len(noNewLine(open(line[len("use "):] + ".ez", "r").read()))): 
            code.insert(b + i + 1, noNewLine(open(line[len("use "):] + ".ez", "r").read())[b])
    else:
        print("No command called \"" + line + "\", assuming it's okay")
i = 0
while i < len(code):
    execLine(code[i])
    i += 1
