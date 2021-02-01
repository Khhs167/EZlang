import os
def Write(text):
    print(text)

def Input():
    return input()

def Ask(question):
    return input(question)

def MergeString(string1, string2):
    return str(string1) + str(string2)

def AddInt(a, b):
    return int(a) + int(b)

def Clear():
    if (os.name == "nt"):
        os.system("cls")
    else:
        os.system("clear")

def Help():
    print('''
    EZlang System Library
    A built in library for basic I/O and maths.
    Feel free to edit system.py
    ''')