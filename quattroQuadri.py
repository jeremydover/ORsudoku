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

class quattroQuadri(sudoku):
	"""A class used to implement QuattroQuadri puzzles. A QQ is a 6-by-6 grid with four square regions. Digits are usually 1-9, and must be different in each row, column and box."""
	
	def __init__(self,blockSizeRoot=3,gridSize=2,irregular=None,digitSet={1,2,3,4,5,6,7,8,9}):
		self.boardSizeRoot = blockSizeRoot
		self.gridSize = gridSize
		self.boardWidth = gridSize*blockSizeRoot

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
		for rowIndex in range(self.boardWidth):
			tempArrayCell = []
			tempArrayBase = []
			for colIndex in range(self.boardWidth):
				tempCell = self.model.NewIntVar(self.minDigit,self.maxDigit,'cellValue{:d}{:d}'.format(rowIndex,colIndex))
				if (self.maxDigit - self.minDigit) >= self.boardWidth:	# If base digit set is not continguous, force values
					self.model.AddAllowedAssignments([tempCell],[(x,) for x in self.digits])
					# Note: no need to force values on cellValues, because they will be tied to base
				tempArrayCell.append(tempCell)
			self.cellValues.insert(rowIndex,tempArrayCell)
						
		# Create rules to ensure rows and columns have no repeats for the BASE digits
		for rcIndex in range(self.boardWidth):
			self.model.AddAllDifferent([self.cellValues[rcIndex][crIndex] for crIndex in range(self.boardWidth)]) 	# Rows
			self.model.AddAllDifferent([self.cellValues[crIndex][rcIndex] for crIndex in range(self.boardWidth)]) 	# Columns

		# NOW deal with regions. Default to boxes. Needed to get all variables set up.
		self.regions = []
		if irregular is None:
			self.__setBoxes()
		
	def __setBoxes(self):
		# Create rules to ensure boxes have no repeats
		for rowBox in range(self.gridSize):
			for colBox in range(self.gridSize):
				tempCellArray = []
				tempCellIndexArray = []
				for rowIndex in range(self.boardSizeRoot):
					for colIndex in range(self.boardSizeRoot):
						tempCellArray.append(self.cellValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
						tempCellIndexArray.append((self.boardSizeRoot*rowBox+rowIndex,self.boardSizeRoot*colBox+colIndex))
				self.model.AddAllDifferent(tempCellArray)					# Squares
				self.regions.append(tempCellIndexArray)
			
	def setRegion(self,inlist):
		# Allow setting of irregular regions
		inlist = self.__procCellList(inlist)
		self.regions.append(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in self.regions[-1]])
		
	def setEntropicKnightTour(self):
		tourRow = [self.model.NewIntVar(0,6,'') for i in range(36)]
		tourCol = [self.model.NewIntVar(0,6,'') for i in range(36)]
		
		for i in range(35):
			# Ensure all cells in tour are different
			for j in range(i+1,35):
				self.model.Add(6*tourRow[i]+tourCol[i] != 6*tourRow[j]+tourCol[j])
			
			# Ensure next cell is knight move. 8 possibilities, so 3 variables
			r1c2 = self.model.NewBoolVar('')
			rpm = self.model.NewBoolVar('')
			cpm = self.model.NewBoolVar('')
			self.model.Add(tourRow[(i+1) % 36] == tourRow[i]+1).OnlyEnforceIf([r1c2,rpm])
			self.model.Add(tourRow[(i+1) % 36] == tourRow[i]-1).OnlyEnforceIf([r1c2,rpm.Not()])
			self.model.Add(tourRow[(i+1) % 36] == tourRow[i]+2).OnlyEnforceIf([r1c2.Not(),rpm])
			self.model.Add(tourRow[(i+1) % 36] == tourRow[i]-2).OnlyEnforceIf([r1c2.Not(),rpm.Not()])
			self.model.Add(tourCol[(i+1) % 36] == tourCol[i]+2).OnlyEnforceIf([r1c2,cpm])
			self.model.Add(tourCol[(i+1) % 36] == tourCol[i]-2).OnlyEnforceIf([r1c2,cpm.Not()])
			self.model.Add(tourCol[(i+1) % 36] == tourCol[i]+1).OnlyEnforceIf([r1c2.Not(),cpm])
			self.model.Add(tourCol[(i+1) % 36] == tourCol[i]-1).OnlyEnforceIf([r1c2.Not(),cpm.Not()])
			
		# Now the ugly part: ensuring entropic
		self._sudoku__setEntropy()
		for k in range(36):
			varBitmap = self._sudoku__varBitmap('',36)
			varTrack = 0
			for i in range(6):
				for j in range(6):
					self.model.Add(tourRow[k] == i).OnlyEnforceIf(varBitmap[varTrack])
					self.model.Add(tourCol[k] == j).OnlyEnforceIf(varBitmap[varTrack])
					self.model.Add(self.cellEntropy[i][j] == (varTrack % 3)).OnlyEnforceIf(varBitmap[varTrack])
					varTrack = varTrack + 1
			
	def printCurrentSolution(self):
		dW = max([len(str(x)) for x in self.digits])
		indexed = [(self.solver.Value(self.indexCells[i][0])-1,self.solver.Value(self.indexCells[i][1])-1) for i in range(self.boardWidth)]
		for rowIndex in range(self.boardWidth):
			for colIndex in range(self.boardWidth):
				if (rowIndex,colIndex) in indexed:
					print(Fore.RED + '{:d}'.format(self.solver.Value(self.cellValues[rowIndex][colIndex])).rjust(dW) + Fore.RESET,end = " ")
				else:
					print('{:d}'.format(self.solver.Value(self.cellValues[rowIndex][colIndex])).rjust(dW),end = " ")
			print()
		print()
		
		#for v in self.allVars:
		#	print('%s=%i' % (v,self.solver.Value(v)))
		
	def preparePrintVariables(self):
		consolidatedCellValues = []
		for tempArray in self.cellValues:
			consolidatedCellValues = consolidatedCellValues + tempArray
		return consolidatedCellValues