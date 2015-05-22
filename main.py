import ply.lex as lex
import ply.yacc as yacc
from random import randint
from tkFileDialog import *
from tkMessageBox import *
from tkSimpleDialog import *
from Tkinter import *
from PIL import Image, ImageTk
import Syntax

from pygments import lex as pyglex
from tkFont import *
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Token, Whitespace

#=====================================GUI PART========================================

START = '1.0'
SEL_FIRST = SEL + '.first'
SEL_LAST = SEL + '.last'
warningCounts = 0
remainder = 0
datatypes = ["boolean", "string", "int", "float"]
listNum = []



#=======================================================================================================


#==============================================================================START OF LEXICAL ANALYZER
# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------

#num_count = 0

# List of token names.   This is always required
"""
All lexers must provide a list tokens that defines all of the possible token names that can be produced by the lexer. 
This list is always required and is used to perform a variety of validation checks. 
The tokens list is also used by the yacc.py module to identify terminals
"""
"""
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'NEGCON',
   'LPAREN',
   'RPAREN',
   'IDENTIFIER' 
)
"""

# STRING VALUE - TOKEN VALUE
reserved = {
  'and': 'AND',
  'or': 'OR',
  'if':'IF',
  'fi': 'FI',
  'end':'END',
  'return':'RETURN',
  'not':'NOT',
  'elif':'ELIF',
  'else':'ELSE',
#  'do':'DO',
  'for':'for',
  'while':'WHILE',
  '.keys()':'KEYS',
  '(int)':'TC_INT', 
  '(float)':'TC_FLOAT',
  'boolean':'BOOLEAN',
  'int':'INT',
  'float':'FLOAT',
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

tokens = ['PRINT', 'SPLIT', 'STRIP', 'CONCAT', 'INSERT', 'POP', 'COPY', 'LISTVALUE' , 'FLOATVALUE', 'EMPTY', 'EQUAL', 'COMMA', 'BAR', 'GREATERTHAN', 'LESSTHAN' ,'MOD','DIV','MULT','MINUS', 'PLUS', 'MINUSEQUAL', 'MULTEQUAL', 'DIVEQUAL', 'MODEQUAL', 'GREATEREQ', 'LESSEREQ', 'NOTEQ', 'COMMENT', 'MINUSMINUS', 'EQUALEQUAL', 'PLUSEQUAL','PLUSPLUS', 'STRINGVALUE', 'LBRACK', 'RBRACK', 'SEMICOLON', 'COLON' , 'LPAREN', 'RPAREN', 'CONSTANT', 'IDENTIFIER']+ list(reserved.values())
# 'QUOTE', 'RCURLY', 'LCURLY','ARROW', 
# Regular expression rules for simple tokens


literals = "+=*/|';\"!%-:,><{}"

def t_LISTVALUE(t):
  r'(\[) ((\"(.+)\") | (\d)) (\, ((\"(.+)\") | (\d)) )* (\])'
  return t

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

#t_ARROW = r'\-\>'
#t_LCURLY = r'\{'
#t_RCURLY = r'\}'
#t_QUOTE = r'\"'
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
t_ignore  = ' \t\f\v\r'                 # ' \t'

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


"""
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)    # print(tok.type, tok.value, tok.lineno, tok.lexpos)
"""

#========================================================END OF LEXICAL ANALYZER


#========================================================START SYNTAX ANALYZER
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

#def p_unionDec(p):
#    '''unionDec : IDENTIFIER EQUAL union SEMICOLON'''

#def p_union(p):
#    '''union : LCURLY unionElement RCURLY'''

#def p_unionElement(p):
#    '''unionElement : STRING EQUAL validListUnionValues
#                 | STRING EQUAL validListUnionValues COMMA unionElement
#                 | EMPTY'''

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
              | FLOATVALUE
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
                  | RelationExpression'''
#union
def p_RelationExpression(p):
    '''RelationExpression : LPAREN Operand RelationOperator Operand RPAREN'''

def p_ArithmeticExpression(p):
    '''ArithmeticExpression : LESSTHAN Operand ArithmeticOperator Operand GREATERTHAN
                            | LESSTHAN CONSTANT GREATERTHAN'''

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

def getLineNumber(num):
  global listNum
  global remainder
  remainder = 0
  count = num
  lineCount = 1
  #print "\nNUMBER :" , num
  for x in listNum:
    #print "COUNT: ", count, "LINE COUNT", lineCount, "X: ", x
    if count >= x:
      count = count - x
      lineCount = lineCount + 1
    else:
      break

  #print "FINAL COUNT:", lineCount, "with remainder", count
  return lineCount

warningCounts = 0

def p_error(p):
    global listNum
    global warningCounts
    global remainder

    warningCounts = warningCounts + 1

    comments = ["\n\n>>> CYAN SAYS: Ahhhh, may mali po sa code niyo",
         "\n\n>>> NEIL SAYS: Pare, advice lang. May warnings. YOLO na yan", 
         "\n\n>>> DOM SAYS: Tigil mo na yan Toph.", 
          "\n\n>>> JAYPEE SAYS: <seenzone> *may warnings ka ata*",
          "\n\n>>> TOPH SAYS: 4r4y k0 b3h :( Ginawa ko naman lahat ah. Huhubells",
          "\n\n>>> SIR PHILIP SAYS: SHIFT NA",
          "\n\n>>> MA'AM ADA SAYS: HALA MALI YAN...",
          "\n\n>>> MA'AM JAH SAYS: Either may mali ka sa syntax or NP-HARD yan",
          "\n\n>>> SIR TOPE SAYS: Tanong mo kay Rae. May warning ka daw sa syntax.",
          "\n\n>>> MA'AM RAE SAYS: Tanong mo kay Tope. May warning ka daw sa syntax.",
          "\n\n>>> SIR BENJ SAYS: OKAY. May syntax error pa.",
          "\n\n>>> SIR EDGE SAYS: There is a DOCUMENTED bug. [Syntax ERROR]",


          ]
    print "\t", comments[randint(0,len(comments)-1)]
    #print "\n\nOO! Nako po! May syntax WARNINGS!"
    if p:

      print ">>> [ WARNING ] Problem before the VALUE '", p.value, "'of TOKEN TYPE '", p.type, "'\n    found in LINE", getLineNumber(p.lexpos), ", COLUMN", remainder, "[ Lexical Position: ", p.lexpos, "]"
         #Syntax error of type: ", p.type, 
         # Just discard the token and tell the parser it's okay.
         #parser.errok()
    else:
      print "ERROR"
      print "NOTE: If an error returns no line number, then the error is on the last line."

#=======================================================END SYNTAX ANALYZER













#======================================================= PARSER
class algorithm():
  def __init__(self):
    self.input = ""
    self.variables = {}
    self.condition = 0  #Determines how deep the code is at
    self.trial = {}
    self.functions = {}

  def set_input(self, temp):
    self.input = temp
    self.input = self.input.split("\n")
    self.check()

  def check(self, b=None, c=None):
    a = 0
    while(1):
      try:
        if b == None:
          temp = self.input[a]
        else:
          temp = b[a]
        temp = temp[:-1]
        temp1 = temp.lstrip()
        temp1 = temp1.split(" ")

        for x in range(len(temp1)):
          if "#" in temp1[x] and ((temp1[:x].count('"') != temp1[x:].count('"')) or (temp1[:x].count("'") != temp1[x:].count("'")) or (temp1[:x].count("'") == 0 and temp1[:x].count('"'))) == 0:
            temp1[x] = temp1[x].split("#")
            temp1[x] = temp1[x][0]
            temp1 = temp1[:x+1]
            break
        temp1 = " ".join([str(i) for i in temp1])
        temp1 = temp1.rstrip()
        temp1 = temp1.split(" ")

      except:
        break

      if temp.count("\t") < self.condition:
        while temp.count("\t") < self.condition:
          self.condition -= 1

      if self.condition != temp.count("\t") or temp1 == [""]:
        pass

      elif "|" in temp1[0] and "|" in temp1[-1]:  #if line is assignment, assign
        temp1 = self.remove_pipe(temp1)

        if len(temp1) > 2:
          temp1 = self.split_equals(temp1)
          temp1 = self.remove_greater(temp1)

          if temp1[0] in datatypes:
            self.equate(temp1[1], temp1[3:], c, temp1)
          else:
            self.equate(temp1[0], temp1[2:], c)
        else:
          self.equate(temp1)

      elif temp1[0] == "if" or (temp1[0] == "elif" and self.trial[self.condition] == -1): #if line is if
        self.conditional(temp1[1:])

      elif temp1[0] == "els" and len(temp1) == 1 and self.trial[self.condition] == -1:
        self.conditional([1])

      elif temp1[0] == "break" and len(temp1) == 1: #break
        self.condition -= 1   

      elif temp1[0] == "for" and "(" in temp1[1]: #for loop
        temp1[1] = list(temp1[1])
        temp1[1].remove("(")
        temp1[1] = "".join([str(i) for i in temp1[1]])

        temp1 = " ".join([str(i) for i in temp1[1:]])
        temp1 = temp1.split(";")
        if b != None:
          self.forer(temp1, a, b)
        else:
          self.forer(temp1, a, self.input)

      elif temp1[0] == "do" and len(temp1) == 1:
        if b != None:
          self.do_whiler(a, b)
        else:
          self.do_whiler(a, self.input)

      elif temp1[0] in datatypes:
        self.function_declare(temp1, a)

      elif temp1[0] in self.functions:
        temp2 = list(temp1[1])
        temp2 = "".join([str(i) for i in temp2[1:-1]])
        temp2 = temp2.split(",")

        self.run_function(temp1[0], temp2)

      elif temp1[0] == "print":
        self.printer(temp1)

      elif temp1[0] == "read":
        self.reader(temp1)

      elif ".insert" in temp1[0]:
        temp1 = "".join([str(i) for i in temp1])
        temp2 = temp1.split(".insert")
        self.insert(temp2[0], temp2[1])

      elif ".pop" in temp1[0]:
        temp1 = "".join([str(i) for i in temp1])
        temp2 = temp1.split(".pop")
        self.pop(temp2[0], temp2[1])



      a += 1

  def remove_pipe(self, thisisvariablenumber1): #input is list
    if thisisvariablenumber1[0] == "|":
      thisisvariablenumber1.pop(0)
    else:
      thisisvariablenumber1[0] = thisisvariablenumber1[0].split("|")
      thisisvariablenumber1[0] = "".join([str(i) for i in thisisvariablenumber1[0][1:]])

    if thisisvariablenumber1[-1] == "|":
      thisisvariablenumber1.pop(-1)
    else:
      
      thisisvariablenumber1[-1] = thisisvariablenumber1[-1].split("|")
      if len(thisisvariablenumber1) != 1:
        thisisvariablenumber1[-1] = "".join([str(i) for i in thisisvariablenumber1[-1][:-1]])
      else:
        return thisisvariablenumber1[0]

    return thisisvariablenumber1

  def split_equals(self, thisisvariablenumber1):
    for x in range(len(thisisvariablenumber1)):
      if "=" in thisisvariablenumber1[x] and len(thisisvariablenumber1[x]) != 1:
        thisisvariablenumber1[x] = thisisvariablenumber1[x].split("=")
        temp1 = thisisvariablenumber1[x]

        if "+" in temp1[0] or "-" in temp1[0] or "*" in temp1[0] or "/" in temp1[0] or "%" in temp1[0]:
          if len(list(temp1[0])) == 1:
            thisisvariablenumber1.insert(x, "=")
            thisisvariablenumber1.insert(x+1, thisisvariablenumber1[0])
            thisisvariablenumber1.insert(x+2, temp1[0])
            thisisvariablenumber1.insert(x+3, temp1[1])
            thisisvariablenumber1.pop(x+4)
          else:
            
            temp2 = list(temp1[0])
            temp3 = temp2[-1]
            temp2 = "".join([str(i) for i in temp2[:-1]])
            temp4 = []
            temp4.append(temp2)
            temp4.append("=")
            temp4.append(temp2)
            temp4.append(temp3)
            temp5 = thisisvariablenumber1[1:]
            temp5.insert(0,list(temp1)[1])
            for x in temp5:
              temp4.append(x)

            thisisvariablenumber1 = temp4
          break

        thisisvariablenumber1.insert(x, temp1[0])
        thisisvariablenumber1.insert(x+1, "=")
        thisisvariablenumber1.insert(x+2, temp1[1])
        thisisvariablenumber1.pop(x+3)
        break
    
    return thisisvariablenumber1

  def remove_greater(self, thisisvariablenumber1):
    if len(thisisvariablenumber1[-1]) == 1 and ">" in thisisvariablenumber1[-1]:
      thisisvariablenumber1.pop(-1)
    elif ">" in thisisvariablenumber1[-1]:
      thisisvariablenumber1[-1] = thisisvariablenumber1[-1].split(">")
      thisisvariablenumber1[-1] = "".join([str(i) for i in thisisvariablenumber1[-1][:-1]])

    if len(thisisvariablenumber1[2:][0]) == 1 and "<" in thisisvariablenumber1[2:][0]:
      thisisvariablenumber1.remove("<")
    else:
      thisisvariablenumber1[2:] = "".join([str(i) for i in thisisvariablenumber1[2:]])
      try:
        thisisvariablenumber1.remove("<")
        thisisvariablenumber1[2:] = "".join([str(i) for i in thisisvariablenumber1[2:]])
      except:
        pass

    return thisisvariablenumber1

  def equate(self, thisisvariablenumber1, thisisvariablenumber2=None, extra=None, data=None):
    if thisisvariablenumber2 != None: 
      temp1 = list(thisisvariablenumber2)
      temp2 = []
      for x in temp1:
        if x == "<" or x == ">":
          pass
        else:
          temp2.append(x)
      temp3 = ""
      for x in range(len(thisisvariablenumber2)):
        if thisisvariablenumber2[x] in ["+", "-", "/", "*", "%"]:
          temp3 = " ".join([str(i) for i in thisisvariablenumber2[:x]]) + " " + thisisvariablenumber2[x] + " " + "".join([str(i) for i in thisisvariablenumber2[x+1:]])
          
      if temp3 == "":
        thisisvariablenumber2 = "".join([str(i) for i in temp2])
        thisisvariablenumber2 = thisisvariablenumber2.split("\n")
      else:
        thisisvariablenumber2 = temp3.split(" ")
      
      try:
        for x in range(len(thisisvariablenumber2)):
          if extra != None and thisisvariablenumber2[x] in extra:
            thisisvariablenumber2[x] = extra[thisisvariablenumber2[x]] 
          elif thisisvariablenumber2[x] in self.variables:
            thisisvariablenumber2[x] = self.variables[thisisvariablenumber2[x]]

        if data == None and (thisisvariablenumber1 in self.variables or thisisvariablenumber1 in extra):
          self.variables[thisisvariablenumber1] = eval("".join([str(i) for i in thisisvariablenumber2]))
          if ".pop" in "".join([str(i) for i in thisisvariablenumber2]):
            temp1 = "".join([str(i) for i in thisisvariablenumber2])
            temp1 = temp1.split(".pop")
            temp2 = list(temp1[1])
            temp2 = "".join([str(i) for i in temp2[1:-1]])
            for x in self.variables:
              if str(self.variables[x]) == str(temp1[0]):
                self.variables[x].pop(int(temp2))
        elif data != None:
          self.variables[thisisvariablenumber1] = eval("".join([str(i) for i in thisisvariablenumber2]))
          if ".pop" in "".join([str(i) for i in thisisvariablenumber2]):
            temp1 = "".join([str(i) for i in thisisvariablenumber2])
            temp1 = temp1.split(".pop")
            temp2 = list(temp1[1])
            temp2 = "".join([str(i) for i in temp2[1:-1]])
            for x in self.variables:
              if str(self.variables[x]) == str(temp1[0]):
                self.variables[x].pop(int(temp2))
        else:
          exit(1)

      except:
        for x in range(len(thisisvariablenumber2)):
          if extra != None and thisisvariablenumber2[x] in extra:
            thisisvariablenumber2[x] = extra[thisisvariablenumber2[x]] 
          elif thisisvariablenumber2[x] in self.variables:
            thisisvariablenumber2[x] = self.variables[thisisvariablenumber2[x]]

        if data == None and (thisisvariablenumber1 in self.variables or thisisvariablenumber1 in extra):
          self.variables[thisisvariablenumber1] = eval("".join([str(i) for i in thisisvariablenumber2]))
          if ".pop" in "".join([str(i) for i in thisisvariablenumber2]):
            temp1 = "".join([str(i) for i in thisisvariablenumber2])
            temp1 = temp1.split(".pop")
            temp2 = list(temp1[1])
            temp2 = "".join([str(i) for i in temp2[1:-1]])
            for x in self.variables:
              if str(self.variables[x]) == str(temp1[0]):
                self.variables[x].pop(int(temp2))
        elif data != None:
          self.variables[thisisvariablenumber1] = eval("".join([str(i) for i in thisisvariablenumber2]))
          if ".pop" in "".join([str(i) for i in thisisvariablenumber2]):
            temp1 = "".join([str(i) for i in thisisvariablenumber2])
            temp1 = temp1.split(".pop")
            temp2 = list(temp1[1])
            temp2 = "".join([str(i) for i in temp2[1:-1]])
            for x in self.variables:
              if str(self.variables[x]) == str(temp1[0]):
                self.variables[x].pop(int(temp2))
        else:
          print "Error. Undeclared variable " + thisisvariablenumber1
          exit(1)

    else:
      #if thisisvariablenumber2 != None and data != None:
      if thisisvariablenumber1[0] == "int":
        self.variables[thisisvariablenumber1[1]] = 0
      elif thisisvariablenumber1[0] == "float":
        self.variables[thisisvariablenumber1[1]] = 0.0
      elif thisisvariablenumber1[0] == "string":
        self.variables[thisisvariablenumber1[1]] = ""
      elif thisisvariablenumber1[0] == "boolean":
        self.variables[thisisvariablenumber1[1]] = False
      #elif data != None:
      # self.equate(thisisvariablenumber1, thisisvariablenumber2, extra, None)

  def conditional(self, thisisvariablenumber1, thisisvariablenumber2=0):
    thisisvariablenumber1 = list(thisisvariablenumber1)

    for x in range(len(thisisvariablenumber1)):
      try:
        thisisvariablenumber1[x] = list(thisisvariablenumber1[x])
        thisisvariablenumber1[x] = [value for value in thisisvariablenumber1[x] if value != "(" and value != ")"]
        thisisvariablenumber1[x] = "".join([str(i) for i in thisisvariablenumber1[x]])

        if thisisvariablenumber1[x]  in self.variables:
          thisisvariablenumber1[x] = self.variables[thisisvariablenumber1[x]]
      except:
        pass
    try:
      temp = eval(" ".join([str(i) for i in thisisvariablenumber1]))
    except:
      temp = eval("".join([str(i) for i in thisisvariablenumber1]))

    if temp == True and thisisvariablenumber2 == 0:
      self.trial[self.condition] = self.condition
      self.condition += 1
    elif temp == True and thisisvariablenumber2 == 1:
      return self.condition
    elif temp == True and thisisvariablenumber2 == 2:
      return True
    else:
      self.trial[self.condition] = -1

  def forer(self, thisisvariablenumber1, linenumber, lines):
    temp1 = self.remove_pipe(list(thisisvariablenumber1[0].replace(" ", "")))
    temp1 = self.split_equals(temp1)
    temp1 = self.remove_greater(temp1)
    self.equate(temp1[0], temp1[2:])

    temp = lines[linenumber+1:]
    temp1 = []
    for x in temp:
      if x.count("\t") >= self.condition+1 and len(x) != 1:
        temp1.append(x)
      elif len(x) == 0:
        pass
      else:
        break
    temp = temp1

    self.condition += 1
    self.trial[self.condition] = self.condition

    temp2 = list(thisisvariablenumber1[2])
    temp3 = []
    for x in temp2:
      if x == "(" or x == ")":
        pass
      else:
        temp3.append(x)
    temp3 = "".join([str(i) for i in temp3])

    while (self.conditional(thisisvariablenumber1[1].lstrip().split(" "), 2) == True):
      self.check(temp)
      self.iterate(temp3)

    self.condition -= 1

  def iterate(self, thisisvariablenumber1):
    temp1 = thisisvariablenumber1.lstrip()
    temp1 = temp1.split(" ")

    temp2 = temp1[-1:]
    temp1 = temp1[:-1]
    temp1 = " ".join([str(i) for i in temp1])

    if temp2 == ["++"]:
      self.variables[temp1] += 1

    elif temp2 == ["--"]:
      self.variables[temp1] -= 1

  def do_whiler(self, linenumber, lines):
    temp = lines[linenumber+1:]
    temp1 = []
    test = ""
    for x in temp:
      if x.count("\t") >= self.condition+1 and len(x) != 1:
        temp1.append(x)
      else:
        test = x
        break

    temp = temp1
    self.condition += 1
    self.trial[self.condition] = self.condition
    self.check(temp)
    test = test.split(" ")
    test[-1] = list(test[-1])[:-1]
    test[-1] = "".join([str(i) for i in test[-1]])
    test = test[1:]
    test = " ".join([str(i) for i in test])

    while(self.conditional(test, 2) == True):
      self.check(temp)

    self.condition -= 1

  def function_declare(self, thisisvariablenumber1, linenumber):
    typer = thisisvariablenumber1[0]
    name = thisisvariablenumber1[1]
    thisisvariablenumber1.pop(2)
    thisisvariablenumber1.pop(-1)
    arguments = " ".join([str(i) for i in thisisvariablenumber1[2:]])
    arguments = arguments.split(",")

    temp = self.input[linenumber+1:]
    temp1 = []
    for x in temp:
      if x.count("\t") == self.condition+1 and len(x) != 1:
        temp1.append(x)
      else:
        break
    temp = temp1
    
    self.functions[name] = [typer, arguments, temp]

  def run_function(self, name, arguments=None):
    temp = self.functions[name]
    if len(temp[1]) != len(arguments):
      print "ERROR. Invalid arguments."
      exit(1)
    else:
      temp1 = {}
      a = 0
      for x in temp[1]:
        temp2 = x.split(" ")
        temp2[1] = " ".join([str(i) for i in temp2[1:]])
        temp3 = temp2[0]
        temp2 = temp2[1]
        temp1[temp2] = arguments[a]
        
        if temp1[temp2] in self.variables:
          temp1[temp2] = self.variables[temp1[temp2]]
        elif temp3 == "int":
          temp1[temp2] = int(temp1[temp2])
        elif temp3 == "float":
          temp1[temp2] = float(temp1[temp2])
        elif temp3 == "string":
          temp1[temp2] = str(temp1[temp2])
        a += 1

    self.condition += 1

    self.check(temp[2], temp1)

  def printer(self, arguments):
    temp = arguments[1:]
    temp = " ".join([str(i) for i in temp])
    temp = list(temp)
    temp.pop(0)
    temp.pop(-1)
    temp = "".join([str(i) for i in temp])
    if temp in self.variables:
      print self.variables[temp]
    else:
      try:
        print eval(temp)
      except:
        print temp

  def reader(self, arguments):
    temp = arguments[1]
    temp = list(temp)
    temp.pop(0)
    temp.pop(-1)
    temp = "".join([str(i) for i in temp])

    temp1 = raw_input();

    self.equate(temp, temp1)

  def insert(self, thisisvariablenumber1, thisisvariablenumber2):
    temp = thisisvariablenumber1
    objects = thisisvariablenumber2
    objects = list(objects)
    objects = "".join([str(i) for i in objects[1:-1]])
    objects = objects.split(",")

    self.variables[temp].insert(int(objects[0]), eval(objects[1]))

  def pop(self, thisisvariablenumber1, thisisvariablenumber2):
    temp = thisisvariablenumber1
    objects = thisisvariablenumber2
    objects = list(objects)
    objects = "".join([str(i) for i in objects[1:-1]])

    self.variables[temp].pop(int(objects))

#================================================================================End of Parser Execution


#================================================================================Running the Parser

class MyPythonLexer(PythonLexer):
    EXTRA_KEYWORDS = set(('fi', 'end'))
    EXTRA_FUNC = set(('print', 'read'))

    def get_tokens_unprocessed(self, text):
        for index, token, value in PythonLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield index, Keyword, value

            elif token is Name and value in self.EXTRA_FUNC:
                yield index, Name.Function, value
            else:
                yield index, token, value


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
                try:
                  self.root.wm_iconbitmap("prismicon.ico")
                except:
                  pass

                
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
                                 background = a.background_color,
                                 highlightcolor = a.highlight_color,
                                 insertbackground = "white",
                                 fg = "white")
                
                self.text.pack(side=LEFT, fill=BOTH, expand=YES)

                scroll = Scrollbar(self.root, orient=VERTICAL, command=self.text.yview)
                scroll.pack(side=RIGHT, fill=Y)

                self.text["yscrollcommand"] = scroll.set
                self.text.bind("<KeyRelease>", self.color)


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
                lexer = lex.lex()     # lex(debug = 1)

                fp = open(self.file, "r")
                data = fp.read()

                fp.close()


                lexer.input(data)

                fp = open("lexicalTokens.out", "w")
                fp.write("TYPE\tVALUE\tLINE NO\tLEX PO\n")
                for tok in lexer:
                  #  x = x + 1
                  valueer = str( tok.type) + "\t" + str(tok.value) + "\t" + str(tok.lineno) + "\t" +  str(tok.lexpos) + "\n"
                  fp.write(valueer)
                  # print find_column(data, tok)
                fp.close()


                  # Build the parser
                parser = yacc.yacc()
                print "Syntax Analyzer Running...\n\nIS THERE A WARNING? :",


                while True:
                  fp = open(self.file, "r")
                  listNum = []
                  for line in fp:
                    listNum.append(len(line.rstrip("\n")))
                  #  print lineList
                  fp.close()

                  fp = open(self.file, "r")
                  try:
                    s = fp.read()
                      #s = raw_input('calc > ')
                  except EOFError:
                      break
                  fp.close()
                  if not s: continue
                  warningCounts = 0
                  result = parser.parse(s, tracking=True)

                  if(warningCounts != 0):
                    print "\n\nThere are a total of", warningCounts, "warning/s."
                  else:
                    print "No Warnings"
                  
                  break

                


                mainParser = algorithm()
                fp = open(self.file,"r")
                binasaNaFile = fp.read()
                mainParser.set_input(binasaNaFile)
                


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
                
        def noItalic(self, str):
                if str == "noItalic":
                        return "roman"
                else:
                        return "italic"

        def noBold(self, str):
                if str == "noBold":
                        return "normal"
                else:
                        return "bold"

        def color(self, event = None):
                self.text.mark_set("range_start", "1.0")
                data = self.text.get("1.0", "end-1c")

                basefont = 'Courier'
                basesize = 10

                self.text.tag_configure("Token.Text", foreground = "white")
                self.text.tag_configure("Token.Token", foreground = a.styles[Token])

                self.text.tag_configure("Token.Whitespace", foreground = a.styles[Whitespace])

                self.text.tag_configure("Token.Comment.Special", foreground = a.styles[Comment.Special].split(' ')[2], font = Font(family = basefont, size = basesize, slant = self.noItalic(a.styles[Comment.Special].split(' ')[0]), weight = a.styles[Comment.Special].split(' ')[1]))
                self.text.tag_configure("Token.Comment", foreground = a.styles[Comment].split(' ')[1], font = Font(family = basefont, size = basesize, slant = a.styles[Comment].split(' ')[0]))
                #self.text.tag_configure("Token.Comment.Multiline", foreground = "#e50808")
                self.text.tag_configure("Token.Comment.Preproc", foreground = a.styles[Comment.Preproc].split(' ')[2], font = Font(family = basefont, size = basesize, slant = self.noItalic(a.styles[Comment.Preproc].split(' ')[0]), weight = a.styles[Comment.Preproc].split(' ')[1]))

                self.text.tag_configure("Token.Keyword", foreground = a.styles[Keyword].split(' ')[1], font = Font(family = basefont, size = basesize, weight = a.styles[Keyword].split(' ')[0]))
                self.text.tag_configure("Token.Keyword.Namespace", foreground = a.styles[Keyword].split(' ')[1], font = Font(family = basefont, size = basesize, weight = a.styles[Keyword].split(' ')[0]))
                self.text.tag_configure("Token.Keyword.Pseudo", font = Font(family = basefont, size = basesize, weight = self.noBold(a.styles[Keyword.Pseudo])))
                self.text.tag_configure("Token.Keyword.Reserved", font = Font(family = basefont, size = basesize, weight = self.noBold(a.styles[Keyword.Pseudo])))
                self.text.tag_configure("Token.Keyword.Type", foreground = a.styles[Keyword.Type])

                self.text.tag_configure("Token.Operator", foreground = "white")
                self.text.tag_configure("Token.Operator.Word", foreground = a.styles[Operator.Word].split(' ')[1], font = Font(family = basefont, size = basesize, weight = a.styles[Operator.Word].split(' ')[0]))

                self.text.tag_configure("Token.String", foreground = a.styles[String])
                self.text.tag_configure("Token.String.Char", foreground = "#40ffff")
                self.text.tag_configure("Token.String.Double", foreground = "#40ffff")
                self.text.tag_configure("Token.String.Other", foreground = a.styles[String.Other])

                self.text.tag_configure("Token.Literal.String", foreground = "#ffa")

                self.text.tag_configure("Token.Number", foreground = a.styles[Number])

                self.text.tag_configure("Token.Name.Builtin", foreground = a.styles[Name.Builtin])
                self.text.tag_configure("Token.Name.Builtin.Pseudo", foreground = a.styles[Name.Builtin])
                self.text.tag_configure("Token.Name.Function", foreground = a.styles[Name.Function])
                self.text.tag_configure("Token.Name.Class", foreground = a.styles[Name.Class].split(' ')[1], font = Font(family = basefont, size = basesize, underline =  1))
                self.text.tag_configure("Token.Name.Namespace", foreground = a.styles[Name.Namespace].split(' ')[1], font = Font(family = basefont, size = basesize, underline =  1))
                self.text.tag_configure("Token.Name.Exception", foreground = a.styles[Name.Exception])
                self.text.tag_configure("Token.Name.Variable", foreground = a.styles[Name.Variable])
                self.text.tag_configure("Token.Name.Constant", foreground = a.styles[Name.Constant])
                self.text.tag_configure("Token.Name.Tag", foreground = a.styles[Name.Tag].split(' ')[1], font = Font(family = basefont, size = basesize, weight = a.styles[Name.Tag].split(' ')[0]))
                self.text.tag_configure("Token.Name.Attribute", foreground = a.styles[Name.Attribute])
                self.text.tag_configure("Token.Name.Decorator", foreground = a.styles[Name.Decorator])


                self.text.tag_configure("Token.Generic.Heading", foreground = a.styles[Generic.Heading].split(' ')[1], font = Font(family = basefont, size = basesize, weight = a.styles[Generic.Heading].split(' ')[0]))
                self.text.tag_configure("Token.Generic.Subheading", foreground = a.styles[Generic.Subheading].split(' ')[1], font = Font(family = basefont, size = basesize, underline = 1))
                self.text.tag_configure("Token.Generic.Deleted", foreground = a.styles[Generic.Deleted])
                self.text.tag_configure("Token.Generic.Inserted", foreground = a.styles[Generic.Inserted])
                self.text.tag_configure("Token.Generic.Error", foreground = a.styles[Generic.Error])
                self.text.tag_configure("Token.Generic.Emph", font = Font(family = basefont, size = basesize, slant =  a.styles[Generic.Emph]))
                self.text.tag_configure("Token.Generic.Strong", font = Font(family = basefont, size = basesize , weight = a.styles[Generic.Strong]))
                self.text.tag_configure("Token.Generic.Prompt", foreground = a.styles[Generic.Prompt])
                self.text.tag_configure("Token.Generic.Output", foreground = a.styles[Generic.Output])
                self.text.tag_configure("Token.Generic.Traceback", foreground = a.styles[Generic.Traceback])

                self.text.tag_configure("Error", foreground = a.styles[Error].split(' ')[1], background = a.styles[Error].split(' ')[0].split(':')[1])


                for token, content in pyglex(data, MyPythonLexer()):
                        self.text.mark_set("range_end", "range_start + %dc" % len(content))
                        self.text.tag_add(str(token), "range_start", "range_end")
                        self.text.mark_set("range_start", "range_end")



a = get_style_by_name('native')                                
ed = GUI()

