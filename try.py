from tkFileDialog import *
from tkMessageBox import *
from tkSimpleDialog import *
from Tkinter import *
from PIL import Image, ImageTk
import Syntax
import ply.lex as lex
from random import randint
import ply.yacc as yacc

warningCounts = 0
remainder = 0
datatypes = ["boolean", "string", "int", "float"]
listNum = []



#========================================================
def p_statementTop(p):
  '''statementTop : END
                  | statement'''

# # # # # # # # # C Y A N # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def p_statement(p):
    '''statement : declaration statementTop
                | expression statementTop
                | IfThenElse statementTop
                | AssignmentHead statementTop
                | WhileLoop statementTop
                | ForLoop statementTop
                | typeCastToInt statementTop
                | typecastToFloat statementTop
                | FunctionDefinition statementTop
                | FunctionCall statementTop
                | returnDec statementTop
                | stringOpStatement statementTop
                | listOPStatement statementTop
                | READ LPAREN IDENTIFIER RPAREN SEMICOLON statementTop
                | PRINT LPAREN content RPAREN SEMICOLON statementTop'''              

                # | DoWhileLoop statementTop
                #| unionAdd statementTop
                #| unionKeys statementTop
                #
                #
def p_statement1(p):
    '''statement1 : declaration
                | expression
                | IfThenElse
                | AssignmentHead
                | WhileLoop
                | ForLoop
                | typeCastToInt
                | typecastToFloat
                | FunctionDefinition
                | FunctionCall
                | returnDec
                | stringOpStatement
                | listOPStatement statementTop
                | READ LPAREN IDENTIFIER RPAREN SEMICOLON
                | PRINT LPAREN content RPAREN SEMICOLON'''
                #| DoWhileLoop
                #| unionAdd
                #| unionKeys

def p_content(p):
    '''content : toPrint morePrint'''

def p_morePrint(p):
    '''morePrint : PLUS toPrint morePrint
                | EMPTY'''

def p_toPrint(p):
    '''toPrint : STRINGVALUE
              | CONSTANT
              | IDENTIFIER'''

def p_declaration(p):
    '''declaration : identifierDeclaration
                  | listDec'''
#                  | unionDec'''

def p_identifierDeclaration(p):
    '''identifierDeclaration : BAR dataType IDENTIFIER BAR SEMICOLON
                            | BAR dataType IDENTIFIER LBRACK CONSTANT RBRACK BAR SEMICOLON
                            | BAR dataType IDENTIFIER LBRACK CONSTANT RBRACK EQUAL expression BAR SEMICOLON
                            | BAR dataType IDENTIFIER EQUAL expression BAR SEMICOLON'''

def p_dataType(p):
  '''dataType : INT
            | BOOLEAN
            | FLOAT'''

def p_stringOPStatement(p):
    '''stringOpStatement : IDENTIFIER stringOp LPAREN STRING RPAREN SEMICOLON
                        | IDENTIFIER stringOp LPAREN IDENTIFIER RPAREN SEMICOLON'''


def p_listOPStatement(p):
    '''listOPStatement : IDENTIFIER INSERT LPAREN CONSTANT COMMA validListUnionValues RPAREN SEMICOLON
                        | IDENTIFIER POP LPAREN listOpChoice RPAREN SEMICOLON'''

def p_listOpChoice(p):
    '''listOpChoice : CONSTANT
                    | EMPTY'''

def p_stringOp(p):
    '''stringOp : SPLIT
                | STRIP 
                | CONCAT
                | COPY'''

def p_listDec(p):
    '''listDec : BAR IDENTIFIER EQUAL list BAR SEMICOLON'''

def p_list(p):
    '''list : LBRACK listElem RBRACK'''

def p_listElem(p):
    '''listElem : validListUnionValues
                | validListUnionValues COMMA listElem
                | EMPTY'''

def p_listEval(p):
    '''listEval : IDENTIFIER LISTVALUE'''

def p_unionDec(p):
    '''unionDec : IDENTIFIER EQUAL union SEMICOLON'''

