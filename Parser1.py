datatypes = ["boolean", "string", "int", "float"]

class algorithm():
	def __init__(self):
		self.input = ""
		self.variables = {}
		self.condition = 0	#Determines how deep the code is at
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

			elif "|" in temp1[0] and "|" in temp1[-1]:	#if line is assignment, assign
				temp1 = self.remove_pipe(temp1)

				if len(temp1) > 2:
					temp1 = self.split_equals(temp1)
					temp1 = self.remove_greater(temp1)

					if temp1[0] in datatypes and len(temp1) == 2:
						self.equate(temp1[1], temp1[3:], c, temp1)
					else:
						self.equate(temp1[0], temp1[2:], c)
				else:
					self.equate(temp1)

			elif temp1[0] == "if" or (temp1[0] == "elif" and self.trial[self.condition] == -1):	#if line is if
				self.conditional(temp1[1:])

			elif temp1[0] == "els" and len(temp1) == 1 and self.trial[self.condition] == -1:
				self.conditional([1])

			elif temp1[0] == "break" and len(temp1) == 1:	#break
				self.condition -= 1		

			elif temp1[0] == "for" and "(" in temp1[1]:	#for loop
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

	def remove_pipe(self, thisisvariablenumber1):	#input is list
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
			#	self.equate(thisisvariablenumber1, thisisvariablenumber2, extra, None)

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

mainParser = algorithm()
mainParser.set_input("""
|int A|;
print ("Hello po. Celcius to Fahrenheit Solver: Input the Celcius thingy");
read (A);
|int x = < 9.0 / 5.0 > |;
|int z = < x * A > |;
|int y = <32> |;
|int answer = <z + 32>|;
print ("The Fahrenheit is :");
print (answer);
if (answer >= 100)
print ("BOILING!");
end
elif (answer >= 50)
	print ("Medyo Mainit!");
end
elif (answer >= 20)
	print ("Malamig!");
end
else
	print ("lamig takte!");
end
end

""")