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

class japaneseSumSudoku(sudoku):
	"""A class used to implement Japanese Sum puzzles."""
	
	def __init__(self,boardSizeRoot,numberOfColors=1,irregular=None,digitSet=None):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot
		self.nColors = numberOfColors
		self.colorMap = [(Fore.WHITE,Back.BLACK),(Fore.BLACK,Back.WHITE),(Fore.BLACK,Back.RED),(Fore.WHITE,Back.BLUE),(Fore.BLACK,Back.MAGENTA),(Fore.BLACK,Back.YELLOW),(Fore.BLACK,Back.CYAN),(Fore.WHITE,Back.GREEN)]

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
			self.digits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit

		self.model = cp_model.CpModel()
		self.allVars = []
		self.cellValues = []
		
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
			
		# Create rules to ensure rows and columns have no repeats
		for rcIndex in range(self.boardWidth):
			self.model.AddAllDifferent([self.cellValues[rcIndex][crIndex] for crIndex in range(self.boardWidth)]) 	# Rows
			self.model.AddAllDifferent([self.cellValues[crIndex][rcIndex] for crIndex in range(self.boardWidth)]) 	# Columns

		# Now deal with regions. Default to boxes...leaving stub for irregular Sudoku for now
		self.regions = []
		if irregular is None:
			self._sudoku__setBoxes()
			
		# Finally, create arrays to determine which cells are shaded, and what color
		self.cellShaded = []
		self.cellColor = []
		
		for rowIndex in range(self.boardWidth):
			tempArray = []
			tempColorArray = []
			for colIndex in range(self.boardWidth):
				b = self.model.NewBoolVar('cellShaded{:d}{:d}'.format(rowIndex,colIndex))
				tempArray.append(b)
				self.allVars.append(b)
				c = self.model.NewIntVar(0,self.nColors,'cellColor{:d}{:d}'.format(rowIndex,colIndex))
				tempColorArray.append(c)
				self.allVars.append(c)
				# Color 0 is always "unshaded", so we set color variable to 0 in this case.
				self.model.Add(c > 0).OnlyEnforceIf(b)
				self.model.Add(c == 0).OnlyEnforceIf(b.Not())
			self.cellShaded.insert(rowIndex,tempArray)
			self.cellColor.insert(rowIndex,tempColorArray)
			
	def setJapaneseSum(self,row1,col1,rc,value,includeColors=[]):
		# row,col are the coordinates of the cell next to the clue
		# rc is whether things are row/column
		# value is a list of sums of unshaded cells that need to be achieved. Use 0 for ?, cluing that a sum exists but is not given
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else 1
		vStep = 0 if rc == sudoku.Row else 1
			
		# For this row/col, an array of Booleans to determine which cells are the end of a colored region, based on current shading
		EOR = [self.model.NewBoolVar('endOfRegion-Cell{:d}{:d}-Clue{:d}{:d}{:d}'.format(row+i*vStep,col+i*hStep,row,col,rc)) for i in range(self.boardWidth)]
		self.allVars = self.allVars + EOR
		for i in range(self.boardWidth-1):
			# If cell is end of region, next cell MUST be a different color. Otherwise, MUST be the same color
			self.model.Add(self.cellColor[row+(i+1)*vStep][col+(i+1)*hStep] != self.cellColor[row+i*vStep][col+i*hStep]).OnlyEnforceIf(EOR[i])
			self.model.Add(self.cellColor[row+(i+1)*vStep][col+(i+1)*hStep] == self.cellColor[row+i*vStep][col+i*hStep]).OnlyEnforceIf(EOR[i].Not())
		self.model.AddBoolAnd(EOR[self.boardWidth-1]) # Last cell in row/column is definitely end of region
		
		# For this row/col, an array of integers which define the ordinal for the shaded region in the row/col. Unshaded regions will keep the 
		# region number of the previous shaded region for tracking purposes. We'll need to keep this in mind when doing region sums.
		RN = [self.model.NewIntVar(0,self.boardWidth,'regionNumber-Cell{:d}{:d}-Clue{:d}{:d}{:d}'.format(row+i*vStep,col+i*hStep,row,col,rc)) for i in range(self.boardWidth)]
		self.allVars = self.allVars + RN
		
		# If first cell is unshaded, it must be region 0; otherwise it is region 1.
		self.model.Add(RN[0] == 0).OnlyEnforceIf(self.cellShaded[row][col].Not())
		self.model.Add(RN[0] == 1).OnlyEnforceIf(self.cellShaded[row][col])
		
		for i in range(1,self.boardWidth):
			# If previous cell is not end of region, then this cell's region number must match the previous cell's
			self.model.Add(RN[i] == RN[i-1]).OnlyEnforceIf(EOR[i-1].Not())
			
			# If previous cell is end of region, but this cell is *unshaded*, we again keep the same region number
			self.model.Add(RN[i] == RN[i-1]).OnlyEnforceIf([EOR[i-1],self.cellShaded[row+i*vStep][col+i*hStep].Not()])
			
			# If previous cell is end of region, and this cell is shaded, then we increment the region number
			self.model.Add(RN[i] == RN[i-1] + 1).OnlyEnforceIf([EOR[i-1],self.cellShaded[row+i*vStep][col+i*hStep]])
			
		# Finally set up array for this row/col to track region sums. We do this by calculating in each cell the sum of the cells in this region *thus far*. Thus the total shaded region sum can be extracted from the endOfRegion cell
		RSTF = [self.model.NewIntVar(0,sum(self.digits),'regionSumThusFar-Cell{:d}{:d}-Clue{:d}{:d}{:d}'.format(row+i*vStep,col+i*hStep,row,col,rc)) for i in range(self.boardWidth)]
		self.allVars = self.allVars + RSTF
		
		# For the first cell, its sum is just the cell value
		self.model.Add(RSTF[0] == self.cellValues[row][col])
		for i in range(1,self.boardWidth):
			# If the previous cell was end of region, this starts a new sum. Otherwise, we accumulate the previous cell's sum too
			self.model.Add(RSTF[i] == self.cellValues[row+i*vStep][col+i*hStep]).OnlyEnforceIf(EOR[i-1])
			self.model.Add(RSTF[i] == RSTF[i-1] + self.cellValues[row+i*vStep][col+i*hStep]).OnlyEnforceIf(EOR[i-1].Not())
			
		# Alright! We've got all of the tracking variables set up. Now let's assert the clues. First, to maintain backwards compatibility,
		# if a clue is just an integer, we assume it is color 1.
		for j in range(len(value)):
			if isinstance(value[j],int):
				thisSum = value[j]
				thisColor = 1
			else:
				thisSum = value[j][0]
				thisColor = value[j][1]
				
			# Now to determine if this clue is satisfied, we must be able to find a cell in the row/col such that:
			# 1. cellColor == thisColor
			# 2. Cell is end of region (to ensure that its RSTF is the total sum of the shaded region)
			# 3. Region number is j+1 (clue indices are 0-based, region ordinals are 1-based)
			# 4. RSTF of this cell == thisSum
			#
			# To do this, we'll create a varBitmap, one for each cell. varBitmap ensures at least one happens
			
			# OK, we're also going to add ambiguity in here. If thisSum==0, we're not actually enforcing any specific sum, just a color, and vice versa
			
			varBitmap = self._sudoku__varBitmap('JSS',self.boardWidth)
			for i in range(self.boardWidth):
				if thisColor > 0:
					self.model.Add(self.cellColor[row+i*vStep][col+i*hStep] == thisColor).OnlyEnforceIf(varBitmap[i])
				else:
					self.model.AddBoolAnd(self.cellShaded[row+i*vStep][col+i*hStep]).OnlyEnforceIf(varBitmap[i])
				self.model.AddBoolAnd(EOR[i]).OnlyEnforceIf(varBitmap[i])
				self.model.Add(RN[i] == j+1).OnlyEnforceIf(varBitmap[i])
				if thisSum > 0:
					self.model.Add(RSTF[i] == thisSum).OnlyEnforceIf(varBitmap[i])
		
		# If we have a list of colors that must be included, ensure that some region has that color
		for j in range(len(includeColors)):
			colorVars = [self.model.NewBoolVar('JSScolor') for i in range(self.boardWidth)]
			for i in range(self.boardWidth):
				self.model.Add(self.cellColor[row+i*vStep][col+i*hStep] == includeColors[j]).OnlyEnforceIf(colorVars[i])
				self.model.Add(self.cellColor[row+i*vStep][col+i*hStep] != includeColors[j]).OnlyEnforceIf(colorVars[i].Not())
			self.model.AddBoolOr(colorVars)
		
		# Finally, we need to ensure there are no extra regions. The RN sequence is strictly increasing, so RN[self.boardWidth-1] is the number of shaded regions in the clue
		self.model.Add(RN[self.boardWidth-1] == len(value))

	def __assertShadedCell(self,row,col=-1,color=-1):
		if col == -1:
			args = self._sudoku__procCell(row)
			row = args[0]
			col = args[1]
			if len(args) > 2:
				color = args[2]
		
		self.model.AddBoolAnd(self.cellShaded[row][col])
		if color > 0:
			self.model.Add(self.cellColor[row][col] == color)
			
	def assertShaded(self,row,col=-1):
		self.__assertShadedCell(row,col)
		
	def assertShadedArray(self,inlist):
		for x in inlist:
			self.assertShaded(x)
			
	def assertUnshaded(self,row,col=-1):
		if col == -1:
			(row,col) = self._sudoku__procCell(row)
			
		self.model.AddBoolAnd(self.cellShaded[row][col].Not())
		
	def assertUnshadedArray(self,inlist):
		for x in inlist:
			self.assertUnshaded(x)
			
	def assertColor(self,row,col=-1,color=-1):
		self.__assertShadedCell(row,col,color)
		
	def assertFixedColorArray(self,inlist,color):
		inlist = self._sudoku__procCellList(inlist)
		for x in inlist:
			self.assertColor(x[0],x[1],color)
			
	def assertColorArray(self,inlist):
		inlist = self._sudoku__procCellList(inlist)
		for x in inlist:
			self.assertColor(x[0],x[1],x[2])
	
	def printCurrentSolution(self):
		colorama.init()
		dW = max([len(str(x)) for x in self.digits])
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				myColors = self.colorMap[self.solver.Value(self.cellColor[i][j])]
				print(myColors[0] + myColors[1] + '{:d}'.format(self.solver.Value(self.cellValues[i][j])).rjust(dW) + Fore.RESET + Back.RESET,end = " ")
			print()
		print()
		
		#for v in self.allVars:
		#	print('%s=%i' % (v,self.solver.Value(v)))
		
	def preparePrintVariables(self):
		consolidatedCellValues = []
		for tempArray in self.cellValues:
			consolidatedCellValues = consolidatedCellValues + tempArray
		for tempArray in self.cellColor:
			consolidatedCellValues = consolidatedCellValues + tempArray
		return consolidatedCellValues
		
	def setColorMap(self,inlist):
		self.colorMap = inlist
		
	def testStringSolution(self):
		testString = ''
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				testString = testString + '{:d}'.format(self.solver.Value(self.cellValues[i][j]))
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):				
				testString = testString + '{:d}'.format(self.solver.Value(self.cellColors[i][j]))
		return testString
