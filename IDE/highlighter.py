import tkinter as tk

def pos(text, pos):
    text = text.get(1.0, tk.END)
    line = 0
    lastLine = 0
    for i in range(pos):
        if (text[i] == "\n"):
            line += 1
            lastLine = i
    return str(line) + "." + str(pos - lastLine)

class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)

        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")
    def highlight_first(self, pattern, tag, start="1.0", end="end"):
        start = self.index(start)
        end = self.index(end)
        startPos = str(self.get(1.0, end)).find(pattern)
        self.tag_add(tag, pos(self, startPos), pos(self, startPos + len(pattern)))


    def highlight_pattern_between(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''
        if (len(getindexes(pattern, self.get(1.0, tk.END))) > 1):
            start = self.index(str(float(getindexes(pattern, self.get(1.0, tk.END))[0])))
            end = self.index(str(float(getindexes(pattern, self.get(1.0, tk.END))[1])))

            #print(start, end)

            self.mark_set("matchStart", start)
            self.mark_set("matchEnd", start)
            self.mark_set("searchLimit", end)

            count = tk.IntVar()
            while True:
                index = self.search(pattern, "matchEnd","searchLimit",
                                    count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.mark_set("matchStart", index)
                self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.tag_add(tag, "matchStart", "matchEnd")

def getindexes(char, text):
    indexed = []
    for i in range(len(text)):
        if text[i] == char:
            indexed.append(i)
    return indexed

class Patterns:
    keywords = ["statement", "function", "program", "use", "return", "include", "Congratulations! you found the sacret and secret highlighted piece of text! Screenshot and send it to me and i will reward you with anything"]
    types = ["num", "string"]
    libraries = []
    comments = []
    strings = []
    numerics = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def UpdatePatterns(text):
    for tag in text.tag_names():
        text.tag_remove(tag, "1.0", "end")
    #Defining colors
    text.tag_configure("grey", foreground="#AAAAAA")
    text.tag_configure("blue", foreground="#0000FF")
    text.tag_configure("orange", foreground="#FFA500")
    text.tag_configure("red", foreground="#FF0000")
    text.tag_configure("dark red", foreground="#AA0000")
    text.tag_configure("purple", foreground="#800080")
    #Patterns in Patterns class
    for pattern in Patterns.comments:
        text.highlight_pattern(pattern, "purple")
    for pattern in Patterns.strings:
        text.highlight_pattern(pattern, "red")
    for pattern in Patterns.keywords:
        text.highlight_pattern(pattern, "red")
    for pattern in Patterns.numerics:
        text.highlight_pattern(pattern, "blue")
    for pattern in Patterns.types:
        text.highlight_pattern(pattern, "blue")
    for pattern in Patterns.strings:
        text.highlight_pattern(pattern, "red")
    for pattern in Patterns.libraries:
        text.highlight_pattern(pattern, "orange")
    for pattern in Patterns.strings:
        text.highlight_pattern(pattern, "red")
    for pattern in Patterns.comments:
        text.highlight_pattern(pattern, "purple")

    #special cases
    text.highlight_first("ah", "purple")
    text.highlight_pattern(";", "grey")
    text.highlight_pattern(",", "grey")
    text.highlight_pattern("//", "purple")
    text.highlight_pattern("\\c", "dark red")
    text.highlight_pattern("\\n", "dark red")
    text.highlight_pattern("\\t", "dark red")
    #text.highlight_pattern_between('a', "red")
    #text.highlight_pattern("\"", "red")