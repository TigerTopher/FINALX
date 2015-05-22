# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

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

# Build the lexer
lexer = lex.lex()     # lex(debug = 1)


# For the data...
fp = open("source.txt", "r")
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
lexer.input(data)

# Tokenize
#x = 0

fp = open("lexicalTokens.out", "w")
fp.write("TYPE\tVALUE\tLINE NO\tLEX PO\n")
for tok in lexer:
#  x = x + 1
  valueer = str( tok.type) + "\t" + str(tok.value) + "\t" + str(tok.lineno) + "\t" +  str(tok.lexpos) + "\n"
  fp.write(valueer)
# print find_column(data, tok)
fp.close()
# print "THERE ARE A TOTAL OF ", x, "TOKENS"
# print find_column(data, tok)

"""
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)    # print(tok.type, tok.value, tok.lineno, tok.lexpos)
"""
