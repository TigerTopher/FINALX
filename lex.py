#	Basic lexical analysis based from reference book
#	Now accepts a number as the first character in an identifier
#	Now accepts whitespaces between two identifiers
#	Input is "input.txt" with one line of text/numbers

class lexical_analysis():
	def __init__(self):
		self.charClass = 0
		self.lexeme = ""
		self.nextchar = ""
		self.lexLen = 0
		self.token = 0
		self.nextToken = 0
		self.text = []
		self.tokens = []

		self.LETTER = 0
		self.DIGIT = 1
		self.UNKNOWN = 99

		self.INT_LIT = 10			#<int_literal>
		self.IDENT = 11				#<identifier>
		self.ASSIGN_OP = 20			#<assign_op>
		self.ADD_OP = 21			#	+
		self.SUB_OP = 22			#	-
		self.MULT_OP = 23			#	*
		self.DIV_OP = 24			#	/
		self.LEFT_PAREN = 25		#	(
		self.RIGHT_PAREN = 26		#	)
		self.LEFT_BRACKET = 27		#	[
		self.RIGHT_BRACKET = 28		#	]
		self.LEFT_BRACE = 29		#	{
		self.RIGHT_BRACE = 30		#	}
		self.SEMI_COLON = 31		#	;
		self.COLON = 32				#	:
		self.APOSTROPHE = 33		#	'
		self.DOUBLE_QUOTATION = 34	#	"
		self.LESS_THAN = 35			#	<
		self.GREATER_THAN = 36		#	>
		self.COMMA = 37				#	,
		self.PERIOD = 38			#	.
		self.QUESTION = 39			#	?
		self.BACKSLASH = 40			#	\
		self.VERTICAL_BAR = 41		#	|
		self.UNDERSCORE = 42		#	_
		self.ACCENT = 43			#	`
		self.TILDE = 44				#	~
		self.EXCLAMATION = 45		#	!
		self.AT = 46				#	@
		self.HASH = 47				#	#
		self.DOLLAR = 48			#	$
		self.PERCENT = 49			#	%
		self.CARET = 50				#	^
		self.AMPERSAND = 51			#	&
		self.EOF = 99

	def set_text(self, temp):
		self.text = temp

	def main(self):
		self.getChar()

		self.tokens.append(self.lex())
		while(self.nextToken != self.EOF):
			self.tokens.append(self.lex())

		return self.tokens

	def lookup(self, ch):
		if (ch == "("):
			self.addChar()
			self.nextToken = self.LEFT_PAREN

		elif (ch == ")"):
			self.addChar()
			self.nextToken = self.RIGHT_PAREN

		elif (ch == "+"):
			self.addChar()
			self.nextToken = self.ADD_OP

		elif (ch == "-"):
			self.addChar()
			self.nextToken = self.SUB_OP

		elif (ch == "*"):
			self.addChar()
			self.nextToken = self.MULT_OP

		elif (ch == "/"):
			self.addChar()
			self.nextToken = self.DIV_OP

		elif (ch == "["):
			self.addChar()
			self.nextToken = self.LEFT_BRACKET

		elif (ch == "]"):
			self.addChar()
			self.nextToken = self.RIGHT_BRACKET

		elif (ch == "{"):
			self.addChar()
			self.nextToken = self.LEFT_BRACE

		elif (ch == "}"):
			self.addChar()
			self.nextToken = self.RIGHT_BRACE

		elif (ch == ";"):
			self.addChar()
			self.nextToken = self.SEMI_COLON

		elif (ch == ":"):
			self.addChar()
			self.nextToken = self.COLON

		elif (ch == "'"):
			self.addChar()
			self.nextToken = self.APOSTROPHE

		elif (ch == '"'):
			self.addChar()
			self.nextToken = self.DOUBLE_QUOTATION

		elif (ch == "<"):
			self.addChar()
			self.nextToken = self.LESS_THAN

		elif (ch == ">"):
			self.addChar()
			self.nextToken = self.GREATER_THAN

		elif (ch == ","):
			self.addChar()
			self.nextToken = self.COMMA

		elif (ch == "."):
			self.addChar()
			self.nextToken = self.PERIOD

		elif (ch == "?"):
			self.addChar()
			self.nextToken = self.QUESTION

		elif (ch == "\\"):
			self.addChar()
			self.nextToken = self.BACKSLASH

		elif (ch == "|"):
			self.addChar()
			self.nextToken = self.VERTICAL_BAR

		elif (ch == "_"):
			self.addChar()
			self.nextToken = self.UNDERSCORE

		elif (ch == "`"):
			self.addChar()
			self.nextToken = self.ACCENT

		elif (ch == "~"):
			self.addChar()
			self.nextToken = self.TILDE

		elif (ch == "!"):
			self.addChar()
			self.nextToken = self.EXCLAMATION

		elif (ch == "@"):
			self.addChar()
			self.nextToken = self.AT

		elif (ch == "#"):
			self.addChar()
			self.nextToken = self.HASH

		elif (ch == "$"):
			self.addChar()
			self.nextToken = self.DOLLAR

		elif (ch == "%"):
			self.addChar()
			self.nextToken = self.PERCENT

		elif (ch == "^"):
			self.addChar()
			self.nextToken = self.CARET

		elif (ch == "&"):
			self.addChar()
			self.nextToken = self.AMPERSAND

		else:
			self.addChar()
			self.nextToken = self.EOF

	def addChar(self):
		self.lexeme += self.nextchar

	def getChar(self):
		try:
			self.nextchar = self.text.pop(0)
			if (self.nextchar):
				if (self.nextchar.isalpha()):
					self.charClass = self.LETTER

				elif (self.nextchar.isdigit()):
					self.charClass = self.DIGIT

				else:
					self.charClass = self.UNKNOWN
		except:
			self.charClass = self.EOF
			self.nextchar = ""

	def getNonBlank(self):
		while (self.nextchar == " "):
			self.getChar()

	def lex(self):
		x = 0
		self.lexLen = 0
		self.getNonBlank()

		if (self.charClass == self.LETTER):
			while (self.charClass == self.LETTER or self.charClass == self.DIGIT or self.nextchar == " "):
				self.addChar()
				self.getChar()

			self.nextToken = self.IDENT

		elif (self.charClass == self.DIGIT):
			while (self.charClass == self.DIGIT or self.charClass == self.LETTER):
				if (self.charClass == self.LETTER):
					x = 1

				self.addChar()
				self.getChar()

			if (x == 1):
				self.nextToken = self.IDENT

			else:
				self.nextToken = self.INT_LIT

		elif (self.charClass == self.UNKNOWN):
			self.lookup(self.nextchar)
			self.getChar()

		elif (self.charClass == EOF):
			self.nextToken = self.EOF
			self.lexeme = "EOF"

		print "%s%s%s%s" %("Next token is ", str(self.nextToken), ", Next lexeme is ", self.lexeme)

		self.lexeme = ""
		return self.nextToken