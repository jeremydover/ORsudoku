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

class crustSandwichSudoku(sudoku):
	"""A class used to implement crust puzzles, where two cells per row/column (and optionally region) are designated crusts of a sandwich, and sandwich clues refer to the digits between the crusts."""	
	
	def __init__(self,boardSizeRoot,enforceRegions=True,includeCrust=False,irregular=None,digitSet=None):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot
		self.enforceRegions = enforceRegions

		self._constraintInitialized = []
		self._constraintNegative = []
		self._propertyInitialized = []
		
		if digitSet is None:
			self.digits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit

		self.model = cp_model.CpModel()
		self.cellValues = [] 
		self.allVars = []
		self.candTests = [[[None for k in range(len(self.digits))] for j in range(self.boardWidth)] for i in range(self.boardWidth)]
		self.candToExclude=[]
		
		# Create the variables containing the cell values
		# Create the variables containing the cell values
		for rowIndex in range(self.boardWidth):
			tempArray = []
			for colIndex in range(self.boardWidth):
				tempCell = self.model.NewIntVar(self.minDigit,self.maxDigit,'cellValue{:d}{:d}'.format(rowIndex,colIndex))
				if (self.maxDigit - self.minDigit) >= self.boardWidth:	#Digit set is not continguous, so force values
					self.model.AddAllowedAssignments([tempCell],[(x,) for x in digitSet])
				tempArray.append(tempCell)
				self.allVars.append(tempCell)
			self.cellValues.insert(rowIndex,tempArray)
						
		# Create rules to ensure rows and columns have no repeats for the digits
		for rcIndex in range(self.boardWidth):
			self.model.AddAllDifferent([self.cellValues[rcIndex][crIndex] for crIndex in range(self.boardWidth)]) 	# Rows
			self.model.AddAllDifferent([self.cellValues[crIndex][rcIndex] for crIndex in range(self.boardWidth)]) 	# Columns

		# Now the crusts. How to do this? So let's start with a 9x9 array of "is crust?" Booleans, and reified integers, so we
		# can count per row/column/region
		self.crust = []
		self.crustInt = []
	
		for i in range(self.boardWidth):
			tempCrustArray = []
			tempCrustIntArray = []
			for j in range(self.boardWidth):
				c = self.model.NewBoolVar('crust{:d}{:d}'.format(i,j))
				d = self.model.NewIntVar(0,1,'crustInt{:d}{:d}'.format(i,j))
				self.model.Add(d == 1).OnlyEnforceIf(c)
				self.model.Add(d == 0).OnlyEnforceIf(c.Not())
				tempCrustArray.append(c)
				tempCrustIntArray.append(d)
			self.crust.insert(i,tempCrustArray)
			self.crustInt.insert(i,tempCrustIntArray)

		# Count crusts per row/column
		for i in range(self.boardWidth):
			self.model.Add(sum(self.crustInt[i][j] for j in range(self.boardWidth)) == 2)
			self.model.Add(sum(self.crustInt[j][i] for j in range(self.boardWidth)) == 2)

		# NOW deal with regions. Default to boxes. Needed to get all variables set up.
		self.regions = []
		if irregular is None:
			self.__setBoxes()

		# Alright, we now have crust cells defined. It's tempting to convert locations to indices, but we don't actually need that. We just need
		# sandwich sum variables, since we can force the sum equation with the Booleans!
		minSum = sum(x for x in self.digits if x <= 0)
		maxSum = sum(x for x in self.digits if x >= 0)
		
		self.sandwichSum = [[self.model.NewIntVar(minSum,maxSum,'rowSandwich{:d}'.format(i)) for i in range(self.boardWidth)],
			               [self.model.NewIntVar(minSum,maxSum,'colSandwich{:d}'.format(i)) for i in range(self.boardWidth)]]

		for i in range(self.boardWidth):
			# Working in row/column i
			for j in range(self.boardWidth):
				for k in range(j+1,self.boardWidth):
					# Crusts are in positions j and k
					if includeCrust:
						self.model.Add(self.sandwichSum[0][i] == sum(self.cellValues[i][m] for m in range(self.boardWidth) if (m >= j and m <= k))).OnlyEnforceIf([self.crust[i][j],self.crust[i][k]])
						self.model.Add(self.sandwichSum[1][i] == sum(self.cellValues[m][i] for m in range(self.boardWidth) if (m >= j and m <= k))).OnlyEnforceIf([self.crust[j][i],self.crust[k][i]])
					else:
						self.model.Add(self.sandwichSum[0][i] == sum(self.cellValues[i][m] for m in range(self.boardWidth) if (m > j and m < k))).OnlyEnforceIf([self.crust[i][j],self.crust[i][k]])
						self.model.Add(self.sandwichSum[1][i] == sum(self.cellValues[m][i] for m in range(self.boardWidth) if (m > j and m < k))).OnlyEnforceIf([self.crust[j][i],self.crust[k][i]])
			
	def __setBoxes(self):
		# Create rules to ensure boxes have no repeats and there are two crusts per box, if enforced
		for rowBox in range(self.boardSizeRoot):
			for colBox in range(self.boardSizeRoot):
				tempCellArray = []
				tempCellIndexArray = []
				tempCrustArray = []
				for rowIndex in range(self.boardSizeRoot):
					for colIndex in range(self.boardSizeRoot):
						tempCellArray.append(self.cellValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
						tempCellIndexArray.append((self.boardSizeRoot*rowBox+rowIndex,self.boardSizeRoot*colBox+colIndex))
						tempCrustArray.append(self.crustInt[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
				self.model.AddAllDifferent(tempCellArray)	# Ensures square regions have all different values
				self.regions.append(tempCellIndexArray)			# Set squares up as regions for region sum rules
				if self.enforceRegions:
					self.model.Add(sum(tempCrustArray) == 2)	# Ensure there are two crusts per square
				
	def setRegion(self,inlist):
		# Allow setting of irregular regions
		inlist = self._procCellList(inlist)
		self.regions.append(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in self.regions[-1]])
		if self.enforceRegions:
			self.model.Add(sum(self.crustInt[x[0]][x[1]] for x in inlist) == 1)	# Ensure one doubler per region

	def setSandwichSum(self,row1,col1,rc,value):
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		
		self.model.Add(self.sandwichSum[rc][row if rc == self.Row else col] == value)
		
	def setCrustHasLength(self):
		for i in range(self.boardWidth):
			# Working in row/column i
			c = self.model.NewBoolVar('rowLengthTest{:d}'.format(i))
			d = self.model.NewBoolVar('colLengthTest{:d}'.format(i))
			for j in range(self.boardWidth):
				for k in range(j+1,self.boardWidth):
					self.model.Add(self.cellValues[i][j] == k-j-1).OnlyEnforceIf([self.crust[i][j],self.crust[i][k],c])
					self.model.Add(self.cellValues[i][k] == k-j-1).OnlyEnforceIf([self.crust[i][j],self.crust[i][k],c.Not()])
					self.model.Add(self.cellValues[j][i] == k-j-1).OnlyEnforceIf([self.crust[j][i],self.crust[k][i],d])
					self.model.Add(self.cellValues[k][i] == k-j-1).OnlyEnforceIf([self.crust[j][i],self.crust[k][i],d.Not()])
				
	def printCurrentSolution(self):
		dW = max([len(str(x)) for x in self.digits])
		colorama.init()
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if self.solver.Value(self.crustInt[i][j]) == 1: # This one is doubled!
					print(Fore.RED + '{:d}'.format(self.solver.Value(self.cellValues[i][j])).rjust(dW) + Fore.RESET,end = " ")
				else:
					print('{:d}'.format(self.solver.Value(self.cellValues[i][j])).rjust(dW),end = " ")
			print()
		print()
		
	def testStringSolution(self):
		testString = ''
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if self.solver.Value(self.crustInt[i][j]) == 1: # This one is doubled!
					testString = testString + '*{:d}*'.format(self.solver.Value(self.cellValues[i][j]))
				else:
					testString = testString + '{:d}'.format(self.solver.Value(self.cellValues[i][j]))
		return testString
		
	def preparePrintVariables(self):
		consolidatedCellValues = []
		for tempArray in self.cellValues:
			consolidatedCellValues = consolidatedCellValues + tempArray
		for tempArray in self.crustInt:
			consolidatedCellValues = consolidatedCellValues + tempArray
		return consolidatedCellValues