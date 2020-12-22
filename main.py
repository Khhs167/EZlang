import sys
import math
import os
import time
from tkinter import *
import tkinter.filedialog as tkFileDialog
from tkinter import colorchooser

from tkinter import messagebox

import string as stringmod
import urllib
import urllib.request

class Splash(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("Splash")

        ## required to make window show before the program gets to the mainloop
        self.update()

def center_window(window, w, h):
    # get screen width and height
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))



root=Tk("Text Editor")
root.withdraw()
root.title("EZlang IDE")
root.geometry("1600x800")

center_window(root, 1600, 800)

splash = Splash(root)
splash.overrideredirect(1)
splash.geometry("800x800")
canvas = Canvas(splash, width = 800, height = 800)      
canvas.pack()      
img = PhotoImage(file="logo.png")      
canvas.create_image(0,0, anchor=NW, image=img)      
center_window(splash, 800, 800)
splash.update()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

scheme = open("colorscheme.sch", "r").read().split("\\")

text=Text(root, font=("Helvetica", 15), bg=scheme[0], foreground=scheme[1], insertbackground='white')

filename = ""

border = True
ismax = False
darkmode = True
fullscreen = False

def update():
    print("Updating...")
    url = "https://raw.githubusercontent.com/Khhs167/EZlang/main/ezcode.py"
    file = urllib.request.urlopen(url)
    endfile = ""
    for line in file:
            decoded_line = line.decode("utf-8")[:len(line.decode("utf-8"))-1]
            #print("." + decoded_line + ".")
            endfile += decoded_line
    open("ezcode.py", "w+").write(endfile)
    print("Updated!")

def set_input(value, text):
    text.delete(1.0, "end")
    text.insert("end", value)

def new():
    global text
    global filename
    set_input("", text)
    filename = ""
    
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

def saveKey(event):
    save()

def openF():
    global text
    global filename
    filename=tkFileDialog.askopenfilename(title="Open file")
    file1=open(filename, "r").read()
    set_input(file1, text)

def openKey(event):
    openF()

def run():
    save()
    os.system("cd " + os.getcwd() + " & " + "python ezcode.py " + filename)

def runKey(event):
    run()

def border():
    global border
    if (border):
        border = False
        root.overrideredirect(1)
    else:
        border = True
        root.overrideredirect(0)

def darkMode():
    global darkmode
    if (darkmode):
        darkmode = False
        text.config(bg=scheme[2], fg=scheme[3], insertbackground='black')
    else:
        darkmode = True
        text.config(bg=scheme[0], fg=scheme[1], insertbackground='white')

def about():
    endfile = open("ezcode.py", "r").readlines()[0][1:len(open("ezcode.py", "r").readlines()[0])-1]
    messagebox.showinfo(title="About EZlang IDE", message="\"EZlang Intergrated Development Enviroment\" - v2.2 \nRunning EZlang verison " + endfile + "\n###Made by kGames###")

def fullscreenC():
    global root
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)


def saveScheme():
    darkMode()
    darkMode()
    schemeWrite = open("colorscheme.sch", "w")
    schemeToWrite = scheme[0] + "\\" + scheme[1] + "\\" + scheme[2] + "\\" + scheme[3] + "\\"
    schemeWrite.write(schemeToWrite)

def darkbg():
    scheme[0] = colorchooser.askcolor(title ="Choose background")[1]
    saveScheme()
def darkfg():
    scheme[1] = colorchooser.askcolor(title ="Choose text color")[1]
    saveScheme()
def lightbg():
    scheme[2] = colorchooser.askcolor(title ="Choose background")[1]
    saveScheme()
def lightfg():
    scheme[3] = colorchooser.askcolor(title ="Choose text color")[1]
    saveScheme()

menubar = Menu(root)
root.config(menu=menubar)

fileMenu = Menu(menubar)
rectMenu = Menu(menubar)
config = Menu(menubar)
window = Menu(config)
theme = Menu(window)
rectMenu.add_command(label='Run', command=run)
rectMenu.add_command(label='Update', command=update)
rectMenu.add_command(label='About', command=about)
window.add_command(label="Toggle Border", command=border)
window.add_command(label="Toggle Dark Mode", command=darkMode)
window.add_command(label="Toggle fullscreen", command=fullscreenC)
config.add_cascade(label="Window", underline=0, menu=window)
theme.add_cascade(label="Darkmode background", underline=0, command=darkbg)
theme.add_cascade(label="Darkmode text", underline=0, command=darkfg)
theme.add_cascade(label="Lightmode background", underline=0, command=lightbg)
theme.add_cascade(label="Lightmode text", underline=0, command=lightfg)
window.add_cascade(label="Theme", underline=0, menu=theme)
fileMenu.add_command(label="New", underline=0, command=new)
fileMenu.add_command(label="Save", underline=0, command=save)
fileMenu.add_command(label="Open", underline=0, command=openF)
fileMenu.add_command(label="Save As", underline=0, command=saveas)
fileMenu.add_command(label="Quit", underline=0, command=quit)
menubar.add_cascade(label="File", underline=0, menu=fileMenu)
menubar.add_cascade(label="EZlang", underline=0, menu=rectMenu)
menubar.add_cascade(label="Configure", underline=0, menu=config)



text.place(relwidth=1.0, relheight=1.0)

root.bind_all('<Control-s>', saveKey)
root.bind_all('<Control-o>', openKey)
root.bind("<F5>", runKey)
root.bind_all('<F4>', quit)

## simulate a delay while loading
time.sleep(1)

## finished loading so destroy splash
splash.destroy()

## show window again
root.deiconify()

root.mainloop()