def p_union(p):
    '''union : LCURLY unionElement RCURLY'''

def p_unionElement(p):
    '''unionElement : STRING EQUAL validListUnionValues
                  | STRING EQUAL validListUnionValues COMMA unionElement
                  | EMPTY'''

#def p_unionAdd(p):
#    '''unionAdd : IDENTIFIER LBRACK STRINGVALUE RBRACK EQUAL validListUnionValues SEMICOLON'''

def p_validListUnionValues(p):
    '''validListUnionValues : CONSTANT
                          | FLOATVALUE
                          | booleanValue
                          | STRINGVALUE
                          | LISTVALUE'''

#def p_unionKeys(p):
#    '''unionKeys : IDENTIFIER KEYS SEMICOLON'''

#def p_unionEval(p):
#    '''unionEval : IDENTIFIER ARROW STRING'''

def p_typeCastToInt(p):
    '''typeCastToInt : TC_INT IDENTIFIER SEMICOLON'''

def p_typeCastToFloat(p):
    '''typecastToFloat : TC_FLOAT IDENTIFIER SEMICOLON'''

def p_WhileLoop(p):
    '''WhileLoop : WHILE Condition COLON Body'''

def p_Body(p):
    '''Body : statementMore'''

def p_statementMore(p):
    '''statementMore : statementMoreCont
                    | END'''

def p_statementMoreCont(p):
    '''statementMoreCont : statement1 statementMore'''

def p_ForLoop(p):
    '''ForLoop : for LPAREN AssignmentHead Condition Increment RPAREN Body'''

#def p_DoWhileLoop(p):
#    '''DoWhileLoop : DO COLON Body WHILE Condition SEMICOLON'''

def p_Increment(p):
    '''Increment : SEMICOLON Operand Options'''

def p_Options(p):
    '''Options : Iterator
              | AssignmentOperator Operand'''

def p_IfThenElse(p):
    '''IfThenElse : IF Condition Body addElif'''

def p_addElif(p):
    '''addElif : addElif2
              | FI
              | ELSE Body'''

def p_addElif2(p):
    '''addElif2 : elifClause addElif'''

def p_elifClause(p):
    '''elifClause : ELIF Condition Body'''

def p_Condition(p):
    '''Condition : RelationExpression
                | LPAREN Condition Compound Condition RPAREN
                | LPAREN NOT Condition RPAREN'''

def p_Operand(p):
    '''Operand : IDENTIFIER
              | CONSTANT
              | booleanValue
              | LISTVALUE'''

def p_Compound(p):
    '''Compound : AND
              | OR'''

def p_Iterator(p):
    '''Iterator : PLUSPLUS
              | MINUSMINUS
              | EMPTY'''

def p_AssignmentHead(p):
    '''AssignmentHead : BAR IDENTIFIER AssignmentOption BAR SEMICOLON'''

def p_AssignmentOption(p):
    '''AssignmentOption : EQUAL AssignmentOptionChain
                      | AssignmentOperator AssignmentOptions2'''

def p_AssignmentOptions2(p):
    '''AssignmentOptions2 : CONSTANT
                        | ArithmeticExpression'''

def p_AssignmentOptionChain(p):
    '''AssignmentOptionChain : listEval
                              | IDENTIFIER
                              | Function
                              | AssignmentOptions2'''
    #                         | unionEval

def p_AssignmentOperator(p):
    '''AssignmentOperator : PLUSEQUAL
                        | MINUSEQUAL
                        | MULTEQUAL
                        | DIVEQUAL
                        | MODEQUAL'''

def p_expression(p):
    '''expression : ArithmeticExpression
                  | listEval
                  | list
                  | union
                  | RelationExpression'''

def p_RelationExpression(p):
    '''RelationExpression : LPAREN Operand RelationOperator Operand RPAREN'''

def p_ArithmeticExpression(p):
    '''ArithmeticExpression : LESSTHAN Operand ArithmeticOperator Operand GREATERTHAN'''

