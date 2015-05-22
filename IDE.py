from tkFileDialog import *
from tkMessageBox import *
from tkSimpleDialog import *
from Tkinter import *
from PIL import Image, ImageTk
import Syntax

START = '1.0'
SEL_FIRST = SEL + '.first'
SEL_LAST = SEL + '.last'
        

class GUI():
        UPDATE = 100
        editors = []
        updateId = None
        
        def __init__(self):
                self.__class__.editors.append(self)

                self.lineNumbers = ''
                self.nomore = False
                
                self.root = Tk()

                self.displaySplash()
                self.createWidgets()


                self.root.mainloop()
                

        def displaySplash(self):
                self.root.overrideredirect(True)
                w = 720
                h = 450

                width = self.root.winfo_screenwidth()
                height = self.root.winfo_screenheight()

                posx = (width/2) - (w/2)
                posy = (height/2) - (h/2)

                self.root.geometry('%dx%d+%d+%d' % (w, h, posx, posy))

                image_file = Image.open("splash.png")
                image_file = image_file.resize((w,h), Image.ANTIALIAS)
                splash = ImageTk.PhotoImage(image_file)

                label = Label(self.root, image = splash)
                label.pack()
                self.root.after(1000, self.root.destroy)

                self.root.mainloop()

        def createWidgets(self):
                self.root = Tk()
                self.root.geometry("800x600")
                self.root.title("PrismX")
                self.root.wm_iconbitmap("prismicon.ico")
                
                menubar = Menu(self.root)

                filemenu = Menu(menubar, tearoff=0)
                filemenu.add_command(label = "New", command = self.new, accelerator = "Ctrl+N")
                filemenu.add_command(label="Open", command=self.open, accelerator = "Ctrl+O")
                filemenu.add_command(label="Save", command=self.save, accelerator = "Ctrl+S")
                filemenu.add_command(label = "Save As...", command = self.saveAs, accelerator = "Ctrl+Shift+S")
                filemenu.add_separator()
                filemenu.add_command(label="Exit", command=self.exit, accelerator = "Ctrl+Q")
                menubar.add_cascade(label="File", menu=filemenu)

                editmenu = Menu(menubar, tearoff = 0)
                editmenu.add_command(label = "Undo", command = self.undo, accelerator = "Ctrl+Z")
                editmenu.add_command(label= "Redo", command = self.redo, accelerator = "Ctrl+Shift+Z")
                editmenu.add_separator()
                editmenu.add_command(label = "Cut", command = self.cut, accelerator = "Ctrl+X")
                editmenu.add_command(label = "Copy", command = self.copy, accelerator = "Ctrl+C")
                editmenu.add_command(label = "Paste", command = self.paste, accelerator = "Ctrl+V")
                editmenu.add_command(label = "Delete", command = self.delete, accelerator = "DEL")
                editmenu.add_command(label = "Select All", command = self.selectAll, accelerator = "Ctrl+A")
                menubar.add_cascade(label = "Edit", menu = editmenu)

                searchmenu = Menu(menubar, tearoff = 0)
                searchmenu.add_command(label = "Go to...", command = self.goTo, accelerator = "Ctrl+G")
                searchmenu.add_command(label = "Find...", command = self.findGui, accelerator = "Ctrl+F")
                searchmenu.add_command(label = "Replace...", command = self.replace, accelerator = "Ctrl+R")
                menubar.add_cascade(label = "Search", menu = searchmenu)
                
                compilemenu = Menu(menubar, tearoff=0)
                compilemenu.add_command(label="Compile", command=self.check, accelerator = "F4")
                compilemenu.add_command(label="Compile and Run", command=self.run, accelerator = "F5")
                menubar.add_cascade(label="Compile", menu=compilemenu)

                self.root.config(menu = menubar)

                self.lineNum = Text(self.root,
                                    width = 4,
                                    padx = 4,
                                    highlightthickness = 0,
                                    takefocus = 0,
                                    bd = 0,
                                    background = 'lightgrey',
                                    state = 'disabled')



                
                self.lineNum.pack(side = LEFT, fill = Y)
                self.text = Text(self.root,
                                 width = 16,
                                 bd = 0,
                                 padx = 4,
                                 undo = True,
                                 background = 'white')
                
                self.text.pack(side=LEFT, fill=BOTH, expand=YES)

                scroll = Scrollbar(self.root, orient=VERTICAL, command=self.text.yview)
                scroll.pack(side=RIGHT, fill=Y)

                self.text["yscrollcommand"] = scroll.set


                self.text.bind("<Control-n>", self.dispNew)
                self.text.bind("<Control-o>", self.dispOpen)
                self.text.bind("<Control-s>", self.dispSave)
                self.text.bind("<Control-Shift-S>", self.dispSaveAs)
                self.text.bind("<Control-q>", self.dispExit)
                self.text.bind("<Control-z>", self.dispUndo)
                self.text.bind("<Control-Shift-Z>", self.dispRedo)
                self.text.bind("<Control-x>", self.dispCut)
                self.text.bind("<Control-c>", self.dispCopy)
                self.text.bind("<Control-v>", self.dispPaste)
                self.text.bind("<Delete>", self.dispDelete)
                self.text.bind("<Control-a>", self.dispSelectAll)
                self.text.bind("<Control-g>", self.dispGoTo)
                self.text.bind("<Control-f>", self.dispFind)
                self.text.bind("<Control-r>", self.dispReplace)
                self.text.bind("<F4>", self.dispCompile)
                self.text.bind("<F5>", self.dispCompileRun)
                
                if self.__class__.updateId is None:
                        self.updateAllNum()
                
        #File menu commands
        def new(self):
                choice = self.isEmpty() or askyesno('PrismX', 'Disregard text?')

                if choice:
                        self.setFileName(None)
                        self.root.title("PrismX")
                        self.clearText()

        def open(self):
                choice = self.isEmpty() or askyesno('PrismX', 'Disregard text?')
                if choice:
                        file = askopenfilename()

                        if file:
                                text = open(file, 'r').read()
                                try:
                                        open(file, 'r').read()
                                except:
                                        showerror('PrismX', 'Could not open file ' + file)
                                else:
                                        self.setText(text)
                                        self.setFileName(file)
        

        def save(self):
                self.saveAs()

        
        def saveAs(self):
                file = asksaveasfilename()
                if file:
                        text = self.getText()

                        try:
                                open(file, 'w').write(text)
                        except:
                                showerror('PrismX', 'Could not write file ' + file)
                        else:
                                self.setFileName(file)
        def exit(self):
                if askyesno('PrismX', 'Quit?'):
                        self.root.destroy()
                                
        #Edit menu commands
        def undo(self):
                self.text.edit_undo()

        def redo(self):
                self.text.edit_redo()

        def cut(self):
                self.copy()
                self.delete()

        def copy(self):
                self.root.clipboard_clear()
                text = self.text.get(SEL_FIRST, SEL_LAST)
                
                self.root.clipboard_append(text)

        def paste(self):
                text = self.text.selection_get(selection = 'CLIPBOARD')
                self.text.insert(INSERT, text)

        def delete(self):
                self.text.delete(SEL_FIRST, SEL_LAST)

        def selectAll(self):
                self.text.tag_add(SEL, '1.0', END + '-1c')
                self.text.mark_set(INSERT, '1.0')
                self.text.see(INSERT)

        #Search menu commands

        def goTo(self):
                linenum = askinteger('PrismX', 'Go to line: ')
                self.text.update()
                self.text.focus()
                if linenum is not None:
                        maxin = self.text.index(END+'-1c')
                        maxln = int(maxin.split('.')[0])
                        if linenum > 0 and linenum <= maxln:
                                self.text.mark_set(INSERT, '%d.0' % linenum)
                                self.text.tag_remove(SEL, '1.0', END)
                                self.text.tag_add(SEL, INSERT, 'insert+1l')
                                self.text.see(INSERT)

        def findGui(self):
                findwin = Toplevel(self.root)
                Label(findwin, text = "Find what: ").grid(pady = 5, row = 0, column = 0, sticky = N+E+W+S)
                self.findstring = Entry(findwin)
                self.findstring.grid(pady = 5, row = 0, column = 1, sticky = N+E+W+S)
                Button(findwin, text = "Find", command = self.find).grid(pady = 2, row = 1, column = 0, sticky = EW)
               # Button(findwin, text = "Find Next", command = self.findAll).grid(pady = 2, row = 1, column = 1, sticky = EW)
                Button(findwin, text = "Find All", command = self.findAll).grid(pady = 2, row = 1, column = 1, sticky = EW)
                findwin.resizable(0,0)            

        def find(self, pastInput = None):
                key = pastInput or self.findstring.get()
                #self.text.update()
                #self.text.focus()
                self.lastInput = key

                if key:
                        #self.selectAll()
                        loc = self.text.search(key, INSERT, END)
                        if not loc:
                                self.nomore = True
                        else:
                                self.selectAll()
                                inputB4 = loc + '+%dc' % len(key)
                                self.text.tag_remove(SEL, '1.0', END)
                                self.text.tag_add(SEL, loc, inputB4)
                                self.text.mark_set(INSERT, inputB4)
                                self.text.see(loc)
                                self.text.focus()
    

        def findAll(self):
                key = self.findstring.get()
                self.lastInput = key
                count = 0
                
                if key:
                        while True:
                                loc = self.text.search(key, INSERT, END)
                                if not loc:
                                        break
                                else:
                                        count += 1
                                        inputB4 = loc + '+%dc' % len(key)
                                        #self.text.tag_remove(SEL, '1.0', END)
                                        self.text.tag_add(SEL, loc, inputB4)
                                        self.text.mark_set(INSERT, inputB4)
                                        self.text.see(loc)
                                        self.text.focus()
                      

        def replace(self):
                replacewin = Toplevel(self.root)
                Label(replacewin, text = "Find what: ").grid(row = 0, column = 0)
                Label(replacewin, text = "Replace with: ").grid(row = 1, column = 0)
                self.findstr = Entry(replacewin)
                self.replacestr = Entry(replacewin)
                self.findstr.grid(row = 0, column = 1, sticky = EW)
                self.replacestr.grid(row = 1, column = 1, sticky = EW)
                Button(replacewin, text = 'Find', command = self.doFind).grid(padx = 2, row = 0, column = 2, sticky = EW)
                Button(replacewin, text = 'Replace', command = self.doReplace).grid(padx = 2, row = 1, column = 2, sticky = EW)
                Button(replacewin, text = 'Replace All', command = self.replaceAll).grid(padx = 2, row = 2, column = 2, sticky = EW)
                replacewin.resizable(0,0) 

        def doFind(self):
                self.find(self.findstr.get())
                

        def doReplace(self):
                if self.text.tag_ranges(SEL):
                        self.text.delete(SEL_FIRST, SEL_LAST)
                        self.text.insert(INSERT, self.replacestr.get())
                        self.text.see(INSERT)
                        self.doFind()
                        self.text.update()

        def replaceAll(self):
                while self.nomore != True:
                        self.text.delete(SEL_FIRST, SEL_LAST)
                        self.text.insert(INSERT, self.replacestr.get())
                        self.text.see(INSERT)
                        self.doFind()
                        self.text.update()
                        
        #Compile Menu commands

        def check(self):
                self.save()
