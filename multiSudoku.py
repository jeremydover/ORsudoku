from __future__ import print_function
from __future__ import print_function
import sys
import math
import colorama
from ORsudoku import sudoku
from ortools.sat.python import cp_model
from array import *
from colorama import Fore,Back,init
init()

class multiSudoku(sudoku):
	"""A class to abstract a couple of utility functions that will be useful for all multi-sudokus, because they do share a lot of code"""
	
	def __init__(self,numberOfPuzzles,boardSizeRoot,irregular=None,digitSet=None):
		self.numberOfPuzzles = numberOfPuzzles
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot

		if digitSet is None:
			self.digits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit
		self._propertyInitialized = []

		self.model = cp_model.CpModel()
		self.subgrids = [sudoku(boardSizeRoot,irregular=irregular,digitSet=self.digits,model=self.model) for i in range(self.numberOfPuzzles)]
		
	def setMultiConstraint(self,puzz,constraint,args):
		getattr(self.subgrids[puzz-1],'set'+constraint)(*args)
		
	def setMultiRegion(self,puzz,inlist):
		self.subgrids[puzz-1].setRegion(inlist)
		
	def _initializeCrossGridLines(self):
		if 'CrossGridLines' not in self._propertyInitialized:
			self._propertyInitialized.append('CrossGridLines')
			self.cellValues = [[self.model.NewIntVar(self.minDigit,self.maxDigit,'CrossGridReferenceVariables') for i in range(self.boardWidth*self.boardWidth)] for k in range(self.numberOfPuzzles)]
			for i in range(self.boardWidth):
				for j in range(self.boardWidth):
					for k in range(self.numberOfPuzzles):
						self.model.Add(self.cellValues[k][self.boardWidth*i + j] == self.subgrids[k].cellValues[i][j])
						
	def setCrossGridLine(self,constraint,inlist,args=[]):
		self._initializeCrossGridLines()
		inlist1 = self._procCellList(inlist)
		L = []
		for x in inlist1:
			L.append((x[0]+1,x[1]*self.boardWidth+x[2]))
		getattr(self,'set'+constraint)(*([L]+args))

	def _initializeParity(self):
		if 'Parity' not in self._propertyInitialized:
			self._setParity()
	
	def _setParity(self):
		# Set up variables to track parity constraints
		divVars = []
		self.cellParity = []
		
		maxDiff = self.maxDigit-self.minDigit
		for i in range(self.numberOfPuzzles):
			t = []
			for j in range(self.boardWidth*self.boardWidth):
				div = self.model.NewIntVar(0,2*maxDiff,'ParityDiv')
				mod = self.model.NewIntVar(0,1,'parityValue{:d}{:d}'.format(i,j))
				t.append(mod)
				self.model.Add(2*div <= self.cellValues[i][j])
				self.model.Add(2*div+2 > self.cellValues[i][j])
				self.model.Add(mod == self.cellValues[i][j]-2*div)
			self.cellParity.insert(i,t)
		
		self._propertyInitialized.append('Parity')
		
	def _initializeEntropy(self):
		if 'Entropy' not in self._propertyInitialized:
			self._setEntropy()
	
	def _setEntropy(self):
		# Set up variables to track entropy and modular constraints
		self.cellEntropy = []
		
		for i in range(self.numberOfPuzzles):
			t = []
			for j in range(self.boardWidth*self.boardWidth):
				c = self.model.NewIntVar(self.minDigit // 3 - 1,self.maxDigit // 3,'entropyValue{:d}{:d}'.format(i,j))
				t.append(c)
				self.model.Add(3*c+1 <= self.cellValues[i][j])
				self.model.Add(3*c+4 > self.cellValues[i][j])
			self.cellEntropy.insert(i,t)
		
		self._propertyInitialized.append('Entropy')
	
	def _initializeModular(self):
		if 'Modular' not in self._propertyInitialized:
			self._setModular()
	
	def _setModular(self):
		# Set up variables to track modular constraints
		if 'Entropy' not in self._propertyInitialized:
			self._setEntropy()
		
		self.cellModular = []
		
		for i in range(self.numberOfPuzzles):
			t = []
			for j in range(self.boardWidth*self.boardWidth):
				c = self.model.NewIntVar(1,3,'modularValue{:d}{:d}'.format(i,j))
				t.append(c)
				self.model.Add(c == self.cellValues[i][j] - 3*self.cellEntropy[i][j])
			self.cellModular.insert(i,t)
		
		self._propertyInitialized.append('Modular')
		
	def applyAllNegativeConstraints(self):
		for i in range(self.numberOfPuzzles):
			self.subgrids[i].applyNegativeConstraints()
	
	def preparePrintVariables(self):
		consolidatedCellValues = []
		for tempArray in [cell for x in self.subgrids for cell in x.cellValues]:
			consolidatedCellValues = consolidatedCellValues + tempArray
		return consolidatedCellValues
		
	def testStringSolution(self,value_source=None):
		if value_source is None:
			value_source = self.solver
		testString = ''
		for x in range(self.numberOfPuzzles):
			for i in range(self.boardWidth):
				for j in range(self.boardWidth):
					testString = testString + '{:d}'.format(value_source.Value(self.subgrids[x].getCellVar(i,j)))
		return testString
		
class doubleDoku(multiSudoku):
	"""A class used to implement DoubleDoku puzzles, where boxes 5/6/8/9 of puzzle 1 are boxes 1/2/4/5 of puzzle 2"""

	def __init__(self,boardSizeRoot,commonSize=None,irregular=None,digitSet=None):
		super().__init__(5,boardSizeRoot,irregular,digitSet)
		
		if commonSize is None:
			self.commonSize = boardSizeRoot
		else:
			self.commonSize = commonSize
		self.overlap = self.boardWidth-self.commonSize

	def __init__(self,boardSizeRoot,commonSize=None,irregular=None,digitSet=None):
		super().__init__(2,boardSizeRoot,irregular,digitSet)
		
		if commonSize is None:
			self.commonSize = boardSizeRoot
		else:
			self.commonSize = commonSize
		self.overlap = self.boardWidth-self.commonSize
		
		for i in range(self.overlap,self.boardWidth):
			for j in range(self.overlap,self.boardWidth):
				self.model.Add(self.subgrids[0].getCellVar(i,j) == self.subgrids[1].getCellVar(i-self.overlap,j-self.overlap))
		
	def setDoubleDokuConstraint(self,puzz,constraint,args):
		self.setMultiConstraint(puzz,constraint,args)

	def printCurrentSolution(self,value_source=None):
		if value_source is None:
			value_source = self.solver
		colorama.init()
		dW = max([len(str(x)) for x in self.digits])
		
		# First print board 1 rows, trailing board 2 as appropriate
		for i in range(self.boardWidth):
			# p1
			for j in range(self.boardWidth):
				if i < self.overlap or j < self.overlap:
					print('{:d}'.format(value_source.Value(self.subgrids[0].getCellVar(i,j))).rjust(dW),end = " ")
				else:
					print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[0].getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			
			# If there is p2 stuff after this
			if i >= self.overlap:
				for j in range(self.commonSize,self.boardWidth):
					print('{:d}'.format(value_source.Value(self.subgrids[1].getCellVar(i-self.overlap,j))).rjust(dW),end = " ")
			print()
			
		# Remainder of p2
		for i in range(self.commonSize,self.boardWidth):
			print (' '*((1+dW)*self.overlap), end = "")
			for j in range(self.boardWidth):
				print('{:d}'.format(value_source.Value(self.subgrids[1].getCellVar(i,j))).rjust(dW),end = " ")
			print()
			
class samuraiSudoku(multiSudoku):
	"""A class used to implement Samurai Sudoku puzzles."""

	def __init__(self,boardSizeRoot,commonSize=None,irregular=None,digitSet=None):
		super().__init__(5,boardSizeRoot,irregular,digitSet)
		
		if commonSize is None:
			self.commonSize = boardSizeRoot
		else:
			self.commonSize = commonSize
		self.overlap = self.boardWidth-self.commonSize
		for i in range(self.commonSize):
			for j in range(self.commonSize):
				self.model.Add(self.subgrids[0].getCellVar(self.overlap+i,self.overlap+j) == self.subgrids[2].getCellVar(i,j))
				self.model.Add(self.subgrids[1].getCellVar(self.overlap+i,j) == self.subgrids[2].getCellVar(i,self.overlap+j))
				self.model.Add(self.subgrids[3].getCellVar(i,self.overlap+j) == self.subgrids[2].getCellVar(self.overlap+i,j))
				self.model.Add(self.subgrids[4].getCellVar(i,j) == self.subgrids[2].getCellVar(self.overlap+i,self.overlap+j))
		
	def setSamuraiConstraint(self,puzz,constraint,args):
		self.setMultiConstraint(puzz,constraint,args)

	def printCurrentSolution(self,value_source=None):
		if value_source is None:
			value_source = self.solver
		colorama.init()
		dW = max([len(str(x)) for x in self.digits])
		# First print boards 1 and 2, and their overlap with board 3
		for i in range(self.boardWidth):
			# p1
			for j in range(self.boardWidth):
				if i < self.overlap or j < self.overlap:
					print('{:d}'.format(value_source.Value(self.subgrids[0].getCellVar(i,j))).rjust(dW),end = " ")
				else:
					print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[0].getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			# Between p1 and p2
			if i < self.overlap:
				print(' '*((1+dW)*(self.boardWidth-2*self.commonSize)),end = '')
			else:
				for j in range(self.commonSize,self.overlap):
					print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[2].getCellVar(i-self.overlap,j))).rjust(dW)+Fore.RESET,end = " ")

			# p2
			for j in range(self.boardWidth):
				if i < self.overlap or j >= self.commonSize:
					print('{:d}'.format(value_source.Value(self.subgrids[1].getCellVar(i,j))).rjust(dW),end = " ")
				else:
					print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[1].getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			print()
			
		# Now we're in the middle where we're printing just board 3
		for i in range(self.commonSize,self.overlap):
			print(' '*((1+dW)*self.overlap),end = '')
			for j in range(self.boardWidth):
				print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[2].getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			print()
				
		# Now the bottom two grids, p4 and p5
		for i in range(self.boardWidth):
			# p4
			for j in range(self.boardWidth):
				if i >= self.commonSize or j < self.overlap:
					print('{:d}'.format(value_source.Value(self.subgrids[3].getCellVar(i,j))).rjust(dW),end = " ")
				else:
					print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[3].getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			# Between p4 and p5
			if i < self.commonSize:
				for j in range(self.commonSize,self.overlap):
					print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[2].getCellVar(i+self.overlap,j))).rjust(dW)+Fore.RESET,end = " ")
			else:
				print(' '*((1+dW)*(self.boardWidth-2*self.commonSize)),end = '')
					
			# p5
			for j in range(self.boardWidth):
				if i >= self.commonSize or j >= self.commonSize:
					print('{:d}'.format(value_source.Value(self.subgrids[4].getCellVar(i,j))).rjust(dW),end = " ")
				else:
					print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[4].getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			print()
		print()

