from ortools.sat.python import cp_model
from array import *
from colorama import Fore,Back,init

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
	"""Print intermediate solutions."""
	def __init__(self, variables,boardWidth):
		cp_model.CpSolverSolutionCallback.__init__(self)
		self.__variables = variables
		self.__solution_count = 0
		self.__printAll = False
		self.__debug = False
		self.__testMode = False
		self.__testStringArray = []
		self.__boardWidth = boardWidth

	def setPrintAll(self):
		self.__printAll = True
		
	def setDebug(self):
		self.__debug = True
		
	def setTestMode(self):
		self.__testMode = True
		
	def TestString(self):
		return ''.join(sorted(self.__testStringArray))
		
	def OnSolutionCallback(self):
		self.__solution_count += 1
		cntr = 0
				
		if self.__testMode is True:
			self.__testStringArray.append(''.join(map(str,[self.Value(v) for v in self.__variables])))
		
		elif self.__printAll is True:
			if self.__debug is False:
				# Note: updated this so print only the expected number of variables on-cut, instead of all variables passed
				for i in range(self.__boardWidth**2):
					v = self.__variables[i]
					print('%i' % (self.Value(v)), end = ' ')
					cntr += 1
					if cntr == self.__boardWidth:
						print ()
						cntr = 0
				print()
			else:
				for v in self.__variables:
					print('%s=%i' % (v,self.Value(v)))

	def SolutionCount(self):
		return self.__solution_count
		
def applyNegativeConstraints(self):
	# This method is used to prepare the model for solution. If negative constraints have been set, i.e. all items not marked
	# cannot be marked. These constraints cannot be applied at time of assertion, since there may be new marks added after
	# the assertion. This function applies all negative constraints just prior to solving, and is called by the solver function.
	
	for x in self._constraintNegative:
		getattr(self,'_apply'+x+'Negative')()

def findSolution(self,test=False,debug=False):
	self.applyNegativeConstraints()
	self.solver = cp_model.CpSolver()
	consolidatedCellValues = []
	for tempArray in self.cellValues: consolidatedCellValues = consolidatedCellValues + tempArray
	solution_printer = SolutionPrinter(consolidatedCellValues,self.boardWidth)
	self.solveStatus = self.solver.Solve(self.model)
	
	if test is True:
		return self.testStringSolution()
	elif debug is True:
		for v in self.allVars:
			print('%s=%i' % (v,self.solver.Value(v)))
		print('Number of variables: '+str(len(self.allVars)))
		return self.solveStatus
	else:
		print('Solver status = %s' % self.solver.StatusName(self.solveStatus))
		if self.solveStatus == cp_model.OPTIMAL:
			print('Solution found!')
			self.printCurrentSolution()
		return self.solveStatus

def preparePrintVariables(self):
	consolidatedCellValues = []
	for tempArray in self.cellValues:
		consolidatedCellValues = consolidatedCellValues + tempArray
	return consolidatedCellValues

def countSolutions(self,printAll = False,debug = False,test=False):
	self.applyNegativeConstraints()
	self.solver = cp_model.CpSolver()
	consolidatedCellValues = self.preparePrintVariables()
	if debug is True:
		solution_printer = SolutionPrinter(self.allVars,self.boardWidth)
	else:	
		solution_printer = SolutionPrinter(consolidatedCellValues,self.boardWidth)
	if printAll is True: solution_printer.setPrintAll()
	if debug is True: solution_printer.setDebug()
	if test is True: solution_printer.setTestMode()
	self.solveStatus = self.solver.SearchForAllSolutions(self.model, solution_printer)
	
	if test is True:
		return str(solution_printer.SolutionCount())+':'+solution_printer.TestString()
	else:
		print('Solutions found : %i' % solution_printer.SolutionCount())
		if printAll is False and self.solveStatus == cp_model.OPTIMAL:
			print('Sample solution')
			self.printCurrentSolution()
		return solution_printer.SolutionCount()
			
def printCurrentSolution(self):
	dW = max([len(str(x)) for x in self.digits])
	for rowIndex in range(self.boardWidth):
		for colIndex in range(self.boardWidth):
			print('{:d}'.format(self.solver.Value(self.cellValues[rowIndex][colIndex])).rjust(dW),end = " ")
		print()
	print()
	
def testStringSolution(self):
	testString = ''
	for rowIndex in range(self.boardWidth):
		for colIndex in range(self.boardWidth):
			testString = testString + '{:d}'.format(self.solver.Value(self.cellValues[rowIndex][colIndex]))
	return testString
	
def listCandidates(self):
	if self.boardWidth != 9:
		print('Candidate listing only implemented for 9x9 boards for now')
		sys.exit()
	if len(self.digits) == 9:
		dPerLine = 3
		numLines = 3
	elif len(self.digits) == 10:
		dPerLine = 5
		numLines = 2
	print('-'*(1+(dPerLine+1)*self.boardWidth))
	for i in range(self.boardWidth):
		rowCand = [self.listCellCandidates(i,j,True) for j in range(self.boardWidth)]
		for j in range(numLines):
			print('|',end='')
			for k in range(self.boardWidth):
				print(''.join(rowCand[k][dPerLine*j:dPerLine*j+dPerLine])+'|',end='')
			print()
		print('-'*(1+(dPerLine+1)*self.boardWidth))
	
	print('To avoid retesting these cases when adding new constraints, add this code:')
	print('addExcludedDigitArray([' + ','.join(list(map(lambda s: ''.join(s),self.candToExclude))) + '])')
	return self.candToExclude
	
def addExcludedDigit(self,row,col=-1,value=-1):
	# Strictly for listing candidates, sets a value that has been excluded from a cell
	if col == -1:
		(row,col,value) = self._procCell(row)
	digitList = list(self.digits)
	self.candTests[row][col][digitList.index(value)] = False
	
def addExcludedDigitArray(self,list):
	for x in list: self.addExcludedDigit(x)

def listCellCandidates(self,row,col=-1,quiet=False):
	if col == -1:
		(row,col) = self._procCell(row)
		
	good = []
	digitList = list(self.digits)
	for k in range(len(digitList)):
		x = digitList[k]
		if self.candTests[row][col][k] is None:
			myCon = self.model.Add(self.cellValues[row][col] == x)
			self.applyNegativeConstraints()
			solver = cp_model.CpSolver()
			solveStatus = solver.Solve(self.model)
			if solveStatus == cp_model.OPTIMAL:
				good.append('{:d}'.format(x))
				for i in range(self.boardWidth):
					for j in range(self.boardWidth):
						self.candTests[i][j][digitList.index(solver.Value(self.cellValues[i][j]))] = True
			else:
				self.candTests[row][col][k] = False
				self.candToExclude.append([str(row+1),str(col+1),str(x)])
				good.append(' ')
			myCon.Proto().Clear()
		elif self.candTests[row][col][k] is True:
			good.append('{:d}'.format(x))
		elif self.candTests[row][col][k] is False:
			good.append(' ')
	if quiet is False:
		print('Possible values for cell {:d},{:d}: '.format(row+1,col+1) + ''.join(good))
	return good