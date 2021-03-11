import tkinter
import tkinter.filedialog as tkFileDialog
import highlighter
import tkinter.font as TkFont
from tkinter import ttk
import os

filename = ""
settings = True
def open_settings():
    settingsMenu = tkinter.Tk()
    settingsMenu.geometry("800x800")
    settingsMenu.title("EZlang IDE - Settings")
    bar = ttk.Notebook(settingsMenu)
    general = ttk.Frame(bar)

    #General Settings
    tkinter.Label(general, text="BETA OPTIONS, SOME ARE JUST PLACEHOLDERS!").pack()
    autoUpdate = tkinter.Checkbutton(general, text="Enable Auto Updating", onvalue=True, offvalue=False)
    autoUpdate.pack()


    apperance = ttk.Frame(bar)
    bar.add(general, text='General Settings')
    bar.add(apperance, text='Apperance')
    bar.pack(expand=1, fill="both")
    while settings:
        settingsMenu.update()
        settingsMenu.update_idletasks()

def new():
    global text
    global filename
    set_input("program\n{\n    use system;\n    system.Write(\"Hello\\c World!\");\n}", text)
    filename = ""

def set_input(value, text):
    text.delete('1.0', tkinter.END)
    text.insert("end", value)
    
def saveas():
    global text
    global filename
    t = text.get("1.0", "end-1c")
    filename=tkFileDialog.asksaveasfilename(title="Save file, note: will be saved as .ez")
    filename = filename if ".ez" in filename else filename + ".ez"
    file1=open(filename, "w+")
    file1.write(t)
    file1.close()

def save():
    if (filename == ""):
        saveas()
    t = text.get("1.0", "end-1c")
    file1=open(filename, "w+")
    file1.write(t)
    file1.close()

def run():
    save()
    os.system("python interpreter/ezlang.pyw " + filename)

def openF():
    global text
    global filename
    filename=tkFileDialog.askopenfilename(title="Open file")
    file1=open(filename, "r").read()
    set_input(file1, text)
    root.title("EZlang IDE - " + filename)

def runKey(event):
    run()

def openKey(event):
    openF()

def saveKey(event):
    save()

def newKey(event):
    new()

def GetLibs():
    textToUse = text.get(1.0, tkinter.END)
    returnValue = []
    for retVal in textToUse.split("use ")[1:]:
        vals = retVal.split(";")[0]
        #print("return "+ vals)
        returnValue.append(vals)
    return returnValue

def GetComments():
    textToUse = text.get(1.0, tkinter.END)
    returnValue = []
    for retVal in textToUse.split("//")[1:]:
        vals = retVal.split(";")[0]
        #print("return "+ vals)
        returnValue.append(vals)
    return returnValue

def GetSecond(list):
    retVal = []
    for i in range(1, len(list), 2):
        retVal.append(list[i])
    return retVal

def GetStrings():
    textToUse = GetSecond(text.get(1.0, tkinter.END).split("\""))
    #print(textToUse)
    returnValue = []
    for retVal in textToUse:
        vals = "\"" + retVal + "\""
        returnValue.append(vals)
    return returnValue
root = tkinter.Tk()
root.title("EZlang IDE")
text = highlighter.CustomText(root)
text.config(bg="black",fg="grey",insertbackground="white",font=("Courier", 16, "normal"))
font = TkFont.Font(font=text['font'])
tab = font.measure('    ')
text.insert("1.0", "program\n{\n    use system;\n    system.Write(\"Hello\\c World!\");\n}") 
text.config(tabs=tab)
menubar = tkinter.Menu(root)
root.config(menu=menubar)
text.place(x=0,y=0, anchor="nw", relwidth=1.0, relheight=1.0)
fileMenu = tkinter.Menu(menubar)
rectMenu = tkinter.Menu(menubar)
config = tkinter.Menu(menubar)
window = tkinter.Menu(config)
theme = tkinter.Menu(window)
rectMenu.add_command(label='Run', command=run)
fileMenu.add_command(label="New", underline=0, command=new)
fileMenu.add_command(label="Settings", underline=0, command=open_settings)
fileMenu.add_command(label="Save", underline=0, command=save)
fileMenu.add_command(label="Open", underline=0, command=openF)
fileMenu.add_command(label="Save As", underline=0, command=saveas)
fileMenu.add_command(label="Quit", underline=0, command=quit)
menubar.add_cascade(label="File", underline=0, menu=fileMenu)
menubar.add_cascade(label="EZlang", underline=0, menu=rectMenu)
root.bind_all('<Control-s>', saveKey)
root.bind_all('<Control-o>', openKey)
#root.bind_all('<Control-n>', newKey)
root.bind("<F5>", runKey)
root.bind_all('<F4>', quit)
root.geometry("800x500")
while True:
    highlighter.UpdatePatterns(text)
    root.update()
    root.update_idletasks()
    highlighter.Patterns.libraries = GetLibs()
    highlighter.Patterns.comments = GetComments()
    highlighter.Patterns.strings = GetStrings()
