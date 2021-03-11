import os
def OpenFile(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

def Write(path, text):
    file = open(path, "w")
    file.write(text)
    file.close()

def Exists(path):
    os.path.isfile(path)