def p_ArithmeticOperator(p):
    '''ArithmeticOperator : PLUS
                          | MINUS
                          | MULT
                          | DIV
                          | MOD'''

def p_RelationOperator(p):
    '''RelationOperator : EQUALEQUAL
                        | EQUAL
                        | LESSTHAN
                        | GREATERTHAN
                        | GREATEREQ
                        | LESSEREQ
                        | NOTEQ'''

def p_FunctionDefinition(p):
    '''FunctionDefinition : dataType Function COLON Body'''

def p_Function(p):
    '''Function : IDENTIFIER LPAREN Parameter RPAREN'''

def p_Parameter(p):
    ''' Parameter : dataType IDENTIFIER
                  | dataType IDENTIFIER COMMA Parameter
                  | EMPTY'''

def p_FunctionCall(p):
    ''' FunctionCall : IDENTIFIER LPAREN FunctionCallParameter RPAREN SEMICOLON'''

def p_FunctionCallParameter(p):
    '''FunctionCallParameter : IDENTIFIER
                            | IDENTIFIER COMMA FunctionCallParameter
                            
                            | EMPTY'''

def p_returnDec(p):
    '''returnDec : RETURN CONSTANT SEMICOLON
                | RETURN IDENTIFIER SEMICOLON
                | RETURN expression SEMICOLON
                | RETURN SEMICOLON'''

def p_booleanValue(p):
  '''booleanValue : TRUE
                  | FALSE'''
# Error rule for syntax errors
def p_error(p):
    x = ["\n\n\tAY NAKO Fudgee bar :( May syntax warnings!", "\n\n\tOMG! May syntax Warnings huhubells", "\n\n\tKalerki:( May syntax warnings!", "\n\n\tput**** may syntax warnings"]
    print x[randint(0,3)]
    #print "\n\nOO! Nako po! May syntax WARNINGS!"
    if p:

      print "[BABALA] Ito'y matatagpuan bago ang TOKEN \" ", p.value, " \" "" sa linya numero: ", p.lineno, "and Lexical posisyon ", p.lexpos
         #Syntax error of type: ", p.type, 
         # Just discard the token and tell the parser it's okay.
         #parser.errok()
    else:
      print "ERROR"




# STRING VALUE - TOKEN VALUE
reserved = {
  'AND': 'AND',
  'OR': 'OR',
  'if':'IF',
  'fi': 'FI',
  'end':'END',
  'return':'RETURN',
  'not':'NOT',
  'elif':'ELIF',
  'else':'ELSE',
  'do':'DO',
  'for':'for',
  'while':'WHILE',
  '.keys()':'KEYS',
  '(int)':'TC_INT', 
  '(float)':'TC_FLOAT',
  'boolean':'BOOLEAN',
  'int':'INT',
#  'float':'FLOAT',
#  '.split':'SPLIT',
#  '.strip':'STRIP',
#  '.concat':'CONCAT',
#  '.insert':'INSERT',
#  '.pop':'POP',
#  '.copy':'COPY',
  'True':'TRUE',
  'False':'FALSE',
  'read':'READ',
#  'print':'PRINT',
  'string':'STRING' 

}

tokens = ['PRINT', 'FLOAT', 'SPLIT', 'STRIP', 'CONCAT', 'INSERT', 'POP', 'COPY', 'LISTVALUE' , 'FLOATVALUE', 'EMPTY', 'ARROW', 'EQUAL', 'COMMA', 'BAR', 'QUOTE', 'RCURLY', 'LCURLY', 'GREATERTHAN', 'LESSTHAN' ,'MOD','DIV','MULT','MINUS', 'PLUS', 'MINUSEQUAL', 'MULTEQUAL', 'DIVEQUAL', 'MODEQUAL', 'GREATEREQ', 'LESSEREQ', 'NOTEQ', 'COMMENT', 'MINUSMINUS', 'EQUALEQUAL', 'PLUSEQUAL','PLUSPLUS', 'STRINGVALUE', 'LBRACK', 'RBRACK', 'SEMICOLON', 'COLON' , 'LPAREN', 'RPAREN', 'CONSTANT', 'IDENTIFIER']+ list(reserved.values())

