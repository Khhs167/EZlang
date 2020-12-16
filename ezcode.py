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

def execLine(line):
    global recursion
    sys.setrecursionlimit(recursion)
    recursion += 1

    if(line[0] == "#"):
        return

    if line[:len("function ")] == "function ":
        variables[line[len("function "):].split("{")[0]] = []
        variables[line[len("function "):].split("{")[0]].append("Function")
        variables[line[len("function "):].split("{")[0]].append(line[len("function "):].split("{")[1].split("}")[0].split(":"))
    elif line[:len("Write(")] == "Write(":
        if (line[len("Write("):len(line)-1] in variables):
            print(variables[line[len("Write("):len(line)-1]][0])
        elif (line[len("Write("):][0] == "\""):
            print(line[len("Write(") + 1:len(line)-2])
    
    elif line.split("(")[0] in variables:
        func = line.split("(")[0]
        if (variables[func][0] == "Function"):
            for funcLine in variables[func][1]:
                execLine(funcLine)
    elif "<-" in line:
        variables[line.split("<-")[0]] = [line.split("<-")[1]]
    elif line[:len(line)-2] in variables and "++" in line:
        variables[line[:len(line)-2]] = [int(variables[line[:len(line)-2]][0]) + 1]
    elif line[:len(line)-2] in variables and "--" in line:
        variables[line[:len(line)-2]] = [int(variables[line[:len(line)-2]][0]) - 1]
    elif line[:len("python ")] == "python ":
        eval(line[len("python "):])
    else:
        print("No command called \"" + line + "\", assuming it's okay")


for codeLine in code:
    execLine(codeLine)
