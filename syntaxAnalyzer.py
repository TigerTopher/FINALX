# Yacc example
from random import randint

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import tokens

#def p_statementAug(p):
#  'statementAug : statementTop'

listNum = []

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

remainder = 0

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

# Build the parser
parser = yacc.yacc()
print "Syntax Analyzer Running...\n\nIS THERE A WARNING? :",


while True:
  fp = open("source.txt", "r")
  listNum = []
  for line in fp:
    listNum.append(len(line.rstrip("\n")))
#  print lineList
  fp.close()
  fp = open("source.txt", "r")
  try:
    s = fp.read()
    #s = raw_input('calc > ')
    
  except EOFError:
    break
  if not s: continue
  warningCounts = 0
  result = parser.parse(s, tracking=True)

  if(warningCounts != 0):
    print "\n\nThere are a total of", warningCounts, "warning/s."
  else:
    print "No Warnings"
  raw_input()