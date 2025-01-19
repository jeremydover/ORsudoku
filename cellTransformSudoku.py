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

class cellTransformSudoku(sudoku):
	"""A class used to implement doubler puzzles. A doubler puzzle has a doubler in each row, column and region. Moreover, each digit is doubled exactly one time. The digit entered is used to determine normal Sudoku contraints, i.e., one of each digit per row, column and region. But for each other constraint, its value needs to be doubled. There are optional parameters to modify the operation from doubling to an arbitrary ratio and/or shift."""	
	
	def __init__(self,boardSizeRoot,canRepeatDigits=False,irregular=None,digitSet=None):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot

		self.isBattenburgInitialized = False
		self.isBattenburgNegative = False
		
		self.isKropkiInitialized = False
		self.isKropkiNegative = False
		self.kropkiDiff = 1
		self.kropkiRatio = 2
		
		self.isFriendlyInitialized = False
		self.isFriendlyNegative = False
		
		self.isRossiniInitialized = False
		self.isRossiniNegative = False
		self.rossiniLength = -1
		self.outsideLength = -1
		
		self.isXVInitialized = False
		self.isXVNegative = False
		
		self.isXVXVInitialized = False
		self.isXVXVNegative = False
		
		self.isXYDifferenceInitialized = False
		self.isXYDifferenceNegative = False
		
		self.isEntropyQuadInitialized = False
		self.isEntropyQuadNegative = False
					
		self.isModularQuadInitialized = False
		self.isModularQuadNegative = False

		self.isEntropyBattenburgInitialized = False
		self.isEntropyBattenburgNegative = False
		
		self.isConsecutiveQuadInitialized = False
		self.isConsecutiveQuadNegative = False
		
		self.isParityQuadInitialized = False
		self.isParityQuadNegative = False
		self.parityQuadExcluded = [0,4]
		
		self.isParity = False
		self.isEntropy = False
		self.isModular = False
		self.isFullRank = False
		self.isPrimality = False
		
		if digitSet is None:
			self.baseDigits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.baseDigits = digitSet
		self.maxDigit = max(self.baseDigits)
		self.minDigit = min(self.baseDigits)
		self.digitRange = self.maxDigit - self.minDigit

		self.model = cp_model.CpModel()
		self.cellValues = [] 		# Since this array is used throughout for the constraints, we'll make this the modified
		self.baseValues = []
		cellValueSet = set(self.baseDigits)
		for x in self.baseDigits:
			cellValueSet = cellValueSet.union(self.transformDoublerValue(x))
		self.digits = cellValueSet

		self.allVars = []
		self.candTests = [[[None for k in range(len(self.baseDigits))] for j in range(self.boardWidth)] for i in range(self.boardWidth)]
		self.candToExclude=[]
		
		# Create the variables containing the cell values
		for rowIndex in range(self.boardWidth):
			tempArrayCell = []
			tempArrayBase = []
			for colIndex in range(self.boardWidth):
				tempBase = self.model.NewIntVar(self.minDigit,self.maxDigit,'cellBase{:d}{:d}'.format(rowIndex,colIndex))
				tempCell = self.model.NewIntVar(min(cellValueSet),max(cellValueSet),'cellValue{:d}{:d}'.format(rowIndex,colIndex))
				if (self.maxDigit - self.minDigit) >= self.boardWidth:	# If base digit set is not continguous, force values
					self.model.AddAllowedAssignments([tempBase],[(x,) for x in self.digits])
					# Note: no need to force values on cellValues, because they will be tied to base
				tempArrayCell.append(tempCell)
				tempArrayBase.append(tempBase)
			self.cellValues.insert(rowIndex,tempArrayCell)
			self.baseValues.insert(rowIndex,tempArrayBase)
						
		# Create rules to ensure rows and columns have no repeats for the BASE digits
		for rcIndex in range(self.boardWidth):
			self.model.AddAllDifferent([self.baseValues[rcIndex][crIndex] for crIndex in range(self.boardWidth)]) 	# Rows
			self.model.AddAllDifferent([self.baseValues[crIndex][rcIndex] for crIndex in range(self.boardWidth)]) 	# Columns

		# Now the doubling stuff
		self.double = []
	
		for i in range(self.boardWidth):
			tempDoubleArray = []
			for j in range(self.boardWidth):
				c = self.model.NewBoolVar('double{:d}{:d}'.format(i,j))
				tempDoubleArray.append(c)
			self.double.insert(i,tempDoubleArray)
		
		# Finally, create integer versions of doubling variables to check conditions
		self.doubleInt = []
  
		for i in range(self.boardWidth):
			tempDoubleArray = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(0,1,'doubleInt{:d}{:d}'.format(i,j))
				tempDoubleArray.append(c)
			self.doubleInt.insert(i,tempDoubleArray)
		
		# Doubling conditions
		
		# First we tie the values of the underlying digits to their apparent values: we function this out so we can override for other cases
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				self.transformDoublerCell(i,j)
				self.model.Add(self.cellValues[i][j] == self.baseValues[i][j]).OnlyEnforceIf([self.double[i][j].Not()])
			
		# Now tie double and doubleInt variables
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				self.model.Add(self.doubleInt[i][j] == 1).OnlyEnforceIf([self.double[i][j]])
				self.model.Add(self.doubleInt[i][j] == 0).OnlyEnforceIf([self.double[i][j].Not()])
			
		# Now we ensure there is only one doubler per row, column, and box
		for i in range(self.boardWidth):
			self.model.Add(sum(self.doubleInt[i][j] for j in range(self.boardWidth)) == 1)
			self.model.Add(sum(self.doubleInt[j][i] for j in range(self.boardWidth)) == 1)

		# NOW deal with regions. Default to boxes. Needed to get all variables set up.
		self.regions = []
		if irregular is None:
			self.__setBoxes()
	
		# The ugly part: ensuring all doubled digits are distinct
		if canRepeatDigits is False:
			for i in range(self.boardWidth):
				for j in range(self.boardWidth):
					for k in range(self.boardWidth):
						for l in range(self.boardWidth):
							if k>i or l>j:
								self.model.Add(self.baseValues[i][j] != self.baseValues[k][l]).OnlyEnforceIf([self.double[i][j],self.double[k][l]]) 

	def transformDoublerCell(self,i,j):
		# We default to the original doubler rules
		self.model.Add(self.cellValues[i][j] == 2*self.baseValues[i][j]).OnlyEnforceIf([self.double[i][j]])
		
	def transformDoublerValue(self,value):
		# Default to the original doubler rules
		return {2*value}
			
	def __setBoxes(self):
		# Create rules to ensure boxes have no repeats in the BASE digits
		for rowBox in range(self.boardSizeRoot):
			for colBox in range(self.boardSizeRoot):
				tempBaseArray = []
				tempCellArray = []
				tempCellIndexArray = []
				tempDoubleArray = []
				for rowIndex in range(self.boardSizeRoot):
					for colIndex in range(self.boardSizeRoot):
						tempBaseArray.append(self.baseValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
						tempCellArray.append(self.cellValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
						tempCellIndexArray.append((self.boardSizeRoot*rowBox+rowIndex,self.boardSizeRoot*colBox+colIndex))
						tempDoubleArray.append(self.doubleInt[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
				self.model.AddAllDifferent(tempBaseArray)	# Ensures square regions have all different values
				self.regions.append(tempCellIndexArray)			# Set squares up as regions for region sum rules
				self.model.Add(sum(tempDoubleArray) == 1)	# Ensure there is only one doubler per square
				
	def setRegion(self,inlist):
		# Allow setting of irregular regions
		inlist = self._procCellList(inlist)
		self.regions.append(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in self.regions[-1]])
		self.model.Add(sum(self.doubleInt[x[0]][x[1]] for x in inlist) == 1)	# Ensure one doubler per region
				
	def setTransform(self,row,col=-1):
		if col == -1:
			(row,col) = self._procCell(row)
		self.model.AddBoolAnd([self.double[row][col]])
	
	def setNotTransform(self,row,col=-1):
		if col == -1:
			(row,col) = self._procCell(row)
		self.model.AddBoolAnd([self.double[row][col].Not()])
	
	def setGiven(self,row,col=-1,value=-1):
		if col == -1:
			(row,col,value) = self._procCell(row)
		self.model.Add(self.baseValues[row][col] == value)
		
	def printCurrentSolution(self):
		dW = max([len(str(x)) for x in self.digits])
		colorama.init()
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if self.solver.Value(self.doubleInt[i][j]) == 1: # This one is doubled!
					print(Fore.RED + '{:d}'.format(self.solver.Value(self.baseValues[i][j])).rjust(dW) + Fore.RESET,end = " ")
				else:
					print('{:d}'.format(self.solver.Value(self.baseValues[i][j])).rjust(dW),end = " ")
			print()
		print()
		
	def testStringSolution(self):
		testString = ''
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if self.solver.Value(self.doubleInt[i][j]) == 1: # This one is doubled!
					testString = testString + '*{:d}*'.format(self.solver.Value(self.baseValues[i][j]))
				else:
					testString = testString + '{:d}'.format(self.solver.Value(self.baseValues[i][j]))
		return testString
		
	def listCandidates(self):
		if self.boardWidth != 9:
			print('Candidate listing only implemented for 9x9 boards for now')
			sys.exit()
		if len(self.baseDigits) == 9:
			dPerLine = 3
			numLines = 3
		elif len(self.baseDigits) == 10:
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
		
	def addExcludedDigit(self,row,col=-1,value=-1):
		# Strictly for listing candidates, sets a value that has been excluded from a cell
		if col == -1:
			(row,col,value) = self._procCell(row)
		self.candTests[row][col][value-1] = False
		
	def addExcludedDigitArray(self,list):
		for x in list: self.addExcludedDigit(x)
	
	def listCellCandidates(self,row,col=-1,quiet=False):
		if col == -1:
			(row,col) = self._procCell(row)
			
		good = []
		digitList = list(self.baseDigits)
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
							self.candTests[i][j][digitList.index(solver.Value(self.baseValues[i][j]))] = True
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
		else:
			return good
			
	def preparePrintVariables(self):
		consolidatedCellValues = []
		for tempArray in self.baseValues:
			consolidatedCellValues = consolidatedCellValues + tempArray
		for tempArray in self.doubleInt:
			consolidatedCellValues = consolidatedCellValues + tempArray
		return consolidatedCellValues

class doublerSudoku(cellTransformSudoku):

	def __init__(self,boardSizeRoot,canRepeatDigits=False,irregular=None,digitSet=None):
		cellTransformSudoku.__init__(self,boardSizeRoot,canRepeatDigits=canRepeatDigits,irregular=irregular,digitSet=digitSet)
		
class negatorSudoku(cellTransformSudoku):
	
	def __init__(self,boardSizeRoot,canRepeatDigits=False,irregular=None,digitSet=None):
		cellTransformSudoku.__init__(self,boardSizeRoot,canRepeatDigits=canRepeatDigits,irregular=irregular,digitSet=digitSet)
		
	def transformDoublerCell(self,i,j):
		self.model.Add(self.cellValues[i][j] == -1*self.baseValues[i][j]).OnlyEnforceIf([self.double[i][j]])
		
	def transformDoublerValue(self,value):
		return {-1*value}
		
class doubleOrNothingSudoku(cellTransformSudoku):
	
	def __init__(self,boardSizeRoot,canRepeatDigits=False,irregular=None,digitSet=None):
		cellTransformSudoku.__init__(self,boardSizeRoot,canRepeatDigits=canRepeatDigits,irregular=irregular,digitSet=digitSet)
		
	def transformDoublerCell(self,i,j):
		c = self.model.NewBoolVar('doublerCellDoubledorNothing')
		self.model.Add(self.cellValues[i][j] == 2*self.baseValues[i][j]).OnlyEnforceIf([self.double[i][j],c])
		self.model.Add(self.cellValues[i][j] == 0).OnlyEnforceIf([self.double[i][j],c.Not()])
		self.model.AddBoolAnd([c]).OnlyEnforceIf([self.double[i][j].Not()])
		
	def transformDoublerValue(self,value):
		return {0,2*value}
		
class doubleOrNegativeSudoku(cellTransformSudoku):
	
	def __init__(self,boardSizeRoot,canRepeatDigits=False,irregular=None,digitSet=None):
		cellTransformSudoku.__init__(self,boardSizeRoot,canRepeatDigits=canRepeatDigits,irregular=irregular,digitSet=digitSet)
		
	def transformDoublerCell(self,i,j):
		c = self.model.NewBoolVar('doublerCellDoubledorNegative')
		self.model.Add(self.cellValues[i][j] == 2*self.baseValues[i][j]).OnlyEnforceIf([self.double[i][j],c])
		self.model.Add(self.cellValues[i][j] == -1*self.baseValues[i][j]).OnlyEnforceIf([self.double[i][j],c.Not()])
		self.model.AddBoolAnd([c]).OnlyEnforceIf([self.double[i][j].Not()])
		
	def transformDoublerValue(self,value):
		return {-1*value,2*value}
		
class affineTransformSudoku(cellTransformSudoku):
	
	def __init__(self,boardSizeRoot,ratio,shift,canRepeatDigits=False,irregular=None,digitSet=None):
		self.ratio = ratio
		self.shift = shift
		cellTransformSudoku.__init__(self,boardSizeRoot,canRepeatDigits=canRepeatDigits,irregular=irregular,digitSet=digitSet)
		
	def transformDoublerCell(self,i,j):
		self.model.Add(self.cellValues[i][j] == self.ratio*self.baseValues[i][j]+self.shift).OnlyEnforceIf([self.double[i][j]])
		
	def transformDoublerValue(self,value):
		return {self.ratio*value+self.shift}