#                temp = Syntax.syntax()
 #               temp.set_input(self.text.get(1.0, END))
  #              temp.algorithm()

        def run(self):
                self.save()

        #Etc
        def isEmpty(self):
                return not self.getText()

        def getText(self):
                return self.text.get('1.0', END+'-1c')

        def setText(self, text):
                self.text.delete('1.0', END)
                self.text.insert(END, text)
                self.text.mark_set(INSERT, '1.0')
                self.text.see(INSERT)

        def clearText(self):
                self.text.delete('1.0', END)

        def getFileName(self):
                return self.file

        def setFileName(self, name):
                self.file = name
                self.root.title(name)


        def getLineNum(self):
                x = 0
                ln = '0'
                col = ''
                line = ''

                lnMask = '      %s\n'
                inMask = '@0, %d'

                for i in range(0, self.text.winfo_height(), 1):
                        ll, cc = self.text.index(inMask % i).split('.')

                        if ln == ll:
                                if col != cc:
                                        col = cc
                                        line += "\n"
                        else:
                                ln, col = ll, cc
                                line += (lnMask % ln)[-5:]

                return line

        def updateLineNumbers(self):
                tt = self.lineNum
                ln = self.getLineNum()
                if self.lineNumbers != ln:
                    self.lineNumbers = ln
                    tt.config(state='normal')
                    tt.delete('1.0', END)
                    tt.insert('1.0', self.lineNumbers)
                    tt.config(state='disabled')
        
        def updateAllNum(cls):
                if len(cls.editors) < 1:
                        cls.updateId = None
                        return
                for ed in cls.editors:
                        ed.updateLineNumbers()

                cls.updateId = ed.text.after(cls.UPDATE, cls.updateAllNum)

        
        #Dispatcher Functions
        def dispNew(self, event = None):
                self.new()
                return "break"

        def dispOpen(self, event = None):
                self.open()
                return "break"

        def dispSave(self, event = None):
                self.save()
                return "break"

        def dispSaveAs(self, event = None):
                self.saveAs()
                return "break"

        def dispExit(self, event = None):
                self.exit()
                return "break"

        def dispUndo(self, event = None):
                self.undo()
                return "break"

        def dispRedo(self, event = None):
                self.redo()
                return "break"

        def dispCut(self, event = None):
                self.cut()
                return "break"

        def dispCopy(self, event = None):
                self.copy()
                return "break"

        def dispPaste(self, event = None):
                self.paste()
                return "break"

        def dispDelete(self, event = None):
                self.delete()
                return "break"

        def dispSelectAll(self, event = None):
                self.selectAll()
                return "break"

        def dispGoTo(self, event = None):
                self.goTo()
                return "break"

        def dispFind(self, event = None):
                self.findGui()
                return "break"

        def dispReplace(self, event = None):
                self.replace()
                return "break"

        def dispCompile(self, event = None):
                self.check()
                return "break"

        def dispCompileRun(self, event = None):
                self.run()
                return "break"
                
ed = GUI()