# Regular expression rules for simple tokens


literals = "+=*/|';\"!%-:,><{}"

def t_LISTVALUE(t):
  r'(\[) ((\"(.+)\") | (\d)) (\, ((\"(.+)\") | (\d)) )* (\])'
  return t

t_FLOAT = r'\.float'
t_SPLIT = r'\.split'
t_STRIP = r'\.strip'
t_CONCAT = r'\.concat'
t_INSERT = r'\.insert'
t_POP = r'\.pop'
t_COPY = r'\.copy'

t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_LBRACK = r'\['
t_RBRACK = r'\]'
#t_INDENT  = r'\t'
t_EQUALEQUAL  = r'\=\='
t_NOTEQ = r'!='

t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'\-='
t_MULTEQUAL = r'\*='
t_DIVEQUAL = r'\/='
t_MODEQUAL = r'%='
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'\-\-'

### CYAN ###

t_ARROW = r'\-\>'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_QUOTE = r'\"'
t_COMMA = r'\,'
t_BAR = r'\|'
t_EMPTY = r'\'\''
t_EQUAL = r'\='

############

t_GREATEREQ = r'>='
t_LESSEREQ = r'<='

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

def t_PRINT(t):
    r'\print .*'
    pass
    # No return value. Token discarded

def t_FLOATVALUE(t):
  r'[+-]?(\d+(\.\d*)|\.\d+)([eE][+-]?\d+)?'
  t.value = float(t.value)
  return t

def t_CONSTANT(t):
  r'[-]*[0-9][0-9]*'
  t.value = int(t.value)    
  return t

def t_STRINGVALUE(t):
  r'".+"'
  t.value = (t.value.lstrip("\"").rstrip("\""))
  return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces ) nottabs)
t_ignore  = ' \t'                 # ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Compute column. 
#     input is the input text string
#     token is a token instance
def find_column(input,token):
  last_cr = input.rfind('\n',0,token.lexpos)
  if last_cr < 0:
    last_cr = 0
  column = (token.lexpos - last_cr) + 1
  return column












#+====================================================================




























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
                self.file = ''  
                
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
                pass
#                temp = Syntax.syntax()
 #               temp.set_input(self.text.get(1.0, END))
  #              temp.algorithm()

        def run(self):
            self.save()
            # Build the lexer
            lexer = lex.lex()     # lex(debug = 1)


            # For the data...
            fp = open(self.file, "r")
            data = fp.read()

            fp.close()
            # Test it out
            """
            data = '''
            7 + 5 
            3 + 4 * 10
              + -20 *2* 30
            '''
            """

            # Give the lexer some input
            #lexer.lineno = 0
            #lexer.input(data)
            #fp = open("lexicalTokens.out", "w")
            #fp.write("TYPE\tVALUE\tLINE NO\tLEX PO\n")
            #for tok in lexer:
            #  x = x + 1
            #  valueer = str( tok.type) + "\t" + str(tok.value) + "\t" + str(tok.lineno) + "\t" +  str(tok.lexpos) + "\n"
            #  fp.write(valueer)
            # print find_column(data, tok)
            #fp.close()
            # print "THERE ARE A TOTAL OF ", x, "TOKENS"
            # print find_column(data, tok)

            """
            while True:
                tok = lexer.token()
                if not tok: 
                    break      # No more input
                print(tok)    # print(tok.type, tok.value, tok.lineno, tok.lexpos)
            """

            # Build the parser
            
            parser = yacc.yacc()
            print "IS THERE A WARNING? :",

            while True:
              fp = open(self.file, "r")
              try:
                s = fp.read()
                #s = raw_input('calc > ')
                
              except EOFError:
                break
              if not s: continue
              result = parser.parse(s, tracking=True)
              print(result)
              break;

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
