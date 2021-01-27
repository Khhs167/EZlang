import tkinter
import tkinter.filedialog as tkFileDialog
import highlighter
import tkinter.font as TkFont
import os

filename = ""

def new():
    global text
    global filename
    set_input("1.0", "program\n{\n    use system;\n    system.Write(\"Hello\\c World!\");\n}")
    filename = ""

def set_input(value, text):
    text.insert(1.0, )
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
    os.system("cd " + os.getcwd() + " & cd .. & python interpreter/ezlang.py " + filename)

def openF():
    global text
    global filename
    filename=tkFileDialog.askopenfilename(title="Open file")
    file1=open(filename, "r").read()
    set_input(file1, text)

def runKey(event):
    run()

def openKey(event):
    openF()

def saveKey(event):
    save()

def newKey(event):
    new()


root = tkinter.Tk()

text = highlighter.CustomText(root)
text.config(bg="black",fg="grey",insertbackground="white",font=("Courier", 16, "normal"))
font = TkFont.Font(font=text['font'])
tab = font.measure('    ')
text.insert("1.0", "program\n{\n    use system;\n    system.Write(\"Hello\\c World!\");\n}") 
text.config(tabs=tab)

text.pack(expand=True, fill='both')

menubar = tkinter.Menu(root)
root.config(menu=menubar)

fileMenu = tkinter.Menu(menubar)
rectMenu = tkinter.Menu(menubar)
config = tkinter.Menu(menubar)
window = tkinter.Menu(config)
theme = tkinter.Menu(window)
rectMenu.add_command(label='Run', command=run)
#fileMenu.add_command(label="New", underline=0, command=new)
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

while True:
    highlighter.UpdatePatterns(text)
    root.update()
    root.update_idletasks()
