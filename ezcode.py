import string as stringmod
import tkinter
import sys
import os
from tkinter import filedialog
x = 500
sys.setrecursionlimit(x)
string = stringmod.ascii_letters
funcname = string
statements = string
func = [funcname, "(", statements, ");"]

noa = len(sys.argv)
args = sys.argv
root = tkinter.Tk()
root.withdraw()
if noa == 1:
    compilefile = filedialog.askopenfilename()
else:
    #print(args[1])
    compilefile = args[1]

code = open(compilefile, "r").read()

code2  = code.split("\n")
newCode = []
for p in code2:
    newCode.append(p.lstrip())
code2 = newCode
code = ''.join(code2).split(";")
write = func
write[0] = "write"
write[2] = string
root.destroy()
variables = {}

funcs = {}
oldcode = code
code = []
for checkline in oldcode:
    if checkline != "":
        if checkline[:1] == "\n":
            checkline = checkline[1:]
        code.append(checkline)

def clear(): 
  
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

def execode():
    global code
    global variables
    for line in code:
        if(line[0] != "#"):
            if "function" in line:
                cmds = line.split("{")[1].split("}")[0].split(":")
                #print(cmds)
                if " {" in line:
                    funcs[line[len("function")+1:line.index("{")-1] + "()"] = cmds
                else:
                    funcs[line[len("function")+1:line.index("{")] + "()"] = cmds
                #print(funcs)
            elif "Write(" in line and line[6] == '"' and line[len(line) - 2] == '"':
                print(line[7:len(line) - 2])
            elif "Write(" in line:
                calc = str(line)[6:len(str(line))-1]
                result = "error, faulty equation!"
                if(calc in variables.keys()):
                    result = variables[calc]
                elif calc.split(" ")[1] in ["+", "-", "*", "/", "^"]:
                    calc = calc.split(" ")
                    if (calc[1] == "+"):
                        result = int(calc[0]) + int(calc[2])
                    elif (calc[1] == "-"):
                        result = int(calc[0]) - int(calc[2])
                    elif (calc[1] == "*"):
                        result = int(calc[0]) * int(calc[2])
                    elif (calc[1] == "/"):
                        result = int(calc[0]) / int(calc[2])
                    elif (calc[1] == "^"):
                        result = int(calc[0]) ** int(calc[2])
                print(result)
            elif "<-" in line:
                lineToWork = line.split("<-")
                inp = lineToWork[1][1:]
                if ("Input()" in line):
                    inp = input()
                variables[''.join(lineToWork[0][0:len(lineToWork[0])-1])] = inp
                #print(variables)

            elif line in funcs.keys():
                #print(funcs[line])
                for cmd in funcs[line]:
                    execodeline(cmd)
            elif "python" in line:
                eval(line[len("python")+1:])
            elif "Input()" in line:
                input()
            elif "<-" in line:
                lineToWork = line.split("<-")
                #print(lineToWork)
                if ("Input()" in line):
                    inp = input()
                variables[''.join(lineToWork[0][0:len(lineToWork[0])-1])] = inp
                #print(variables)

            elif "ifequal" in line:
                lineForWork = line[len("if"):].split("{")[1].split(",")
                if (int(variables[lineForWork[0]]) == int(lineForWork[1])):
                    execodeline(lineForWork[2][1:len(lineForWork[2])-1])
            elif "ifless" in line:
                lineForWork = line[len("if"):].split("{")[1].split(",")
                if (int(variables[lineForWork[0]]) < int(lineForWork[1])):
                    execodeline(lineForWork[2][1:len(lineForWork[2])-1])

            elif line[:len(line)-2] in variables.keys() and "++" in line:
                variables[line[:len(line)-2]] = int(variables[line[:len(line)-2]]) + 1
            elif line[:len(line)-2] in variables.keys() and "--" in line:
                variables[line[:len(line)-2]] = int(variables[line[:len(line)-2]]) - 1
            
            elif line in funcs.keys():
                #print(funcs[line])
                for cmd in funcs[line]:
                    execodeline(cmd)
            elif "python" in line:
                eval(line[len("python")+1:])
            elif "Input()" in line:
                input()
            elif "Clear()" in line:
                clear()
            elif "import" in line:
                os.system("cd " + os.getcwd() + " & " + "python ezcode.py " + line[len("import"):])
            else:
                print("No program called " + line + " assuming it is okay")

def execodeline(code):
    global x
    global variables
    x += 1
    sys.setrecursionlimit(x)
    line = str(code)
    if str(line).find("Write(") != -1 and line[6] == '"' and line[len(line) - 2] == '"':
        print(line[7:len(line) - 2])
    elif str(line).find("Write(") != -1 :
        calc = str(line)[6:len(str(line))-1]
        result = "error, faulty equation!"
        if(calc in variables.keys()):
            result = variables[calc]
        else:
            calc = calc.split(" ")
            if (calc[1] == "+"):
                result = int(calc[0]) + int(calc[2])
            elif (calc[1] == "-"):
                result = int(calc[0]) - int(calc[2])
            elif (calc[1] == "*"):
                result = int(calc[0]) * int(calc[2])
            elif (calc[1] == "/"):
                result = int(calc[0]) / int(calc[2])
            elif (calc[1] == "^"):
                result = int(calc[0]) ** int(calc[2])
        print(result)
    elif "ifequal" in line:
        lineForWork = line[len("if"):].split("[")[1].split(",")
        if (int(variables[lineForWork[0]]) == int(lineForWork[1])):
            execodeline(lineForWork[2][1:len(lineForWork[2])-1])
    elif "ifless" in line:
        lineForWork = line[len("if"):].split("[")[1].split(",")
        if (int(variables[lineForWork[0]]) < int(lineForWork[1])):
            execodeline(lineForWork[2][1:len(lineForWork[2])-1])
    elif line[:len(line)-2] in variables.keys() and "++" in line:
        variables[line[:len(line)-2]] = int(variables[line[:len(line)-2]]) + 1
    elif line[:len(line)-2] in variables.keys() and "-" in line:
        variables[line[:len(line)-2]] = int(variables[line[:len(line)-2]]) - 1
    elif line in funcs.keys():
        #print(funcs[line])
        for cmd in funcs[line]:
            execodeline(cmd)
    elif "Clear()" in line:
        clear()
    elif line == "":
        pass
    elif "import" in line:
        print("import can only happen at definition level(outside of function), keep that in mind.")
    else:
        print("." + line + ".")
        print("No program called " + line + " assuming it is okay")
        
execode()
