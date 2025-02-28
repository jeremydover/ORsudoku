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

class starBattleSudoku(sudoku):
	"""A class used to implement star battle/sudoku hybrid puzzles."""	
	
	def __init__(self,boardSizeRoot,irregular=None,digitList=[1,2,3,4,5,6,7,0,0],starSymbols=[],numberOfStars=None):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot
		
		self._constraintInitialized = []
		self._constraintNegative = []
		self._propertyInitialized = []
		
		self.digitList = digitList
		self.digits = set(digitList)
		self.digitOrdinal = list(self.digits) # Converting this back to a list squashes repeats
		self.digitOrdinalCount = [digitList.count(self.digitOrdinal[k]) for k in range(len(self.digitOrdinal))]
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit
		
		self.model = cp_model.CpModel()
		self.cellValues = [] 		# Since this array is used throughout for the constraints, we use this to contain the numerical value
		self.baseValues = []		# We'll use this array to track the ordinal of the digit that appears in this cell

		self.allVars = []
		self.candTests = [[[None for k in range(len(self.digits))] for j in range(self.boardWidth)] for i in range(self.boardWidth)]
		self.candToExclude=[]
		
		# Arrays to determine which digits are stars. If set explicitly via starSymbols, force here. This allows ambiguity.
		self.isStarDigit = [self.model.NewBoolVar('StarDigits') for k in range(len(self.digitOrdinal))]
		self.model.AddBoolAnd([self.isStarDigit[k] for k in range(len(self.digitOrdinal)) if self.digitOrdinal[k] in starSymbols])
		
		# Calculate number of stars from digit list and star symbols, of not given
		if numberOfStars is None:
			self.numberOfStars = sum(digitList.count(x) for x in starSymbols)
		else:
			self.numberOfStars = numberOfStars

		
		# Star Battle tracking arrays
		self.isStarCell = []		# Boolean to track if a given cell is a star cell or not
		self.isStarCellInt = []		# Reified versions
		
		# Create the variables containing the cell values
		for rowIndex in range(self.boardWidth):
			tempArrayCell = []
			tempArrayBase = []
			tempArrayStar = []
			tempArrayStarInt = []
			for colIndex in range(self.boardWidth):
				tempBase = self.model.NewIntVar(0,len(self.digitOrdinal)-1,'cellBase{:d}{:d}'.format(rowIndex,colIndex))
				tempCell = self.model.NewIntVar(self.minDigit,self.maxDigit,'cellValue{:d}{:d}'.format(rowIndex,colIndex))
				tempStar = self.model.NewBoolVar('isStarCell{:d}{:d}'.format(rowIndex,colIndex))
				tempStarInt = self.model.NewIntVar(0,1,'isStarCellInt{:d}{:d}'.format(rowIndex,colIndex))
				self.model.Add(tempStarInt == 1).OnlyEnforceIf(tempStar)
				self.model.Add(tempStarInt == 0).OnlyEnforceIf(tempStar.Not())
				tempArrayCell.append(tempCell)
				tempArrayBase.append(tempBase)
				tempArrayStar.append(tempStar)
				tempArrayStarInt.append(tempStarInt)
			self.cellValues.insert(rowIndex,tempArrayCell)
			self.baseValues.insert(rowIndex,tempArrayBase)
			self.isStarCell.insert(rowIndex,tempArrayStar)
			self.isStarCellInt.insert(rowIndex,tempArrayStarInt)
			
		# I *think* this is the best way to do this. We need a massive array of bools, and a corresponding reified integer array, such
		# that a[i][j][k] means cellValues[i][j]==digitOrdinal[k]. Ugh...ly.
		
		self.cellDigit = []
		self.cellDigitInts = []
		for i in range(self.boardWidth):
			tempArrayDigit1 = []
			tempArrayInt1 = []
			for j in range(self.boardWidth):
				tempArrayDigit2 = []
				tempArrayInt2 = []
				for k in range(len(self.digitOrdinal)):
					b = self.model.NewBoolVar('cellDigit{:d}{:d}{:d}'.format(i,j,k))
					c = self.model.NewIntVar(0,1,'cellDigitInt{:d}{:d}{:d}'.format(i,j,k))
					self.model.Add(c == 1).OnlyEnforceIf(b)
					self.model.Add(c == 0).OnlyEnforceIf(b.Not())
					self.model.Add(self.baseValues[i][j] == k).OnlyEnforceIf(b)
					self.model.Add(self.baseValues[i][j] != k).OnlyEnforceIf(b.Not())
					self.model.Add(self.cellValues[i][j] == self.digitOrdinal[k]).OnlyEnforceIf(b)
					self.model.Add(self.cellValues[i][j] != self.digitOrdinal[k]).OnlyEnforceIf(b.Not())
					tempArrayDigit2.append(b)
					tempArrayInt2.append(c)
				tempArrayDigit1.insert(j,tempArrayDigit2)
				tempArrayInt1.insert(j,tempArrayInt2)
			self.cellDigit.insert(i,tempArrayDigit1)
			self.cellDigitInts.insert(i,tempArrayInt1)
			
		# OK, now we CAN have repeats in rows, columns and regions. Pain in the patootie. So we need to count number of appearances and compare it to the number of times the symbol appears in digit list. Also, we ensure the number of stars per area is correct.
		
		for i in range(self.boardWidth):
			for k in range(len(self.digitOrdinal)):
				self.model.Add(sum(self.cellDigitInts[i][j][k] for j in range(self.boardWidth)) == self.digitOrdinalCount[k])
				self.model.Add(sum(self.cellDigitInts[j][i][k] for j in range(self.boardWidth)) == self.digitOrdinalCount[k])
			self.model.Add(sum(self.isStarCellInt[i][j] for j in range(self.boardWidth)) == self.numberOfStars)
			self.model.Add(sum(self.isStarCellInt[j][i] for j in range(self.boardWidth)) == self.numberOfStars)
		
		# NOW deal with regions. Default to boxes. Ensuring correct number of symbols per box/region is taken care of in the appropriate call.
		self.regions = []
		if irregular is None:
			self.__setBoxes()
			
		# Now do the star battle stuff
		#self.starOrdinals = [k for k in range(len(self.digitOrdinal)) if self.digitOrdinal[k] in starSymbols]
		#for i in range(self.boardWidth):
		#	for j in range(self.boardWidth):
		#		neighbors = {(i+x,j+y) for x in range(-1,2) for y in range(-1,2) if x != 0 or y !=0} & {(k,m) for k in range(self.boardWidth) #			for m in range(self.boardWidth)}
		#		for x in self.starOrdinals:
		#			self.model.AddBoolAnd([self.cellDigit[y[0]][y[1]][m].Not() for y in neighbors for m in self.starOrdinals]).OnlyEnforceIf(self.cellDigit[i][j][x])
		
		# Now RE-do the star battle stuff with ambiguity. Already counted star cells per row/box/region.
		# First, tie star cell determination to digits
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				for k in range(len(self.digitOrdinal)):
					self.model.AddBoolAnd(self.isStarCell[i][j]).OnlyEnforceIf([self.cellDigit[i][j][k],self.isStarDigit[k]])
					self.model.AddBoolAnd(self.isStarCell[i][j].Not()).OnlyEnforceIf([self.cellDigit[i][j][k],self.isStarDigit[k].Not()])
					
		# Now ensure no neighbors
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				neighbors = {(i+x,j+y) for x in range(-1,2) for y in range(-1,2) if x != 0 or y !=0} & {(k,m) for k in range(self.boardWidth) for m in range(self.boardWidth)}
				self.model.AddBoolAnd([self.isStarCell[x[0]][x[1]].Not() for x in neighbors]).OnlyEnforceIf(self.isStarCell[i][j])
					
	def __setBoxes(self):
		# Create rules to ensure boxes have no repeats in the BASE digits
		for rowBox in range(self.boardSizeRoot):
			for colBox in range(self.boardSizeRoot):
				tempCellIndexArray = []
				for rowIndex in range(self.boardSizeRoot):
					for colIndex in range(self.boardSizeRoot):
						tempCellIndexArray.append((self.boardSizeRoot*rowBox+rowIndex,self.boardSizeRoot*colBox+colIndex))
				for k in range(len(self.digitOrdinal)):
					self.model.Add(sum(self.cellDigitInts[x[0]][x[1]][k] for x in tempCellIndexArray) == self.digitOrdinalCount[k])
				self.model.Add(sum(self.isStarCellInt[x[0]][x[1]] for x in tempCellIndexArray) == self.numberOfStars)
				self.regions.append(tempCellIndexArray)			# Set squares up as regions for region sum rules
				
	def setRegion(self,inlist):
		# Allow setting of irregular regions
		inlist = self._procCellList(inlist)
		self.regions.append(inlist)
		for k in range(len(self.digitOrdinal)):
			self.model.Add(sum(self.cellDigitInts[x[0]][x[1]][k] for x in inlist) == self.digitOrdinalCount[k])
		self.model.Add(sum(self.isStarCellInt[x[0]][x[1]] for x in inlist) == self.numberOfStars)
				
	def printCurrentSolution(self):
		dW = max([len(str(x)) for x in self.digits])
		colorama.init()
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if self.solver.Value(self.isStarCell[i][j]) == 1: # This one is a star
					print(Fore.RED + '{:d}'.format(self.solver.Value(self.cellValues[i][j])).rjust(dW) + Fore.RESET,end = " ")
				else:
					print('{:d}'.format(self.solver.Value(self.cellValues[i][j])).rjust(dW),end = " ")
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
		for tempArray in self.cellValues:
			consolidatedCellValues = consolidatedCellValues + tempArray
		return consolidatedCellValues