class soheiSudoku(multiSudoku):
	"""A class used to implement Sohei Sudoku puzzles."""

	def __init__(self,boardSizeRoot,commonSize=None,irregular=None,digitSet=None):
		super().__init__(4,boardSizeRoot,irregular,digitSet)
		if commonSize is None:
			self.commonSize = boardSizeRoot
		else:
			self.commonSize = commonSize
		self.overlap = self.boardWidth-self.commonSize
		
		for i in range(self.commonSize):
			for j in range(self.commonSize):
				self.model.Add(self.subgrids[0].getCellVar(self.overlap+i,j) == self.subgrids[1].getCellVar(i,self.overlap+j))
				self.model.Add(self.subgrids[0].getCellVar(self.overlap+i,self.overlap+j) == self.subgrids[2].getCellVar(i,j))
				self.model.Add(self.subgrids[1].getCellVar(self.overlap+i,self.overlap+j) == self.subgrids[3].getCellVar(i,j))
				self.model.Add(self.subgrids[2].getCellVar(self.overlap+i,j) == self.subgrids[3].getCellVar(i,self.overlap+j))
		
	def setSoheiConstraint(self,puzz,constraint,args):
		self.setMultiConstraint(puzz,constraint,args)
	
	def printCurrentSolution(self,value_source=None):
		if value_source is None:
			value_source = self.solver
		colorama.init()
		dW = max([len(str(x)) for x in self.digits])
		
		# p1
		for i in range(self.overlap):
			# Space before p1
			print(' '*((1+dW)*self.overlap),end = '')
			# p1
			for j in range(self.boardWidth):
				print('{:d}'.format(value_source.Value(self.subgrids[0].getCellVar(i,j))).rjust(dW),end = " ")
			print()

		#p2/p1/p3 rows
		for i in range(self.commonSize):
			#p2 cells
			for j in range(self.overlap):
				print('{:d}'.format(value_source.Value(self.subgrids[1].getCellVar(i,j))).rjust(dW),end = " ")
			#p1/p2 overlap
			for j in range(self.commonSize):
				print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[1].getCellVar(i,self.overlap+j))).rjust(dW)+Fore.RESET,end = " ")
			#p1 middle bottom
			for j in range(self.boardWidth-2*self.commonSize):
				print('{:d}'.format(value_source.Value(self.subgrids[0].getCellVar(self.overlap+i,self.commonSize+j))).rjust(dW),end = " ")
			#p1/p3 overlap
			for j in range(self.commonSize):
				print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[2].getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			#p3 cells
			for j in range(self.overlap):
				print('{:d}'.format(value_source.Value(self.subgrids[2].getCellVar(i,self.commonSize+j))).rjust(dW),end = " ")
			print()
		
		#Middle row
		for i in range(self.boardWidth-2*self.commonSize):
			#p2 cells
			for j in range(self.boardWidth):
				print('{:d}'.format(value_source.Value(self.subgrids[1].getCellVar(self.commonSize+i,j))).rjust(dW),end = " ")
			#hole
			print(' '*((1+dW)*(self.boardWidth-2*self.commonSize)),end = '')
			#p3 cells
			for j in range(self.boardWidth):
				print('{:d}'.format(value_source.Value(self.subgrids[2].getCellVar(self.commonSize+i,j))).rjust(dW),end = " ")
			print()
				
		#p2/p4/p3 rows
		for i in range(self.commonSize):
			#p2 cells
			for j in range(self.overlap):
				print('{:d}'.format(value_source.Value(self.subgrids[1].getCellVar(self.overlap+i,j))).rjust(dW),end = " ")
			#p2/p4 overlap
			for j in range(self.commonSize):
				print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[1].getCellVar(self.overlap+i,self.overlap+j))).rjust(dW)+Fore.RESET,end = " ")
			#p4 middle
			for j in range(self.boardWidth-2*self.commonSize):
				print('{:d}'.format(value_source.Value(self.subgrids[3].getCellVar(i,self.commonSize+j))).rjust(dW),end = " ")
			#p3/p4 overlap
			for j in range(self.commonSize):
				print(Fore.CYAN+'{:d}'.format(value_source.Value(self.subgrids[3].getCellVar(i,self.overlap+j))).rjust(dW)+Fore.RESET,end = " ")
			#p3 cells
			for j in range(self.overlap):
				print('{:d}'.format(value_source.Value(self.subgrids[2].getCellVar(self.overlap+i,self.commonSize+j))).rjust(dW),end = " ")
			print()
		
		for i in range(self.overlap):
			# Space before p4
			print(' '*((1+dW)*self.overlap),end = '')
			# p4
			for j in range(self.boardWidth):
				print('{:d}'.format(value_source.Value(self.subgrids[3].getCellVar(self.commonSize+i,j))).rjust(dW),end = " ")
			print()

