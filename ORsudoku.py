from __future__ import print_function
import sys
import math
import colorama
from ortools.sat.python import cp_model
from array import *
from colorama import Fore,Back,init
init()

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
	"""Print intermediate solutions."""
	def __init__(self, variables):
		cp_model.CpSolverSolutionCallback.__init__(self)
		self.__variables = variables
		self.__solution_count = 0
		self.__printAll = False
		self.__debug = False
		self.__testMode = False
		self.__testStringArray = []

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
				for v in self.__variables:
					print('%i' % (self.Value(v)), end = ' ')
					cntr += 1
					if cntr == 9:
						print ()
						cntr = 0
				print()
			else:
				for v in self.__variables:
					print('%s=%i' % (v,self.Value(v)))

	def SolutionCount(self):
		return self.__solution_count

class CombinationIterator():
	def __init__(self,n,k):
		self.n = n
		self.k = k
		self.Code = [j for j in range(k)] + [n+1]
				
	def getNext(self):
		if self.Code is None:
			return None
		else:
			current = self.Code[:-1:]
		flag = False
		for i in range(self.k):
			if (self.Code[i] + 1 < self.Code[i+1]):
				flag = True
				self.Code[i] = self.Code[i] + 1
				for j in range(i):
					self.Code[j] = j
				break
		if flag is False: self.Code = None					
		return current
		
class sudoku:
	"""A class used to create a square Sudoku puzzle with variable size,
	   though 3x3 is the default and best (only?) tested use case.
	   
	   Constants
	   =========
		Row/Col - can specify a row/column to indicate whether a clue,
					typically given outside the grid, applies to a row or
					column. Usually only one choice, but needed for (literally)
					the corner cases.
				 
		V/X    - specifies type of XV or XVXV Sudoku clue is used
		
		White/Black - same as XV, but for Kropkis
		
		Horz/Vert - clues that go on edges are usually specified with the
		            grid of the top/left most cell, and then an H or V to
					determine whether the clue is on the right (H) or bottom (V)
					edge
					
		Location Specifications
		=======================
		Cells are specified by coordinates, with (0,0) at top left, (8,8) at bottom right
		First coordinate is the row, so a change causes vertial motion.
		
		Quads are specified analogously, on a (0,0) to (7,7) basis.
		
		Lines are specified as lists of cells. Order within the list usually matters, unless
		it does not matter for the underlying constraint.
		
		There are a whole fistful of methods, so I'm going to have to figure out a better way
		to document
	"""
		
	Row = 0		#Constant to pass to indicate row/column
	Col = 1		#Constant to pass to indicate row/column
	
	V = 0		#Constant to distinguish XV sudoku clues
	X = 1		#Constant to distinguish XV sudoku clues
	
	White = 0	#Constant to distinguish Kropki clues
	Black = 1	#Constant to distinguish Kropki clues
	
	Horz = 0	#Constant to determine clues going horizontally/vertically
	Vert = 1	#Constant to determine clues going horizontally/vertically
	
	Min = 0		#Constant to determine whether min/max clues are mins or maxs
	Max = 1		#Constant to determine whether min/max clues are mins or maxs
	
	Even = 0	# Constant to determine whether parity constraint is even or odd
	Odd = 1		# Constant to determine whether parity constraint is even or odd
	
	Top = 0		# Constant to determine direction arrow on 2x2 points...note code assumes this value is the same as Left
	Bottom = 1	# Constant to determine direction arrow on 2x2 points
	Left = 2	# Constant to determine direction arrow on 2x2 points
	Right = 3	# Constant to determine direction arrow on 2x2 points
	Up = 0		# Constant for Rossini clues
	Down = 1	# Constant for Rossini clues
	
	Corner = 0	# Constant to determine clue type for corner/edge clues
	Edge = 1	# Constant to determine clue type for corner/edge clues
	
	def __init__(self,boardSizeRoot,irregular=None,digitSet=None,model=None):
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
		
		self.isXVInitialized = False
		self.isXVNegative = False
		
		self.isXVXVInitialized = False
		self.isXVXVNegative = False
		
		self.isEntropyQuadInitialized = False
		self.isEntropyQuadNegative = False
		
		self.isEntropyBattenburgInitialized = False
		self.isEntropyBattenburgNegative = False
		
		self.isConsecutiveQuadInitialized = False
		self.isConsecutiveQuadNegative = False
		
		self.isParityQuadInitialized = False
		self.isParityQuadNegative = False
		
		self.isParity = False
		self.isEntropy = False
		self.isModular = False
		self.isFullRank = False
		
		if digitSet is None:
			self.digits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit

		if model is None:
			self.model = cp_model.CpModel()
		else:
			self.model = model
		self.cellValues = []
		self.allVars = []
		self.candTests = [[[None for k in range(len(self.digits))] for j in range(self.boardWidth)] for i in range(self.boardWidth)]
		self.candToExclude=[]
		
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
			self.__setBoxes()
			
	def __setBoxes(self):
		# Create rules to ensure boxes have no repeats
		for rowBox in range(self.boardSizeRoot):
			for colBox in range(self.boardSizeRoot):
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
		
	def setRegions(self,inlist):
		# Allow setting of multiple regions
		for x in inlist: self.setRegion(x)

	def __setParity(self):
		# Set up variables to track parity constraints
		divVars = []
		self.cellParity = []
		
		maxDiff = self.maxDigit-self.minDigit
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				div = self.model.NewIntVar(0,2*maxDiff,'ParityDiv')
				mod = self.model.NewIntVar(0,1,'parityValue{:d}{:d}'.format(i,j))
				t.append(mod)
				self.allVars.append(mod)
				self.model.Add(2*div <= self.cellValues[i][j])
				self.model.Add(2*div+2 > self.cellValues[i][j])
				self.model.Add(mod == self.cellValues[i][j]-2*div)
			self.cellParity.insert(i,t)
		
		self.isParity = True
		
	def __setEntropy(self):
		# Set up variables to track entropy and modular constraints
		self.cellEntropy = []
		
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(self.minDigit // 3 - 1,self.maxDigit // 3,'entropyValue{:d}{:d}'.format(i,j))
				t.append(c)
				self.allVars.append(c)
				self.model.Add(3*c+1 <= self.cellValues[i][j])
				self.model.Add(3*c+4 > self.cellValues[i][j])
			self.cellEntropy.insert(i,t)
		
		self.isEntropy = True

	def __setModular(self):
		# Set up variables to track modular constraints
		if self.isEntropy is False:
			self.__setEntropy()
		
		self.cellModular = []
		
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(1,3,'modularValue{:d}{:d}'.format(i,j))
				t.append(c)
				self.allVars.append(c)
				self.model.Add(c == self.cellValues[i][j] - 3*self.cellEntropy[i][j])
			self.cellModular.insert(i,t)
		
		self.isModular = True
		
	def __setFullRank(self):
		if self.boardWidth != 9 or self.minDigit < 0 or self.maxDigit > 9:
			print("Full rank constraints only supported for digits {0..9} on 9x9 boards or smaller.")
			sys.exit()
			
		# Set up variables to track full rank constraints
		self.rcRank = [self.model.NewIntVar(1,4*self.boardWidth,'fullRankRank') for i in range(4*self.boardWidth)]
		self.rcSum = [self.model.NewIntVar(0,10**self.boardWidth,'fullRankSum') for i in range(4*self.boardWidth)]
		# Set up tie between rank sums and cell values
		for k in range(2):	# Top/left or bottom/right
			for j in range(2):	# Row or column
				for i in range(self.boardWidth):
					# Note: these sums seems backwards because the closest digit to the clue is the MOST significant
					sumRow = i if j == sudoku.Row else (self.boardWidth-1 if k == 0 else 0)
					sumCol = i if j == sudoku.Col else (self.boardWidth-1 if k == 0 else 0)
					hStep = 0 if j == sudoku.Col else (-1 if k == 0 else 1) 
					vStep = 0 if j == sudoku.Row else (-1 if k == 0 else 1)
					#print (sum(self.cellValue[sumRow+m*vStep][sumCol+m*hStep]*10**m for m in range(self.boardWidth)))
					self.model.Add(self.rcSum[4*i+2*j+k] == sum(self.cellValues[sumRow+m*vStep][sumCol+m*hStep]*10**m for m in range(self.boardWidth)))
		
		# Set up Booleans to force rank ordering
		for i in range(4*self.boardWidth):
			for j in range(i+1,4*self.boardWidth):
				c = self.model.NewBoolVar('rankOrder{:d}{:d}'.format(i,j))
				self.model.Add(self.rcSum[i] > self.rcSum[j]).OnlyEnforceIf(c)
				self.model.Add(self.rcRank[i] > self.rcRank[j]).OnlyEnforceIf(c)
				self.model.Add(self.rcSum[i] < self.rcSum[j]).OnlyEnforceIf(c.Not())
				self.model.Add(self.rcRank[i] < self.rcRank[j]).OnlyEnforceIf(c.Not())
				
		self.isFullRank = True

	def getCellVar(self,i,j):
		# Returns the model variable associated with a cell value. Useful when tying several puzzles together, e.g. Samurai
		return self.cellValues[i][j]
				
####Global constraints

	def setXSudokuMain(self):
		self.model.AddAllDifferent([self.cellValues[i][i] for i in range(self.boardWidth)])
		
	def setXSudokuOff(self):
		self.model.AddAllDifferent([self.cellValues[i][self.boardWidth-1-i] for i in range(self.boardWidth)])

	def setBentDiagonals(self):
		ul = [self.cellValues[i][i] for i in range(self.boardWidth//2)]
		ur = [self.cellValues[i][self.boardWidth-1-i] for i in range(self.boardWidth//2)]
		bl = [self.cellValues[self.boardWidth-1-i][i] for i in range(self.boardWidth//2)]
		br = [self.cellValues[self.boardWidth-1-i][self.boardWidth-1-i] for i in range(self.boardWidth//2)]
		c = []
		if self.boardWidth % 2 == 1:
			c.append(self.cellValues[self.boardWidth//2][self.boardWidth//2])
		self.model.AddAllDifferent(ul + bl + c)
		self.model.AddAllDifferent(ul + ur + c)
		self.model.AddAllDifferent(br + bl + c)
		self.model.AddAllDifferent(ur + br + c)
		
	def setAntiKing(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth-1):
				self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+1][j+1]])
			for j in range(1,self.boardWidth):
				self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+1][j-1]])

	def setAntiKnight(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth):
				if j > 1:
					self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+1][j-2]])
				if j > 0 and i < self.boardWidth-2:
					self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+2][j-1]])
				if j < self.boardWidth-1 and i < self.boardWidth-2:
					self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+2][j+1]])
				if j < self.boardWidth-2:
					self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+1][j+2]])
					
	def setDisjointGroups(self):
		for i in range(self.boardSizeRoot):
			for j in range(self.boardSizeRoot):
				self.model.AddAllDifferent([self.cellValues[self.boardSizeRoot*k+i][self.boardSizeRoot*l+j] for k in range(self.boardSizeRoot) for l in range(self.boardSizeRoot)])
				
	def setNonConsecutive(self,n=2):
		if n == 2:
			for i in range(self.boardWidth):
				for j in range(self.boardWidth-1):
					self.model.Add(self.cellValues[i][j] - self.cellValues[i][j+1] != 1)
					self.model.Add(self.cellValues[i][j+1] - self.cellValues[i][j] != 1)
					self.model.Add(self.cellValues[j][i] - self.cellValues[j+1][i] != 1)
					self.model.Add(self.cellValues[j+1][i] - self.cellValues[j][i] != 1)
		else:
			for i in range(self.boardWidth):
				for j in range(self.boardWidth-n):
					self.setNotRenbanLine([(i+1,j+k+1) for k in range(n)])
					self.setNotRenbanLine([(j+k+1,i+1) for k in range(n)])
				
	def setWindoku(self):
		if (self.boardWidth != 9):
			print('Cannot use Windoku on non-9x9 board.')
			sys.exit()
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(1,4) for j in range(1,4)])
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(1,4) for j in range(5,8)])
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(5,8) for j in range(1,4)])
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(5,8) for j in range(5,8)])
		
	def __setIndexCell(self,row,col,rc):
		# This is the atomic call to set an index condition. Dealing with whether it's a whole row, whether or not there's a negative
		# constraint is dealt with higher level functions. This is not generally meant to be set outside the class.
		# row,col is exactly what you think
		# rc determines whether the cell is indexing its row or its column: 0 -> row, 1 -> column
		
		hStep = 0 if rc == sudoku.Col else 1
		vStep = 0 if rc == sudoku.Row else 1		
		target = row+1 if rc == sudoku.Col else col+1
		varBitmap = self.__varBitmap('IndexRow{:d}Col{:d}'.format(row,col),self.boardWidth)
		
		for k in range(self.boardWidth):
			self.model.Add(self.cellValues[row][col] == k+1).OnlyEnforceIf(varBitmap[k])
			self.model.Add(self.cellValues[row*hStep+k*vStep][col*vStep+k*hStep] == target).OnlyEnforceIf(varBitmap[k])
	
	def __setNonIndexCell(self,row,col,rc):
		# This is the atomic call to set a negative constraint on an index condition. Dealing with whether it's a whole row, whether
		# or not there's a negative
		# constraint is dealt with higher level functions. This is not generally meant to be set outside the class.
		# row,col is exactly what you think
		# rc determines whether the cell is indexing its row or its column: 0 -> row, 1 -> column
				
		hStep = 0 if rc == sudoku.Col else 1
		vStep = 0 if rc == sudoku.Row else 1		
		target = row+1 if rc == sudoku.Col else col+1
		varBitmap = self.__varBitmap('IndexRow{:d}Col{:d}'.format(row,col),self.boardWidth-1)
		
		varTrack = 0
		for k in range(self.boardWidth):
			if k+1 == target:
				self.model.Add(self.cellValues[row*hStep+k*vStep][col*vStep+k*hStep] != target)
			else:
				self.model.Add(self.cellValues[row][col] == k+1).OnlyEnforceIf(varBitmap[varTrack])
				self.model.Add(self.cellValues[row*hStep+k*vStep][col*vStep+k*hStep] != target).OnlyEnforceIf(varBitmap[varTrack])
				varTrack = varTrack + 1

	def setIndexRow(self,row1,neg=False,inlist1=[]):
		# This sets up an indexing row. Each cell indexes the *column* so don't be surprised when we call 
		# the cell method with rc=1.
		# Row is the row number
		# neg is whether or not there is a negative constraint on cells not in the index list
		# inlist is the list of cells that index vs. not index in the negative constraint scenario
		
		# Convert 1-base to 0-base
		row0 = row1 - 1
		if len(inlist1) == 0:
			inlist0 = [x for x in range(self.boardWidth)]
		else:
			inlist0 = [x-1 for x in inlist1]
		
		for i in range(self.boardWidth):
			if i in inlist0:
				self.__setIndexCell(row0,i,sudoku.Col)
			elif neg is True:
				self.__setNonIndexCell(row0,i,sudoku.Col)
				
	def setIndexColumn(self,col1,neg=False,inlist1=[]):
		# This sets up an indexing column. Each cell indexes the *row* so don't be surprised when we call 
		# the cell method with rc=0.
		# Row is the column number
		# neg is whether or not there is a negative constraint on cells not in the index list
		# inlist is the list of cells that index vs. not index in the negative constraint scenario
		
		# Convert 1-base to 0-base
		col0 = col1 - 1
		if len(inlist1) == 0:
			inlist0 = [x for x in range(self.boardWidth)]
		else:
			inlist0 = [x-1 for x in inlist1]
		
		for i in range(self.boardWidth):
			if i in inlist0:
				self.__setIndexCell(i,col0,sudoku.Row)
			elif neg is True:	
				self.__setNonIndexCell(i,col0,sudoku.Row)

	def setGlobalWhispers(self,diff=4):
		# Every cell must have at least one neighbor which with its difference is at least diff
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				wwwvars = []
				if i > 0:
					cOn = self.model.NewBoolVar('GlobalWhisperUpNeighborGoodRow{:d}Col{:d}'.format(i,j))
					cOrd = self.model.NewBoolVar('GlobalWhisperUpNeighborOrderRow{:d}Col{:d}'.format(i,j))
					self.model.Add(self.cellValues[i][j] - self.cellValues[i-1][j] >= diff).OnlyEnforceIf([cOn,cOrd])
					self.model.Add(self.cellValues[i-1][j] - self.cellValues[i][j] >= diff).OnlyEnforceIf([cOn,cOrd.Not()])
					self.model.Add(self.cellValues[i][j] - self.cellValues[i-1][j] < diff).OnlyEnforceIf([cOn.Not()])
					self.model.Add(self.cellValues[i-1][j] - self.cellValues[i][j] < diff).OnlyEnforceIf([cOn.Not()])
					self.model.AddBoolAnd([cOrd]).OnlyEnforceIf([cOn.Not()])
					wwwvars.append(cOn)
				if i < self.boardWidth-1:
					cOn = self.model.NewBoolVar('GlobalWhisperDownNeighborGoodRow{:d}Col{:d}'.format(i,j))
					cOrd = self.model.NewBoolVar('GlobalWhisperDownNeighborOrderRow{:d}Col{:d}'.format(i,j))
					self.model.Add(self.cellValues[i][j] - self.cellValues[i+1][j] >= diff).OnlyEnforceIf([cOn,cOrd])
					self.model.Add(self.cellValues[i+1][j] - self.cellValues[i][j] >= diff).OnlyEnforceIf([cOn,cOrd.Not()])
					self.model.Add(self.cellValues[i][j] - self.cellValues[i+1][j] < diff).OnlyEnforceIf([cOn.Not()])
					self.model.Add(self.cellValues[i+1][j] - self.cellValues[i][j] < diff).OnlyEnforceIf([cOn.Not()])
					self.model.AddBoolAnd([cOrd]).OnlyEnforceIf([cOn.Not()])
					wwwvars.append(cOn)
				if j > 0:
					cOn = self.model.NewBoolVar('GlobalWhisperLeftNeighborGoodRow{:d}Col{:d}'.format(i,j))
					cOrd = self.model.NewBoolVar('GlobalWhisperLeftNeighborOrderRow{:d}Col{:d}'.format(i,j))
					self.model.Add(self.cellValues[i][j] - self.cellValues[i][j-1] >= diff).OnlyEnforceIf([cOn,cOrd])
					self.model.Add(self.cellValues[i][j-1] - self.cellValues[i][j] >= diff).OnlyEnforceIf([cOn,cOrd.Not()])
					self.model.Add(self.cellValues[i][j] - self.cellValues[i][j-1] < diff).OnlyEnforceIf([cOn.Not()])
					self.model.Add(self.cellValues[i][j-1] - self.cellValues[i][j] < diff).OnlyEnforceIf([cOn.Not()])
					self.model.AddBoolAnd([cOrd]).OnlyEnforceIf([cOn.Not()])
					wwwvars.append(cOn)
				if j < self.boardWidth-1:
					cOn = self.model.NewBoolVar('GlobalWhisperRightNeighborGoodRow{:d}Col{:d}'.format(i,j))
					cOrd = self.model.NewBoolVar('GlobalWhisperRightNeighborOrderRow{:d}Col{:d}'.format(i,j))
					self.model.Add(self.cellValues[i][j] - self.cellValues[i][j+1] >= diff).OnlyEnforceIf([cOn,cOrd])
					self.model.Add(self.cellValues[i][j+1] - self.cellValues[i][j] >= diff).OnlyEnforceIf([cOn,cOrd.Not()])
					self.model.Add(self.cellValues[i][j] - self.cellValues[i][j+1] < diff).OnlyEnforceIf([cOn.Not()])
					self.model.Add(self.cellValues[i][j+1] - self.cellValues[i][j] < diff).OnlyEnforceIf([cOn.Not()])
					self.model.AddBoolAnd([cOrd]).OnlyEnforceIf([cOn.Not()])
					wwwvars.append(cOn)
				self.model.AddBoolOr(wwwvars)
				
	def setGlobalEntropy(self):
		self.setEntropyQuadArray([(i,j) for i in range(1,self.boardWidth) for j in range(1,self.boardWidth)])

	def setQuadro(self):
		self.setParityQuadArray([(i,j) for i in range(1,self.boardWidth) for j in range(1,self.boardWidth)])

	def setUnicornDigit(self,value):
		# A unicorn digit is one such that for any instance of that digit in the grid, all of the cells a knight's move away are different
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				c = self.model.NewBoolVar('UnicornDigitD{:d}R{:d}C{:d}'.format(value,i,j))
				self.model.Add(self.cellValues[i][j] == value).OnlyEnforceIf(c)

				# Curses...lack of OnlyEnforceIf on AddAllDifferent strikes again. Gotta do it the long way
				kCells = [self.cellValues[i+k][j+m] for k in [-2,-1,1,2] for m in [-2,-1,1,2] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth]
				for k in range(len(kCells)):
					for m in range(k+1,len(kCells)):
						self.model.Add(kCells[k] != kCells[m]).OnlyEnforceIf(c)

				self.model.Add(self.cellValues[i][j] != value).OnlyEnforceIf(c.Not())

	def setAntiQueenDigit(self,values):
		# An anti-queen digit cannot repeat on diagonals
		if type(values) is int:
			values = [values]
		
		for value in values:
			for i in range(self.boardWidth):
				for j in range(self.boardWidth):
					c = self.model.NewBoolVar('AntiQueenDigitD{:d}R{:d}C{:d}'.format(value,i,j))
					self.model.Add(self.cellValues[i][j] == value).OnlyEnforceIf(c)
					dCells = {(i+m*k,j+n*k) for k in range(1,self.boardWidth) for m in [-1,1] for n in [-1,1]} & {(k,m) for k in range(self.boardWidth) for m in range(self.boardWidth)}
					for x in dCells:
						self.model.Add(self.cellValues[x[0]][x[1]] != value).OnlyEnforceIf(c)
					self.model.Add(self.cellValues[i][j] != value).OnlyEnforceIf(c.Not())
					
	def setGSP(self,pairs=[]):
		# Adds a global constraint asserting a symmetry where cells are transformed by pairs under 180 degree rotation
		
		# Set default to pairs adding to maxDigit+minDigit
		if len(pairs) == 0:
			total = self.maxDigit + self.minDigit
			pairs = [[i,total-i] for i in self.digits if i < total - i]
		
		for i in range((self.boardWidth + 1)//2):
			for j in range(self.boardWidth):
				if (i == self.boardWidth//2) and (j >= i): continue	# Does top half of board, and if there is a center row, do left half of it
				else:
					varBitmap = self._sudoku__varBitmap('GSPRow{:d}Col{:d}'.format(i,j),len(pairs))
					otherDigit = self.model.NewBoolVar('GSPOtherRow{:d}Col{:d}'.format(i,j)) # Allows for the case that other non-constrained digits are placed
					pairOrder = self.model.NewBoolVar('GSPPairRow{:d}Col{:d}'.format(i,j))
					for k in range(len(pairs)):
						self.model.Add(self.cellValues[i][j] == pairs[k][0]).OnlyEnforceIf(varBitmap[k] + [pairOrder,otherDigit.Not()])
						self.model.Add(self.cellValues[self.boardWidth-1-i][self.boardWidth-1-j] == pairs[k][1]).OnlyEnforceIf(varBitmap[k] + [pairOrder,otherDigit.Not()])
						self.model.Add(self.cellValues[i][j] == pairs[k][1]).OnlyEnforceIf(varBitmap[k] + [pairOrder.Not(),otherDigit.Not()])
						self.model.Add(self.cellValues[self.boardWidth-1-i][self.boardWidth-1-j] == pairs[k][0]).OnlyEnforceIf(varBitmap[k] + [pairOrder.Not(),otherDigit.Not()])
						self.model.Add(self.cellValues[i][j] != pairs[k][0]).OnlyEnforceIf([otherDigit])
						self.model.Add(self.cellValues[i][j] != pairs[k][1]).OnlyEnforceIf([otherDigit])
						self.model.Add(self.cellValues[self.boardWidth-1-i][self.boardWidth-1-j] != pairs[k][0]).OnlyEnforceIf([otherDigit])
						self.model.Add(self.cellValues[self.boardWidth-1-i][self.boardWidth-1-j] != pairs[k][1]).OnlyEnforceIf([otherDigit])
						
	def setNoThreeInARowParity(self):
		if self.isParity is False:
			self.__setParity()
		for i in range(self.boardWidth-2):
			for j in range(self.boardWidth):
				self.model.Add(sum(self.cellParity[i+k][j] for k in range(3)) > 0)
				self.model.Add(sum(self.cellParity[i+k][j] for k in range(3)) < 3)
				self.model.Add(sum(self.cellParity[j][i+k] for k in range(3)) > 0)
				self.model.Add(sum(self.cellParity[j][i+k] for k in range(3)) < 3)
					
	def setIsotopic(self):
		# Only for 9x9 puzzle. If two boxes have the same center cell, then the other cells in the box must be in the same order around the center cell, with rotations considered the same.
		
		# This is the walk order of cells around the center
		w = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
		for x in range(9):
			i = x // 3
			j = x % 3
			for y in range(x+1,9):
				k = y // 3
				m = y % 3
				if (i == k) or (j == m): continue
				
				c = self.model.NewBoolVar('RotorCenterSquaresEqual')
				self.model.Add(self.cellValues[3*i+1][3*j+1] == self.cellValues[3*k+1][3*m+1]).OnlyEnforceIf(c)
				self.model.Add(self.cellValues[3*i+1][3*j+1] != self.cellValues[3*k+1][3*m+1]).OnlyEnforceIf(c.Not())
				varBitmap = self._sudoku__varBitmap('RotorOffset'.format(i,j),8)
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf(c.Not())		# Pegs variables if there is no match
				for n in range(8):
					for p in range(8):
						self.model.Add(self.cellValues[3*i+1+w[p][0]][3*j+1+w[p][1]] == self.cellValues[3*k+1+w[(p+n)%8][0]][3*m+1+w[(p+n)%8][1]]).OnlyEnforceIf(varBitmap[n]+[c])

####Single cell constraints
	def setGiven(self,row,col=-1,value=-1):
		if col == -1:
			(row,col,value) = self.__procCell(row)
		self.model.Add(self.cellValues[row][col] == value)
	
	def setGivenArray(self,cells):
		for x in cells:	self.setGiven(x)

	def setMinMaxCell(self,row,col=-1,minmax=-1):
		if col == -1:
			(row,col,minmax) = self.__procCell(row)
		if row > 0:
			self.model.Add(self.cellValues[row][col] < self.cellValues[row-1][col]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row-1][col])
		if row < self.boardWidth-1:
			self.model.Add(self.cellValues[row][col] < self.cellValues[row+1][col]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row+1][col])
		if col > 0:
			self.model.Add(self.cellValues[row][col] < self.cellValues[row][col-1]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row][col-1])
		if col < self.boardWidth-1:
			self.model.Add(self.cellValues[row][col] < self.cellValues[row][col+1]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row][col+1])
	setMaxMinCell = setMinMaxCell
			
	def setMinCell(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		self.setMinMaxCell(row,col,self.Min)

	def setMaxCell(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		self.setMinMaxCell(row,col,self.Max)
		
	def setMinMaxArray(self,cells):
		for x in cells: self.setMinMaxCell(x)
	setMaxMinArray = setMinMaxArray
		
	def setMinArray(self,cells):
		for x in cells: self.setMinCell(x)
		
	def setMaxArray(self,cells):
		for x in cells: self.setMaxCell(x)
		
	def setEvenOdd(self,row,col=-1,parity=-1):
		if col == -1:
			(row,col,parity) = self.__procCell(row)
		self.model.AddModuloEquality(parity,self.cellValues[row][col],2)
	setOddEven = setEvenOdd	
		
	def setEven(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		self.setEvenOdd(row,col,self.Even)
		
	def setOdd(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		self.setEvenOdd(row,col,self.Odd)
		
	def setEvenArray(self,cells):
		for x in cells: self.setEven(x)
		
	def setOddArray(self,cells):
		for x in cells: self.setOdd(x)
		
	def setEvenOddArray(self,cells):
		for x in cells: self.setEvenOdd(x)
	setOddEvenArray = setEvenOddArray
		
	def setNeighborSum(self,row,col=-1):
		# Cell whose value is the sum of its orthogonally adjacent neighbors
		if col == -1:
			(row,col) = self.__procCell(row)
		sCells = [self.cellValues[row+k][col+m] for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m) and row+k >= 0 and row+k < self.boardWidth and col+m >= 0 and col+m < self.boardWidth]
		self.model.Add(sum(sCells) == self.cellValues[row][col])
	
	def	setNeighbourSum(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		self.setNeighborSum(row,col)
		
	def setNeighborSumArray(self,cells):
		for x in cells: self.setNeighborSum(x)
		
	def	setNeighbourSumArray(self,cells):
		self.setNeighborSum(cells)
	
	def setFriendly(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
			
		if self.isFriendlyInitialized is not True:
			self.friendlyCells = [(row,col)]
			self.isFriendlyInitialized = True
		else:
			self.friendlyCells.append((row,col))
			
		rowMatch = self.model.NewBoolVar('FriendlyRowRow{:d}Col{:d}'.format(row,col))
		colMatch = self.model.NewBoolVar('FriendlyColRow{:d}Col{:d}'.format(row,col))
		boxMatch = self.model.NewBoolVar('FriendlyBoxRow{:d}Col{:d}'.format(row,col))
		
		self.model.Add(self.cellValues[row][col] == row+1).OnlyEnforceIf(rowMatch)
		self.model.Add(self.cellValues[row][col] != row+1).OnlyEnforceIf(rowMatch.Not())
		self.model.Add(self.cellValues[row][col] == col+1).OnlyEnforceIf(colMatch)
		self.model.Add(self.cellValues[row][col] != col+1).OnlyEnforceIf(colMatch.Not())
		
		rowInd = row // self.boardSizeRoot	# Determines box row: 0,1,2 -> 0; 3,4,5 -> 1, 6,7,8 -> 2
		colInd = col // self.boardSizeRoot	# Determines box col: 0,1,2 -> 0; 3,4,5 -> 1, 6,7,8 -> 2
		box = 3*rowInd + colInd				# Determines 0-base box index
		
		self.model.Add(self.cellValues[row][col] == box+1).OnlyEnforceIf(boxMatch)
		self.model.Add(self.cellValues[row][col] != box+1).OnlyEnforceIf(boxMatch.Not())
		
		self.model.AddBoolOr([rowMatch,colMatch,boxMatch])
		
	def setFriendlyArray(self,cells):
		for x in cells: self.setFriendly(x)
		
	def setUnfriendly(self,row,col=-1):
		# To label a single cell as specifically not friendly
		if col == -1:
			(row,col) = self.__procCell(row)
		self.model.Add(self.cellValues[row][col] != row+1)
		self.model.Add(self.cellValues[row][col] != col+1)
		rowInd = row // self.boardSizeRoot
		colInd = col // self.boardSizeRoot
		box = 3*rowInd + colInd
		self.model.Add(self.cellValues[row][col] != box+1)			
		
	def setUnfriendlyArray(self,cells):
		for x in cells: self.setUnfriendly(x)

	def setFriendlyNegative(self):
		if self.isFriendlyInitialized is not True:
			self.friendlyCells = []
			self.isFriendlyInitialized = True
		self.isFriendlyNegative = True
		
	def __applyFriendlyNegative(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if (i,j) not in self.friendlyCells:
					self.setUnfriendly(i,j)
					
	def setScary(self,row,col=-1,diff=3):
		if col == -1:
			(row,col) = self.__procCell(row)
		nCells = {(row+i,col+j) for i in [-1,0,1] for j in [-1,0,1] if (i,j) != (0,0)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)}
		for x in nCells:
			c = self.model.NewBoolVar('ScaryCell')
			self.model.Add(self.cellValues[row][col] - self.cellValues[x[0]][x[1]] >= diff).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[x[0]][x[1]] - self.cellValues[row][col] >= diff).OnlyEnforceIf(c.Not())

	def setPencilmarks(self,row1,col1=-1,values=-1):
		# A list of allowed values in the cell
		if col1 == -1:
			T = self.__procCell(row1)
			row = T[0]
			col = T[1]
			values = [T[i] for i in range(2,len(T))]
		else:
			row = row1 - 1
			col = col1 - 1
			
		self.model.AddAllowedAssignments([self.cellValues[row][col]],[(x,) for x in values])
		
	def setPencilmarksArray(self,list):
		for x in list: self.setPencilmarks(x)

	def setSearchNine(self,row1,col1,uldr,digit=9):
		# A search nine clue indicates the distance and direction of a 9 from the clued cell. The distance is the cell value, the arrow clue points
		row = row1 - 1
		col = col1 - 1		
		if uldr == self.Up:
			maxD = row
			minD = self.boardWidth-1-row
			hStep = 0
			vStep = -1
		elif uldr == self.Down:
			maxD = self.boardWidth-1-row
			minD = row
			hStep = 0
			vStep = 1
		elif uldr == self.Left:
			maxD = col
			minD = self.boardWidth-1-col
			hStep = -1
			vStep = 0
		else:
			maxD = self.boardWidth-1-col
			minD = col
			hStep = 1
			vStep = 0
		allowableDigits = [x for x in self.digits if 0 <= x <= maxD or 0 <= -1*x <= minD]
		varBitmap = self.__varBitmap('SearchNineRow{:d}Col{:d}'.format(row,col),len(allowableDigits))
		varTrack = 0
		for x in allowableDigits:
			self.model.Add(self.cellValues[row][col] == x).OnlyEnforceIf(varBitmap[varTrack])
			self.model.Add(self.cellValues[row+x*vStep][col+x*hStep] == digit).OnlyEnforceIf(varBitmap[varTrack])
			varTrack = varTrack + 1

	def setAllOddOrEven(self,inlist):
		if self.isParity is False:
			self.__setParity()
		inlist = set(self.__procCellList(inlist))
		
		for i in range(len(self.regions)):
			rList = list(inlist & set(self.regions[i]))
			if len(rList) > 1:
				for j in range(1,len(rList)):
					self.model.Add(self.cellParity[rList[0][0]][rList[0][1]] == self.cellParity[rList[j][0]][rList[j][1]])
			
####Multi-cell constraints
	def setFortress(self,inlist):
		inlist = self.__procCellList(inlist)
		for x in inlist:
			if x[0] > 0 and (x[0]-1,x[1]) not in inlist:
				self.model.Add(self.cellValues[x[0]][x[1]] > self.cellValues[x[0]-1][x[1]])
			if x[0] < self.boardWidth-1 and (x[0]+1,x[1]) not in inlist:
				self.model.Add(self.cellValues[x[0]][x[1]] > self.cellValues[x[0]+1][x[1]])
			if x[1] > 0 and (x[0],x[1]-1) not in inlist:
				self.model.Add(self.cellValues[x[0]][x[1]] > self.cellValues[x[0]][x[1]-1])
			if x[1] < self.boardWidth-1 and (x[0],x[1]+1) not in inlist:
				self.model.Add(self.cellValues[x[0]][x[1]] > self.cellValues[x[0]][x[1]+1])
				
	def setKropkiWhite(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		if self.isKropkiInitialized is not True:
			self.kropkiCells = [(row,col,hv)]
			self.isKropkiInitialized = True
		else:
			self.kropkiCells.append((row,col,hv))
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bit = self.model.NewBoolVar('KropkiWhiteBiggerDigitRow{:d}Col{:d}HV{:d}'.format(row,col,hv))
		self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == self.kropkiDiff).OnlyEnforceIf(bit)
		self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == -1*self.kropkiDiff).OnlyEnforceIf(bit.Not())
		
	def setKropkiBlack(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		if self.isKropkiInitialized is not True:
			self.kropkiCells = [(row,col,hv)]
			self.isKropkiInitialized = True
		else:
			self.kropkiCells.append((row,col,hv))
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bit = self.model.NewBoolVar('KropkiBlackBiggerDigitRow{:d}Col{:d}HV{:d}'.format(row,col,hv))
		self.model.Add(self.cellValues[row][col] == self.kropkiRatio*self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf(bit)
		self.model.Add(self.kropkiRatio*self.cellValues[row][col] == self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf(bit.Not())
		
	def setKropkiWhiteArray(self,cells):
		for x in cells: self.setKropkiWhite(x)
		
	def setKropkiBlackArray(self,cells):
		for x in cells: self.setKropkiBlack(x)
		
	def setKropkiArray(self,cells):
		cellList = self.__procCellList(cells)
		for x in cellList:
			if x[3] == sudoku.White:
				self.setKropkiWhite(x[0],x[1],x[2])
			else:
				self.setKropkiBlack(x[0],x[1],x[2])

	def setKropkiNegative(self):
		if self.isKropkiInitialized is not True:
			self.kropkiCells = []
			self.isKropkiInitialized = True
		self.isKropkiNegative = True
		
	def setAntiKropki(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] != self.kropkiDiff)
		self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] != -1*self.kropkiDiff)
		self.model.Add(self.cellValues[row][col] != self.kropkiRatio*self.cellValues[row+hv][col+(1-hv)])
		self.model.Add(self.kropkiRatio*self.cellValues[row][col] != self.cellValues[row+hv][col+(1-hv)])
		
	def setAntiKropkiArray(self,cells):
		for x in cells: self.setAntiKropki(x)
	
	def __applyKropkiNegative(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if i < 8 and (i,j,1) not in self.kropkiCells:
					self.setAntiKropki(i,j,1)
				if j < 8 and (i,j,0) not in self.kropkiCells:
					self.setAntiKropki(i,j,0)
	
	def setKropkiDifference(self,diff=1):
		# Sets the difference used in all subseqequent white Kropki dots
		self.kropkiDiff = diff
		
	def setKropkiRatio(self,ratio=2):
		# Sets the ratio used in all subseqequent black Kropki dots
		self.kropkiRatio = ratio
					
	def setXVV(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		if self.isXVInitialized is not True:
			self.xvCells = [(row,col,hv)]
			self.isXVInitialized = True
		else:
			self.xvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] == 5)
		
	def setXVX(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		if self.isXVInitialized is not True:
			self.xvCells = [(row,col,hv)]
			self.isXVInitialized = True
		else:
			self.xvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] == 10)
		
	def setXVVArray(self,cells):
		for x in cells: self.setXVV(x)
		
	def setXVXArray(self,cells):
		for x in cells: self.setXVX(x)
		
	def setXVArray(self,cells):
		cellList = self.__procCellList(cells)
		for x in cellList:
			if x[3] == sudoku.V:
				self.setXVV(x[0],x[1],x[2])
			else:
				self.setXVX(x[0],x[1],x[2])
				
	def setAntiXV(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] != 5)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] != 10)
		
	def setAntiXVArray(self,cells):
		for x in cells: self.setAntiXV(x)

	def setXVNegative(self):
		if self.isXVInitialized is not True:
			self.xvCells = []
			self.isXVInitialized = True
		self.isXVNegative = True
		
	def __applyXVNegative(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if i < 8 and (i,j,1) not in self.xvCells:
					self.setAntiXV(i,j,1)
				if j < 8 and (i,j,0) not in self.xvCells:
					self.setAntiXV(i,j,0)
					
	def setXVXVV(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		if self.isXVXVInitialized is not True:
			self.xvxvCells = [(row,col,hv)]
			self.isXVXVInitialized = True
		else:
			self.xvxvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bit = self.model.NewBoolVar('XVXV515Row{:d}Col{:d}'.format(row,col))
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] == 5).OnlyEnforceIf(bit)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] == 15).OnlyEnforceIf(bit.Not())
		
	def setXVXVX(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		if self.isXVXVInitialized is not True:
			self.xvxvCells = [(row,col,hv)]
			self.isXVXVInitialized = True
		else:
			self.xvxvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bit = self.model.NewBoolVar('XVXV1015Row{:d}Col{:d}'.format(row,col))
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] == 10).OnlyEnforceIf(bit)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] == 15).OnlyEnforceIf(bit.Not())
		
	def setXVXVVArray(self,cells):
		for x in cells: self.setXVXVV(x)
		
	def setXVXVXArray(self,cells):
		for x in cells: self.setXVXVX(x)
		
	def setXVXVArray(self,cells):
		cellList = self.__procCellList(cells)
		for x in cellList:
			if x[3] == sudoku.V:
				self.setXVXVV(x[0],x[1],x[2])
			else:
				self.setXVXVX(x[0],x[1],x[2])

	def setAntiXVXV(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] != 5)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] != 10)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] != 15)
		
	def setAntiXVXVArray(self,cells):
		for x in cells: self.setAntiXVXV(x)

	def setXVXVNegative(self):
		if self.isXVXVInitialized is not True:
			self.xvxvCells = []
			self.isXVXVInitialized = True
		self.isXVXVNegative = True
		
	def __applyXVXVNegative(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if i < 8 and (i,j,1) not in self.xvxvCells:
					self.setAntiXVXV(i,j,1)
				if j < 8 and (i,j,0) not in self.xvxvCells:
					self.setAntiXVXV(i,j,0)

	def setEitherOr(self,row,col=-1,hv=-1,value=-1):
		if col == -1:
			(row,col,hv,value) = self.__procCell(row)
		c = self.model.NewBoolVar('EitherOr')
		self.model.Add(self.cellValues[row][col] == value).OnlyEnforceIf(c)
		self.model.Add(self.cellValues[row+hv][col+(1-hv)] == value).OnlyEnforceIf(c.Not())
		
	def setEitherOrArray(self,cells):
		for x in cells: self.setEitherOr(x)
	
	def setCloneRegion(self,inlist):
		inlist = list(map(self.__procCellList,inlist))
		for j in range(1,len(inlist)):
			for k in range(len(inlist[0])):
				self.model.Add(self.cellValues[inlist[0][k][0]][inlist[0][k][1]] == self.cellValues[inlist[j][k][0]][inlist[j][k][1]])
				
	def setDominantCloneRegion(self,inlist,strict=True):
		# Cloned regions where digits in one clone are greater than (by position) all other clones
		inlist = list(map(self.__procCellList,inlist))
		for j in range(1,len(inlist)):
			for k in range(len(inlist[0])):
				if strict is True:
					self.model.Add(self.cellValues[inlist[0][k][0]][inlist[0][k][1]] > self.cellValues[inlist[j][k][0]][inlist[j][k][1]])
				else:
					self.model.Add(self.cellValues[inlist[0][k][0]][inlist[0][k][1]] >= self.cellValues[inlist[j][k][0]][inlist[j][k][1]])
				
	def setCage(self,inlist,value = None):
		inlist = self.__procCellList(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in inlist])
		if value is not None:
			self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in inlist) == value)
			
	def setRepeatingCage(self,inlist,value):
		inlist = self.__procCellList(inlist)
		self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in inlist) == value)
		
	def setMedianCage(self,inlist,value):
		inlist = self.__procCellList(inlist)
		equalVars = [self.model.NewBoolVar('MedianEqual{:d}'.format(i)) for i in range(len(inlist))]
		gtltVars = [self.model.NewBoolVar('MedianGreaterThan{:d}'.format(i)) for i in range(len(inlist))]
		ternVars = [self.model.NewIntVar(-1,1,'MedianTern{:d}'.format(i)) for i in range(len(inlist))]
		for i in range(len(inlist)):
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == value).OnlyEnforceIf([equalVars[i]])
			self.model.AddBoolAnd([gtltVars[i]]).OnlyEnforceIf(equalVars[i])	#Pegs unneeded gtlt to True if equal
			self.model.Add(ternVars[i] == 0).OnlyEnforceIf(equalVars[i])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] > value).OnlyEnforceIf([equalVars[i].Not(),gtltVars[i]])
			self.model.Add(ternVars[i] == 1).OnlyEnforceIf([equalVars[i].Not(),gtltVars[i]])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < value).OnlyEnforceIf([equalVars[i].Not(),gtltVars[i].Not()])
			self.model.Add(ternVars[i] == -1).OnlyEnforceIf([equalVars[i].Not(),gtltVars[i].Not()])
			
		self.model.AddBoolOr(equalVars)	# At least some cell equals the median
		self.model.Add(sum(ternVars) == 0)	# Ensures there are an equal number of values less than vs. greater than the median
		
	def setBlockCage(self,inlist,values):
		# A block cage is an area with a list of values that cannot appear in that area
		inlist = self.__procCellList(inlist)
		if isinstance(values,list):
			myValues = values
		else:
			myValues = [int(x) for x in str(values)]
		
		for i in range(len(inlist)):
			for j in range(len(myValues)):
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] != myValues[j])
				
	def setMOTECage(self,inlist):
		# A MOTE cage has more odd than even cells
		inlist = self.__procCellList(inlist)
		if self.isParity is False:
			self.__setParity()
		self.model.Add(sum([self.cellParity[inlist[i][0]][inlist[i][1]] for i in range(len(inlist))]) >= (len(inlist)+2)//2)
		
	def setMETOCage(self,inlist):
		# A METO cage has more even than odd cells
		inlist = self.__procCellList(inlist)
		if self.isParity is False:
			self.__setParity()
		self.model.Add(sum([self.cellParity[inlist[i][0]][inlist[i][1]] for i in range(len(inlist))]) <= (len(inlist)-1)//2)
		
	def setCapsule(self,inlist):
		# A capsule has the same number of even and odd digits
		inlist = self.__procCellList(inlist)
		if self.isParity is False:
			self.__setParity()
		if len(inlist) % 2 == 1:
			print("Odd length capsule cannot be satisfied")
			sys.exit()
		else:
			self.model.Add(sum([self.cellParity[inlist[i][0]][inlist[i][1]] for i in range(len(inlist))]) == len(inlist)//2)
			
	def setDavidAndGoliath(self,inlist,borderDigit=5,borderType=0):
		# The pair contains at least one David digit and at least one Goliath digit, where any overlapping digit itself meets both conditions
		inlist = self.__procCellList(inlist)
		d = [self.model.NewBoolVar('david') for i in range(2)]
		g = [self.model.NewBoolVar('goliath') for i in range(2)]
		for i in range(2):
			if borderType <= 0: # borderDigit is a David digit
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] <= borderDigit).OnlyEnforceIf(d[i])
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] > borderDigit).OnlyEnforceIf(d[i].Not())
			else:
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < borderDigit).OnlyEnforceIf(d[i])
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] >= borderDigit).OnlyEnforceIf(d[i].Not())
			if borderType >= 0: # borderDigit is a Goliath digit
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] >= borderDigit).OnlyEnforceIf(g[i])
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < borderDigit).OnlyEnforceIf(g[i].Not())
			else:
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] > borderDigit).OnlyEnforceIf(d[i])
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] <= borderDigit).OnlyEnforceIf(g[i].Not())
		self.model.AddBoolOr(d)
		self.model.AddBoolOr(g)

	def setDigitCountCage(self,inlist,value):
		# A digit count cage specifies the number of distinct digits that appear in the cage...h/t clover!
		inlist = self.__procCellList(inlist)
		digits = list(self.digits)
		digitCellBools = [[self.model.NewBoolVar('DigitCellPairs') for i in range(len(digits))] for j in range(len(inlist))]
		digitCellInts = [[self.model.NewIntVar(0,1,'DigitCellPairs') for i in range(len(digits))] for j in range(len(inlist))]
		digitBools = [self.model.NewBoolVar('DigitCounts') for i in range(len(digits))]
		digitInts = [self.model.NewIntVar(0,1,'DigitCounts') for i in range(len(digits))]
		for j in range(len(inlist)):
			for i in range(len(digits)):
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] == digits[i]).OnlyEnforceIf(digitCellBools[j][i])
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] != digits[i]).OnlyEnforceIf(digitCellBools[j][i].Not())
				self.model.Add(digitCellInts[j][i] == 1).OnlyEnforceIf(digitCellBools[j][i])
				self.model.Add(digitCellInts[j][i] == 0).OnlyEnforceIf(digitCellBools[j][i].Not())
				
		for i in range(len(digits)):
			self.model.Add(sum([digitCellInts[j][i] for j in range(len(inlist))]) > 0).OnlyEnforceIf(digitBools[i])
			self.model.Add(sum([digitCellInts[j][i] for j in range(len(inlist))]) == 0).OnlyEnforceIf(digitBools[i].Not())
			self.model.Add(digitInts[i] == 1).OnlyEnforceIf(digitBools[i])
			self.model.Add(digitInts[i] == 0).OnlyEnforceIf(digitBools[i].Not())
		
		self.model.Add(sum([digitInts[i] for i in range(len(digits))]) == value)

	def setVault(self,inlist):
		# Digits in a vault cannot appear in any cell outside the vault but orthogonally adjacent ot a cell in it.
		inlist = self.__procCellList(inlist)
		adjCells = set()
		for i in range(len(inlist)):
			adjCells = adjCells.union({(inlist[i][0],inlist[i][1]-1),(inlist[i][0],inlist[i][1]+1),(inlist[i][0]+1,inlist[i][1]),(inlist[i][0]-1,inlist[i][1])})
		adjCells = adjCells & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth) if (i,j) not in inlist}

		for x in inlist:
			for y in adjCells:
				self.model.Add(self.cellValues[x[0]][x[1]] != self.cellValues[y[0]][y[1]])

	def setZone(self,inlist,values):
		# A zone is an area with potentially repeating values; the clue is a list of digits that must appear in the zone
		inlist = self.__procCellList(inlist)
		for x in set(values):
			xVars = []
			for i in range(len(inlist)):
				c = self.model.NewBoolVar('ZoneR{:d}C{:d}V{:d}'.format(inlist[i][0],inlist[i][1],x))
				# Tie Boolean to integer so we can count instances
				cI = self.model.NewIntVar(0,1,'ZoneIntR{:d}C{:d}V{:d}'.format(inlist[i][0],inlist[i][1],x))
				self.model.Add(cI == 1).OnlyEnforceIf(c)
				self.model.Add(cI == 0).OnlyEnforceIf(c.Not())
				xVars.append(cI)
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == x).OnlyEnforceIf(c)
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] != x).OnlyEnforceIf(c.Not())
				
			self.model.Add(sum(xVars) == values.count(x))
			
	def setOrderSumCages(self,inlist,slow=False,repeat=False):
		# A list of cages whose sum increases based on the order in the list
		inlist = list(map(self.__procCellList,inlist))
		for j in range(len(inlist)):
			if repeat is False:
				self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in inlist[j]])
			if j < len(inlist)-1:
				if slow is True:
					self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in inlist[j]) <= sum(self.cellValues[x[0]][x[1]] for x in inlist[j]))
				else:
					self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in inlist[j]) < sum(self.cellValues[x[0]][x[1]] for x in inlist[j]))

	def setMagicSquare(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		tSum = (self.boardWidth+1)*self.boardSizeRoot // 2
		for i in range(self.boardSizeRoot):
			self.model.Add(sum(self.cellValues[row+i][col+j] for j in range(self.boardSizeRoot)) == tSum) # Row sum
			self.model.Add(sum(self.cellValues[row+j][col+i] for j in range(self.boardSizeRoot)) == tSum) # Column sum
		
		self.model.Add(sum(self.cellValues[row+j][col+j] for j in range(self.boardSizeRoot)) == tSum) # Main diagonal sum
		self.model.Add(sum(self.cellValues[row+j][col+self.boardSizeRoot-1-j] for j in range(self.boardSizeRoot)) == tSum) # Off diagonal sum
		
	def setEntropkiWhite(self,row,col=-1,hv=-1):
		if self.isEntropy is False:
			self.__setEntropy()
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellEntropy[row][col] != self.cellEntropy[row+hv][col+(1-hv)])
		
	def setEntropkiBlack(self,row,col=-1,hv=-1):
		if self.isEntropy is False:
			self.__setEntropy()
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellEntropy[row][col] == self.cellEntropy[row+hv][col+(1-hv)])

	def setEntropkiWhiteArray(self,cells):
		for x in cells: self.setEntropkiWhite(x)
		
	def setEntropkiBlackArray(self,cells):
		for x in cells: self.setEntropkiBlack(x)
		
	def setEntropkiArray(self,cells):
		cellList = self.__procCellList(cells)
		for x in cellList:
			if x[3] == sudoku.White:
				self.setEntropkiWhite(x[0],x[1],x[2])
			else:
				self.setEntropkiBlack(x[0],x[1],x[2])
				
	def setParityDotWhite(self,row,col=-1,hv=-1):
		if self.isParity is False:
			self.__setParity()
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellParity[row][col] != self.cellParity[row+hv][col+(1-hv)])
		
	def setParityDotBlack(self,row,col=-1,hv=-1):
		if self.isParity is False:
			self.__setParity()
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellParity[row][col] == self.cellParity[row+hv][col+(1-hv)])

	def setParityDotWhiteArray(self,cells):
		for x in cells: self.setParityDotWhite(x)
		
	def setParityDotBlackArray(self,cells):
		for x in cells: self.setParityDotBlack(x)
		
	def setParityDotArray(self,cells):
		cellList = self.__procCellList(cells)
		for x in cellList:
			if x[3] == sudoku.White:
				self.setParityDotWhite(x[0],x[1],x[2])
			else:
				self.setParityDotBlack(x[0],x[1],x[2])

	def setGenetic(self,inlist):
		inlist = self.__procCellList(inlist)
		if self.isEntropy is False:
			self.__setEntropy()
		if self.isParity is False:
			self.__setParity()
			
		p1Parity = self.model.NewBoolVar('GeneticsP1ParityMatchRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1]))
		p1Entropy = self.model.NewBoolVar('GeneticsP1EntropyMatchRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1]))
		p2Parity = self.model.NewBoolVar('GeneticsP2ParityMatchRow{:d}Col{:d}'.format(inlist[1][0],inlist[1][1]))
		p2Entropy = self.model.NewBoolVar('GeneticsP2EntropyMatchRow{:d}Col{:d}'.format(inlist[1][0],inlist[1][1]))
		
		self.model.Add(self.cellParity[inlist[0][0]][inlist[0][1]] == self.cellParity[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p1Parity)
		self.model.Add(self.cellParity[inlist[0][0]][inlist[0][1]] != self.cellParity[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p1Parity.Not())
		self.model.Add(self.cellParity[inlist[1][0]][inlist[1][1]] == self.cellParity[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p2Parity)
		self.model.Add(self.cellParity[inlist[1][0]][inlist[1][1]] != self.cellParity[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p2Parity.Not())
		self.model.Add(self.cellEntropy[inlist[0][0]][inlist[0][1]] == self.cellEntropy[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p1Entropy)
		self.model.Add(self.cellEntropy[inlist[0][0]][inlist[0][1]] != self.cellEntropy[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p1Entropy.Not())
		self.model.Add(self.cellEntropy[inlist[1][0]][inlist[1][1]] == self.cellEntropy[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p2Entropy)
		self.model.Add(self.cellEntropy[inlist[1][0]][inlist[1][1]] != self.cellEntropy[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p2Entropy.Not())
		
		self.model.AddBoolOr([p1Parity,p2Parity])	#Inherit parity from a parent
		self.model.AddBoolOr([p1Entropy,p2Entropy])	#Inherit entropy from a parent
		self.model.AddBoolOr([p1Parity,p1Entropy])	#Inherit something from parent 1
		self.model.AddBoolOr([p2Parity,p2Entropy])	#Inherit something from parent 2
		
	def setGeneticArray(self,cells):
		for x in cells: self.setGenetic(x)
		
	def setParitySnake(self,row1,col1,row2,col2,parity=None):
		if self.isParity is False:
			self.__setParity()
		r1 = row1 - 1
		c1 = col1 - 1
		r2 = row2 - 1
		c2 = col2 - 1
		if parity is None:
			parity = self.cellParity[r1][c1]
			
		self.model.Add(self.cellParity[r1][c1] == parity)
		self.model.Add(self.cellParity[r2][c2] == parity)
		
		pathBool = []
		pathInt = []
		for i in range(self.boardWidth):
			tB = []
			tI = []
			for j in range(self.boardWidth):
				cB = self.model.NewBoolVar('snake{:d}{:d}'.format(i,j))
				cI = self.model.NewIntVar(0,1,'snake{:d}{:d}'.format(i,j))
				self.model.Add(cI == 1).OnlyEnforceIf(cB)
				self.model.Add(cI == 0).OnlyEnforceIf(cB.Not())
				tB.append(cB)
				tI.append(cI)
			pathBool.insert(i,tB)
			pathInt.insert(i,tI)
			
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if (i,j) == (r1,c1) or (i,j) == (r2,c2):
					self.model.Add(sum(pathInt[x[0]][x[1]] for x in self.getOrthogonalNeighbors(i,j)) == 1)
					self.model.AddBoolAnd(pathBool[i][j])
				else:
					self.model.Add(sum(pathInt[x[0]][x[1]] for x in self.getOrthogonalNeighbors(i,j)) == 2).OnlyEnforceIf(pathBool[i][j])
					self.model.Add(self.cellParity[i][j] == parity).OnlyEnforceIf(pathBool[i][j])
					
	def setAntiQueenCell(self,row,col=-1,r2=-1,c2=-1):
		# The digit in an anti-queen cell cannot repeat on any diagonal. If a second cell is given, only repeats in the direction of the given cell are forbidden
		if col == -1:
			T = self.__procCell(row)
			row = T[0]
			col = T[1]
			values = [T[i] for i in range(2,len(T))]
			if len(values) == 2:
				r2 = values[0] - 1
				c2 = values[1] - 1
			else:
				r2 = -1
		
		if r2 == -1:
			# No repeats on any diagonals
			dCells = {(row+m*k,col+n*k) for k in range(1,self.boardWidth) for m in [-1,1] for n in [-1,1]} & {(k,m) for k in range(self.boardWidth) for m in range(self.boardWidth)}
		else:
			m = r2 - row
			n = c2 - col
			dCells = {(row+m*k,col+n*k) for k in range(1,self.boardWidth)} & {(k,j) for k in range(self.boardWidth) for j in range(self.boardWidth)}

		for x in dCells:
			self.model.Add(self.cellValues[x[0]][x[1]] != self.cellValues[row][col])
			
####Externally-clued constraints
	def setLittleKiller(self,row1,col1,row2,col2,value):
		# row1,col1 is the position of the first cell in the sum
		# row2,col2 is the position of the second cell in the sum
		
		# Note: leave cell specs 1-based, since the call to setRepeatingCage will 0-base them
		hStep = col2 - col1
		vStep = row2 - row1
		cells = [(row1+vStep*k,col1+hStep*k) for k in range(self.boardWidth) if row1+vStep*k-1 in range(self.boardWidth) and col1+hStep*k-1 in range(self.boardWidth)]
		self.setRepeatingCage(cells,value)
		
	def setXSumBase(self,row1,col1,rc,value,pm):
		#row,col are the coordinates of the cell containing the length, value is the sum
		#rc: 0 -> if adding in row, 1 -> if adding in column. Needed for corner cells.
		#pm: determines if these are normal X-sums (including the digit) or reverse X-Sums (sum on the other side)
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		sumRow = row if rc == sudoku.Row or pm == 1 else self.boardWidth-1-row
		sumCol = col if rc == sudoku.Col or pm == 1 else self.boardWidth-1-col
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		hStep = pm * hStep	# Change direction in case we're doing reverse
		vStep = pm * vStep
		
		digits = list(self.digits)
		varBitmap = self.__varBitmap('XSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(digits))
			
		for i in range(len(digits)):
			if digits[i] == 0:
				# In this case we have to have a null sum, which must be 0.
				if value == 0:
					self.model.Add(self.cellValues[sumRow][sumCol] == 0).OnlyEnforceIf(varBitmap[i])
				else:
					self.model.AddBoolAnd([varBitmap[i][0].Not()]).OnlyEnforceIf(varBitmap[i])		
					# If value is not 0, then 0 is not a valid digit and this case cannot occur, but there's no arithmetic way to express this	
			elif abs(digits[i]) > self.boardWidth:
				# Digit is too big to have a reasonable sum, so disallow
				self.model.AddBoolAnd([varBitmap[i][0].Not()]).OnlyEnforceIf(varBitmap[i])	
			elif digits[i] > 0:
				self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])
				self.model.Add(sum(self.cellValues[sumRow+j*vStep][sumCol+j*hStep] for j in range(digits[i])) == value).OnlyEnforceIf(varBitmap[i])
			else: # So if a digit is negative, we reverse the intended direction
				mySumRow = self.boardWidth-1-sumRow if rc == sudoku.Col else sumRow
				mySumCol = self.boardWidth-1-sumCol if rc == sudoku.Row else sumCol
				myHStep = -1 * hStep
				myVStep = -1 * vStep				
				self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])
				self.model.Add(sum(self.cellValues[mySumRow+j*myVStep][mySumCol+j*myHStep] for j in range(-1*digits[i])) == value).OnlyEnforceIf(varBitmap[i])
				
	def setXSum(self,row1,col1,rc,value):
		self.setXSumBase(row1,col1,rc,value,1)
		
	def setReverseXSum(self,row1,col1,rc,value):
		self.setXSumBase(row1,col1,rc,value,-1)
				
	def setDoubleXSum(self,row1,col1,rc,value):
		# A double X sum clue gives the sum of the X sums from each direction (top/bottom or left/right) in the clued row or column.
		row = row1 - 1 if rc == sudoku.Row else 0
		col = col1 - 1 if rc == sudoku.Col else 0
		hStep = 0 if rc == sudoku.Col else 1
		vStep = 0 if rc == sudoku.Row else 1
		
		digits = [x for x in self.digits if abs(x) <= self.boardWidth]
		varBitmap = self.__varBitmap('doubleXSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(digits)*len(digits))
			
		varTrack = 0
		for i in range(len(digits)):
			myRow = self.boardWidth-1 if rc == sudoku.Col and digits[i] < 0 else row
			myCol = self.boardWidth-1 if rc == sudoku.Row and digits[i] < 0 else col
			myVStep = vStep if digits[i] > 0 else -1 * vStep
			myHStep = hStep if digits[i] > 0 else -1 * hStep
			sumIVars = [self.cellValues[myRow+k*myVStep][myCol+k*myHStep] for k in range(abs(digits[i]))]
			for j in range(len(digits)):
				otherRow = self.boardWidth-1 if rc == sudoku.Col else row
				otherCol = self.boardWidth-1 if rc == sudoku.Row else col
				self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[varTrack])
				self.model.Add(self.cellValues[otherRow][otherCol] == digits[j]).OnlyEnforceIf(varBitmap[varTrack])
				myRow = 0 if rc == sudoku.Col and digits[j] < 0 else otherRow
				myCol = 0 if rc == sudoku.Row and digits[j] < 0 else otherCol
				myVStep = -1*vStep if digits[j] > 0 else vStep
				myHStep = -1*hStep if digits[j] > 0 else hStep
				sumJVars = [self.cellValues[myRow+k*myVStep][myCol+k*myHStep] for k in range(abs(digits[j]))]
				
				myVars = sumIVars + sumJVars
				if len(myVars) == 0:
					# In this case both digits are zero, could happen in a weird 0-8, double or nothing scenario
					if value == 0: # This is always true
						self.model.AddBoolAnd([varBitmap[varTrack][0]]).OnlyEnforceIf(varBitmap[varTrack])
					else: # This is never true
						self.model.AddBoolAnd([varBitmap[varTrack][0].Not()]).OnlyEnforceIf(varBitmap[varTrack])
				else:
					self.model.Add(sum(myVars) == value).OnlyEnforceIf(varBitmap[varTrack])
				varTrack = varTrack + 1
	
	def setXKropki(self,row1,col1,rc,wb,neg=False):
		# row,col are the coordinates of the cell containing the Kropki position, so no 9s allowed
		# rc is whether the cell is poiting to the row or column 0->row, 1->column
		# wb whether kropki is white or black, 0->white,1->black
		# neg: True if Kropki implies no other Kropkis can occur in row/col
			
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)		
		
		allowableDigits = [x for x in self.digits if x >= 1 and x <=self.boardWidth-1]
		varBitmap = self.__varBitmap('XKropkiPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits))
		lgr = self.model.NewBoolVar('XKropkiLargerRow{:d}Col{:d}RC{:d}'.format(row,col,rc))
		
		for i in range(len(allowableDigits)):
			self.model.Add(self.cellValues[row][col] == allowableDigits[i]).OnlyEnforceIf(varBitmap[i])
			for j in range(self.boardWidth-1):
				firstCell = self.cellValues[row+j*vStep][col+j*hStep]
				secondCell = self.cellValues[row+(j+1)*vStep][col+(j+1)*hStep]				
				if j == allowableDigits[i]-1:
					# First case: difference 1
					if wb == sudoku.White:
						self.model.Add(firstCell - secondCell == 1).OnlyEnforceIf(varBitmap[i] + [lgr])
						self.model.Add(secondCell - firstCell == 1).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
					# Ratio 2
					else:
						self.model.Add(firstCell - 2*secondCell == 0).OnlyEnforceIf(varBitmap[i] + [lgr])
						self.model.Add(secondCell - 2*firstCell == 0).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
				else:
					# Nothing forced...unless negative constraint
					if neg is True:
						if wb == sudoku.White:
							self.model.Add(firstCell - secondCell != 1).OnlyEnforceIf(varBitmap[i] + [lgr])
							self.model.Add(secondCell - firstCell != 1).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
						else:
							self.model.Add(firstCell - 2*secondCell != 0).OnlyEnforceIf(varBitmap[i] + [lgr])
							self.model.Add(secondCell - 2*firstCell != 0).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
							
	def setNumberedRoomBase(self,row1,col1,rc,value,pm):
		# row,col are the coordinates of the cell containing the index of the target cell
		# rc is whether things are row/column
		# value is the target value to place
		# pm: determines if these are normal numbered rooms or reverse (count from the opposite side)
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		posRow = row if rc == sudoku.Row or pm == 1 else self.boardWidth-1-row
		posCol = col if rc == sudoku.Col or pm == 1 else self.boardWidth-1-col
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		hStep = pm * hStep	# Change direction in case we're doing reverse
		vStep = pm * vStep
		
		digits = list(self.digits)
		varBitmap = self.__varBitmap('NumRoomPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(digits))
		
		for i in range(len(digits)):
			if digits[i] == 0 or abs(digits[i]) > self.boardWidth:	# No place to put digit...bury these cases
				self.model.AddBoolAnd([varBitmap[i][0].Not()]).OnlyEnforceIf(varBitmap[i])
			elif digits[i] > 0:
				self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])
				self.model.Add(self.cellValues[posRow+(digits[i]-1)*vStep][posCol+(digits[i]-1)*hStep] == value).OnlyEnforceIf(varBitmap[i])
			else: # So if a digit is negative, we reverse the intended direction
				myPosRow = self.boardWidth-1-posRow if rc == sudoku.Col else posRow
				myPosCol = self.boardWidth-1-posCol if rc == sudoku.Row else posCol
				myHStep = -1 * hStep
				myVStep = -1 * vStep				
				self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])
				self.model.Add(self.cellValues[myPosRow+(-1*digits[i]-1)*myVStep][myPosCol+(-1*digits[i]-1)*myHStep] == value).OnlyEnforceIf(varBitmap[i])
		
	def setNumberedRoom(self,row1,col1,rc,value):
		self.setNumberedRoomBase(row1,col1,rc,value,1)
		
	def setReverseNumberedRoom(self,row1,col1,rc,value):
		self.setNumberedRoomBase(row1,col1,rc,value,-1)
			
	def setSandwichSum(self,row1,col1,rc,value,digits=[]):
		# row,col are the coordinates of the cell containing the index of the target cell
		# rc is whether things are row/column
		# value is the sum of values between two given digits (highest and lowest by default)
		# digits the two digits in the digit set to bound the sandwich sums
		
		# If digits is null, set it to highest and lowest
		if len(digits) == 0:
			digits = [self.minDigit,self.maxDigit]
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		# This variable determines if the sandwich digits are adjacent. We have to treat this case separately, since we
		# cannot create a constraint with an empty sum
		adj = self.model.NewBoolVar('SandwichAdjacentRow{:d}Col{:d}RC{:d}'.format(row,col,rc))
		
		if value == 0:
			# This is the only case where the lowest and highest digits can be adjacent, which can happen in boardWidth-1 ways
			varBitmap = self.__varBitmap('Sandwich0PosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth-1)
			lgr = self.model.NewBoolVar('Sandwich0LargerRow{:d}Col{:d}RC{:d}'.format(row,col,rc))
					
			for j in range(self.boardWidth-1):
				firstCell = self.cellValues[row+j*vStep][col+j*hStep]
				secondCell = self.cellValues[row+(j+1)*vStep][col+(j+1)*hStep]
				# Note: High/low pairs forces if difference is maximal
				self.model.Add(firstCell == digits[0]).OnlyEnforceIf(varBitmap[j] + [lgr,adj])
				self.model.Add(secondCell == digits[1]).OnlyEnforceIf(varBitmap[j] + [lgr,adj])
				self.model.Add(firstCell == digits[1]).OnlyEnforceIf(varBitmap[j] + [lgr.Not(),adj])
				self.model.Add(secondCell == digits[0]).OnlyEnforceIf(varBitmap[j] + [lgr.Not(),adj])
		else:
			# If value is not 0, then we need to make sure adj does not occur, since otherwise constraint is ignored
			self.model.AddBoolAnd([adj.Not()]).OnlyEnforceIf(adj)
		
		# In this case there are spaces. Combinatorics helps here...there are 9 choose 2 minus (9-1) pairs of positions
		# where they can go. Man this new varBitmap function makes this easier..save a whole page of code. Notice: with varying digits,
		# we may still be able to get a zero sum, but that side was not the problem, so we can just put the conditions in and go.
		
		varBitmap = self.__varBitmap('SandwichPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth*(self.boardWidth-1) // 2 - (self.boardWidth-1))
		lgr = self.model.NewBoolVar('SandwichLargerRow{:d}Col{:d}RC{:d}'.format(row,col,rc))
			
		varTrack = 0
		for j in range(self.boardWidth-2):
			for k in range(j+2,self.boardWidth):
				firstCell = self.cellValues[row+j*vStep][col+j*hStep]
				secondCell = self.cellValues[row+k*vStep][col+k*hStep]
				self.model.Add(firstCell == digits[0]).OnlyEnforceIf(varBitmap[varTrack] + [lgr,adj.Not()])
				self.model.Add(secondCell == digits[1]).OnlyEnforceIf(varBitmap[varTrack] + [lgr,adj.Not()])
				self.model.Add(firstCell == digits[1]).OnlyEnforceIf(varBitmap[varTrack] + [lgr.Not(),adj.Not()])
				self.model.Add(secondCell == digits[0]).OnlyEnforceIf(varBitmap[varTrack] + [lgr.Not(),adj.Not()])
				self.model.Add(sum(self.cellValues[row+m*vStep][col+m*hStep] for m in range(j+1,k)) == value).OnlyEnforceIf(varBitmap[varTrack] + [adj.Not()])
				varTrack = varTrack + 1
					
	def setOpenfacedSandwichSum(self,row1,col1,rc,value,digit=9):
		# Also known as before 9, like a sandwich sum, but clue is the sum of all digits prior to the stopper digit, usually 9.
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		varBitmap = self.__varBitmap('OFSandwichPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
		
		for i in range(self.boardWidth):
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == digit).OnlyEnforceIf(varBitmap[i])
			if i == 0:
				if value != 0:
					self.model.AddBoolAnd([varBitmap[i][0].Not()]).OnlyEnforceIf(varBitmap[i])	# Bury it, cannot be this case.
			else:
				self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(i)) == value).OnlyEnforceIf(varBitmap[i])
	
	def setBeforeNine(self,row1,col1,rc,value):
		self.setOpenfacedSandwichSum(row1,col1,rc,value,digit=9)

	def setBattlefield(self,row1,col1,rc,value):
		# row,col are the coordinates of the cell next to the clue
		# rc is whether things are row/column
		# value is the sum of uncovered, or double covered, cells in the row, where the first cell on either side indicates the 
		# number of cells covered from each direction
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else 1
		vStep = 0 if rc == sudoku.Row else 1
		rFirst = row if rc == sudoku.Row else 0
		cFirst = col if rc == sudoku.Col else 0
		rLast = row if rc == sudoku.Row else self.boardWidth-1
		cLast = col if rc == sudoku.Col else self.boardWidth-1
		
		allowableDigits = [x for x in self.digits if x >= 1 and x <=self.boardWidth]
		varBitmap = self.__varBitmap('BattlefieldRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits)*(len(allowableDigits)-1))
		
		varTrack = 0
		for i in range(len(allowableDigits)):
			for j in range(len(allowableDigits)):
				if i == j: continue
				self.model.Add(self.cellValues[rFirst][cFirst] == allowableDigits[i]).OnlyEnforceIf(varBitmap[varTrack])
				self.model.Add(self.cellValues[rLast][cLast] == allowableDigits[j]).OnlyEnforceIf(varBitmap[varTrack])
				if (allowableDigits[i]+allowableDigits[j]) < self.boardWidth:
					# Add up gap between
					self.model.Add(sum(self.cellValues[rFirst+k*vStep][cFirst+k*hStep] for k in range(allowableDigits[i],self.boardWidth - allowableDigits[j])) == value).OnlyEnforceIf(varBitmap[varTrack])
				elif (allowableDigits[i]+allowableDigits[j]) == self.boardWidth:
					if value != 0: # Nothing in the middle, so cannot work if value !=0. If value = 0, no further constraints.
						self.model.AddBoolAnd([varBitmap[varTrack][0],varBitmap[varTrack][0].Not()]).OnlyEnforceIf(varBitmap[varTrack])
				else:
					self.model.Add(sum(self.cellValues[rFirst+k*vStep][cFirst+k*hStep] for k in range(self.boardWidth - allowableDigits[j],allowableDigits[i])) == value).OnlyEnforceIf(varBitmap[varTrack])
				varTrack = varTrack + 1
				
	def setPositionSum(self,row1,col1,rc,value1,value2):
		# row,col are the coordinates of the cell next to the clues
		# rc is whether things are row/column
		# value1 is the sum of the first two cells in the row/column
		# value2 is the sum of the cells which the first two cells index
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		allowableDigits = [x for x in self.digits if x >= 1 and x <=self.boardWidth]
		varBitmap = self.__varBitmap('PositionSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits)*(len(allowableDigits)-1))
		
		varTrack = 0
		for i in range(len(allowableDigits)):
			for j in range(len(allowableDigits)):
				if i == j: continue
				self.model.Add(self.cellValues[row][col] == allowableDigits[i]).OnlyEnforceIf(varBitmap[varTrack])
				self.model.Add(self.cellValues[row+vStep][col+hStep] == allowableDigits[j]).OnlyEnforceIf(varBitmap[varTrack])
				self.model.Add(self.cellValues[row][col] + self.cellValues[row+vStep][col+hStep] == value1).OnlyEnforceIf(varBitmap[varTrack])
				self.model.Add(self.cellValues[row+(allowableDigits[i]-1)*vStep][col+(allowableDigits[i]-1)*hStep] + self.cellValues[row+(allowableDigits[j]-1)*vStep][col+(allowableDigits[j]-1)*hStep] == value2).OnlyEnforceIf(varBitmap[varTrack])
				varTrack = varTrack + 1

	def setOutside(self,row1,col1,rc,valueList):
		# row,col are the coordinates of the cell next to the clues
		# rc is whether things are row/column
		# valueList is a list of values that must appear in the first region in that direction
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		# List of cell indices in the row/column we're looking at
		candCells = {(row+i*vStep,col+i*hStep) for i in range(self.boardWidth)}
		for i in range(len(self.regions)):
			if len({(row,col)} & set(self.regions[i])) > 0: currentRegion = i
			
		clueCells = list(candCells & set(self.regions[currentRegion]))
		vars = [[self.model.NewBoolVar('OutsideClue') for i in range(len(clueCells))] for j in range(len(valueList))]
		for j in range(len(valueList)):
			for i in range(len(clueCells)):
				self.model.Add(self.cellValues[clueCells[i][0]][clueCells[i][1]] == valueList[j]).OnlyEnforceIf(vars[j][i])
				self.model.Add(self.cellValues[clueCells[i][0]][clueCells[i][1]] != valueList[j]).OnlyEnforceIf(vars[j][i].Not())
			self.model.AddBoolOr(vars[j])

	def setCornerEdge(self,box1,ce,valueList):
		# box is the box number to which to apply the clue. 1-based so, upper left corner is 1, to its right is 2, etc.
		# ce specifies whether the clue is for corner (0) or edge (1). Use class variable Corner and Edge
		# valueList is the list of values to appear in these locations
		
		box = box1 - 1
		boxRow = box // self.boardSizeRoot
		boxCol = box % self.boardSizeRoot
		ulRow = self.boardSizeRoot * boxRow	# Cell in upper left corner of box
		ulCol = self.boardSizeRoot * boxCol
			
		for i in range(self.boardSizeRoot):
			for j in range(self.boardSizeRoot):
				if ((i > 0) and (i < self.boardSizeRoot - 1) and (j > 0) and (j < self.boardSizeRoot - 1)) or\
					((ce == self.Corner) and (i % (self.boardSizeRoot-1) != 0 or j % (self.boardSizeRoot-1) != 0)) or\
					((ce == self.Edge) and (i % (self.boardSizeRoot-1) == 0 and j % (self.boardSizeRoot-1) == 0)):	# Middle, edge, and corner square
						for k in valueList: self.model.Add(self.cellValues[ulRow+i][ulCol+j] != k)
						
	def setRossini(self,row1,col1,udlr):
		# row,col is the cell next to the clue
		# udlr determines whether the arrow points up/down or left/right
		# value is optional. By default the increase condition holds in the first region, but if value is set it will hold
		# only for a fixed number of cells.
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		rc = self.Row if udlr >= self.Left else self.Col
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)

		if self.isRossiniInitialized is not True:
			self.rossiniCells = [(row,col,rc)]
			self.isRossiniInitialized = True
		else:
			self.rossiniCells.append((row,col,rc))
		
		if self.rossiniLength == -1:	# We are using the default region-based cluing
			for i in range(len(self.regions)):
				if len({(row,col)} & set(self.regions[i])) > 0: region = i
			clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.boardWidth) if len({(row+i*vStep,col+i*hStep)} & set(self.regions[region])) > 0]
		else:
			clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.rossiniLength)]
			
		# So this is weird in external cluing, that the arrows are absolute with respect to the grid. So a left arrow on a row, regardless
		# of which side it is on, indicates the values increase from right to left. In this case, arrows on right or bottom are in the
		# "wrong" order, since they proceed from the edge into the grid (which is usually what you want.) So we reverse the array in these cases.
		
		if (rc == self.Row and col != 0) or (rc == self.Col and row != 0):
			clueCells.reverse()
			
		if udlr == self.Top or udlr == self.Left:		# Same value as self.Left
			for i in range(len(clueCells)-1):
				self.model.Add(clueCells[i] > clueCells[i+1])
		else:
			for i in range(len(clueCells)-1):
				self.model.Add(clueCells[i] < clueCells[i+1])
				
	def setRossiniLength(self,value):
		self.rossiniLength = value
	
	def setRossiniNegative(self):
		if self.isRossiniInitialized is not True:
			self.rossiniCells = []
			self.isRossiniInitialized = True
		self.isRossiniNegative = True
		
	def __applyRossiniNegative(self):
		for i in range(0,self.boardWidth,self.boardWidth-1):	# Gives two values 0 and self.boardWidth-1...picks top/bottom , left/right
			for j in range(self.boardWidth):					# Pick which index to process
				for k in range(2):									# Pick row/col
					row = j if k is self.Row else i
					col = j if k is self.Col else i
					if (row,col,k) not in self.rossiniCells:
						hStep = 0 if k == sudoku.Col else (1 if col == 0 else -1)
						vStep = 0 if k == sudoku.Row else (1 if row == 0 else -1)
						if self.rossiniLength == -1:	# We are using the default region-based cluing
							for m in range(len(self.regions)):
								if len({(row,col)} & set(self.regions[m])) > 0: region = m
							clueCells = [self.cellValues[row+m*vStep][col+m*hStep] for m in range(self.boardWidth) if len({(row+m*vStep,col+m*hStep)} & set(self.regions[region])) > 0]
						else:
							clueCells = [self.cellValues[row+m*vStep][col+m*hStep] for m in range(self.rossiniLength)]
						# Note: no need to reverse since we're going to exclude a run in either direction
						
						# We're going to test each triple for an up-down, or down-up pattern
						varlist = []
						n = len(clueCells)
						for x in range(n):
							for y in range(x+1,n):
								for z in range(y+1,n):
									good = self.model.NewBoolVar('RossiniNeg')
									ud = self.model.NewBoolVar('RossiniNeg')
									self.model.Add(clueCells[x] < clueCells[y]).OnlyEnforceIf([good,ud])
									self.model.Add(clueCells[z] < clueCells[y]).OnlyEnforceIf([good,ud])
									self.model.Add(clueCells[x] > clueCells[y]).OnlyEnforceIf([good,ud.Not()])
									self.model.Add(clueCells[z] > clueCells[y]).OnlyEnforceIf([good,ud.Not()])
									self.model.Add(clueCells[x] < clueCells[y]).OnlyEnforceIf([good.Not(),ud])
									self.model.Add(clueCells[y] < clueCells[z]).OnlyEnforceIf([good.Not(),ud])
									self.model.Add(clueCells[x] > clueCells[y]).OnlyEnforceIf([good.Not(),ud.Not()])
									self.model.Add(clueCells[y] > clueCells[z]).OnlyEnforceIf([good.Not(),ud.Not()])
									varlist.append(good)
						self.model.AddBoolOr(varlist)		# Just need one triple to be good
									
	def setMaxAscending(self,row1,col1,rc,value):
		# row,col are the coordinates of the cell containing the index of the target cell
		# rc is whether things are row/column
		# value is the length of the longest adjacent ascending run, looking from the clue
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		incBools = [self.model.NewBoolVar('MaxAscendingIncBoolRow{:d}Col{:d}RC{:d}'.format(row,col,rc)) for i in range(self.boardWidth-1)]
		incInts = [self.model.NewIntVar(0,1,'MaxAscendingIncIntRow{:d}Col{:d}RC{:d}'.format(row,col,rc)) for i in range(self.boardWidth-1)]
		for i in range(len(incBools)):
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] < self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep]).OnlyEnforceIf(incBools[i])
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] >= self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep]).OnlyEnforceIf(incBools[i].Not())
			self.model.Add(incInts[i] == 1).OnlyEnforceIf(incBools[i])
			self.model.Add(incInts[i] == 0).OnlyEnforceIf(incBools[i].Not())
			
		if value == 1:		# In this case the row/col must be strictly decreasing
			self.model.AddBoolAnd([x.Not() for x in incBools])
		else:
			lenBools = [self.model.NewBoolVar('MaxAscendingLenBoolRow{:d}Col{:d}RC{:d}'.format(row,col,rc)) for i in range(self.boardWidth+1-value)]
			for i in range(self.boardWidth+1-value):
				self.model.Add(sum([incInts[j] for j in range(i,i+value-1)]) == value-1).OnlyEnforceIf(lenBools[i])
				self.model.Add(sum([incInts[j] for j in range(i,i+value-1)]) < value-1).OnlyEnforceIf(lenBools[i].Not())
			self.model.AddBoolOr(lenBools)	#There is a run of length value
			
			for i in range(self.boardWidth-value):	#There is no longer run
				self.model.Add(sum([incInts[j] for j in range(i,i+value)]) < value)

	def setSkyscraper(self,row1,col1,rc,value):
		# row,col are the coordinates of the cell containing the index of the target cell
		# rc is whether things are row/column
		# value is the number of digits that can be "seen" (i.e. are greater than all their predecessors) from the direction of the clue
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		# Create Boolean variables to determine where cell i in the row (from the correct direction) is greater than each of its predecessors
		incVars = [[]]
		for i in range(1,self.boardWidth):
			t = []
			for j in range(i):
				c = self.model.NewBoolVar('SkyscraperRow{:d}Col{:d}Cell{:d}Cell{:d}'.format(row,col,i,j))
				t.append(c)
				self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] > self.cellValues[row+j*vStep][col+j*hStep]).OnlyEnforceIf(c)
				self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] < self.cellValues[row+j*vStep][col+j*hStep]).OnlyEnforceIf(c.Not())
			incVars.insert(i,t)
		
		seenBools = [self.model.NewBoolVar('SkyscraperSeenBool{:d}{:d}'.format(row+i*vStep,col+i*hStep)) for i in range(self.boardWidth)]
		seenInts = [self.model.NewIntVar(0,1,'SkyscraperSeenInt{:d}{:d}'.format(row+i*vStep,col+i*hStep)) for i in range(self.boardWidth)]
		for i in range(self.boardWidth):
			self.model.Add(seenInts[i] == 1).OnlyEnforceIf(seenBools[i])
			self.model.Add(seenInts[i] == 0).OnlyEnforceIf(seenBools[i].Not())
			
		# Need to treat i=0 separately, since it is always seen, so seenBool[0] is always true
		self.model.AddBoolAnd([seenBools[0]])
		
		for i in range(1,self.boardWidth):
			self.model.AddBoolAnd(incVars[i]).OnlyEnforceIf(seenBools[i])
			self.model.AddBoolAnd([seenBools[i]]).OnlyEnforceIf(incVars[i])
			
		self.model.Add(sum([seenInts[i] for i in range(self.boardWidth)]) == value)
		
	def setNextToNine(self,row1,col1,rc,values,digit=9):
		if type(values) is int:
			values  = [values]
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		varBitmap = self.__varBitmap('NextToNineRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
		lr = self.model.NewBoolVar('NextToNineLeftRightChoice')
		lrA = [lr,lr.Not()]
		for i in range(self.boardWidth):
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == digit).OnlyEnforceIf(varBitmap[i])
			for j in range(len(values)):
				if i == 0:
					self.model.Add(self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep] == values[j]).OnlyEnforceIf(varBitmap[i])
					self.model.AddBoolAnd([lr]).OnlyEnforceIf(varBitmap[i])
				elif i == self.boardWidth - 1:
					self.model.Add(self.cellValues[row+(i-1)*vStep][col+(i-1)*hStep] == values[j]).OnlyEnforceIf(varBitmap[i])
					self.model.AddBoolAnd([lr.Not()]).OnlyEnforceIf(varBitmap[i])
				else:
					# If there are two values, the %2 trick in the variable ensures they alternate, so that values are put on different sides
					self.model.Add(self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep] == values[j]).OnlyEnforceIf(varBitmap[i] + [lrA[j%2]])
					self.model.Add(self.cellValues[row+(i-1)*vStep][col+(i-1)*hStep] == values[j]).OnlyEnforceIf(varBitmap[i] + [lrA[(j+1)%2]])

	def setMaximumRun(self,row1,col1,rc,value,length=3):
		# row,col are the coordinates of the cell containing the index of the target cell
		# rc is whether things are row/column
		# value is the largest sum of any contiguous set of triplets in the clued row/column
		# length is the number of cells to add to create the sum
		
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		numSums = self.boardWidth - length + 1
		runVars = [self.model.NewBoolVar('MaximumRunVar') for i in range(numSums)]
		for i in range(numSums):
			self.model.Add(sum(self.cellValues[row+(i+j)*vStep][col+(i+j)*hStep] for j in range(length)) == value).OnlyEnforceIf(runVars[i])
			self.model.Add(sum(self.cellValues[row+(i+j)*vStep][col+(i+j)*hStep] for j in range(length)) < value).OnlyEnforceIf(runVars[i].Not())
		self.model.AddBoolOr(runVars)
		
	def setMaximumTriplet(self,row1,col1,rc,value):
		self.setMaximumRun(row1,col1,rc,value,length=3)
		
	def setDescriptivePair(self,row1,col1,rc,values):
		# Value is a list of two digits XY: either X appears in the Yth place, or Y appears in the Xth place in the row/column
		if type(values) is int:
			values = tuple(map(int,list(str(values))))
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		c = self.model.NewBoolVar('DescriptivePair')
		
		myRow = row if values[0] > 0 or rc == sudoku.Row else self.boardWidth-1-row
		myCol = col if values[0] > 0 or rc == sudoku.Col else self.boardWidth-1-col
		myHStep = hStep if values[0] > 0 else -1*hStep
		myVStep = vStep if values[0] > 0 else -1*vStep
		self.model.Add(self.cellValues[myRow+(abs(values[0])-1)*myVStep][myCol+(abs(values[0])-1)*myHStep] == values[1]).OnlyEnforceIf(c)
		
		myRow = row if values[1] > 0 or rc == sudoku.Row else self.boardWidth-1-row
		myCol = col if values[1] > 0 or rc == sudoku.Col else self.boardWidth-1-col
		myHStep = hStep if values[1] > 0 else -1*hStep
		myVStep = vStep if values[1] > 0 else -1*vStep
		self.model.Add(self.cellValues[myRow+(abs(values[1])-1)*myVStep][myCol+(abs(values[1])-1)*myHStep] == values[0]).OnlyEnforceIf(c.Not())

	def setMinimax(self,row1,col1,rc,value,length=-1):
		# row,col is the cell next to the clue
		# rc is whether things are row/column
		# value is the value of the sum of the largest and smallest digits in the range
		# length: if not present, range over which to find min/max is defined by the region the clue is next to
		# If given, the clue will instead work on a fixed number of cells from the edge
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)

		if length == -1:	# We are using the default region-based cluing
			for i in range(len(self.regions)):
				if len({(row,col)} & set(self.regions[i])) > 0: region = i
			clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.boardWidth) if len({(row+i*vStep,col+i*hStep)} & set(self.regions[region])) > 0]
		else:
			clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(length)]
			
		# OK, we copied that from Rossini, now the hard part: min/max. Best just to do it, since that's
		# usually the best for these LP problems.
		minVars = [self.model.NewBoolVar('minimax') for i in range(len(clueCells))]
		maxVars = [self.model.NewBoolVar('minimax') for i in range(len(clueCells))]
		for i in range(len(clueCells)):
			for j in range(i,len(clueCells)):
				self.model.Add(clueCells[i] >= clueCells[j]).OnlyEnforceIf(maxVars[i])
				self.model.Add(clueCells[i] >= clueCells[j]).OnlyEnforceIf(minVars[j])
				self.model.Add(clueCells[i] <= clueCells[j]).OnlyEnforceIf(minVars[i])
				self.model.Add(clueCells[i] <= clueCells[j]).OnlyEnforceIf(maxVars[j])
				self.model.Add(clueCells[i]+clueCells[j] == value).OnlyEnforceIf([maxVars[j],minVars[i]])
				self.model.Add(clueCells[i]+clueCells[j] == value).OnlyEnforceIf([maxVars[i],minVars[j]])
		self.model.AddBoolOr(minVars)
		self.model.AddBoolOr(maxVars)
		
	def setMaximin(self,row1,col1,rc,value,length=-1):
		# row,col is the cell next to the clue
		# rc is whether things are row/column
		# value is the value of the difference of the largest and smallest digits in the range
		# length: if not present, range over which to find min/max is defined by the region the clue is next to
		# If given, the clue will instead work on a fixed number of cells from the edge
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)

		if length == -1:	# We are using the default region-based cluing
			for i in range(len(self.regions)):
				if len({(row,col)} & set(self.regions[i])) > 0: region = i
			clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.boardWidth) if len({(row+i*vStep,col+i*hStep)} & set(self.regions[region])) > 0]
		else:
			clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(length)]
			
		# OK, we copied that from Rossini, now the hard part: min/max. Best just to do it, since that's
		# usually the best for these LP problems.
		minVars = [self.model.NewBoolVar('maximin') for i in range(len(clueCells))]
		maxVars = [self.model.NewBoolVar('maximin') for i in range(len(clueCells))]
		for i in range(len(clueCells)):
			for j in range(i,len(clueCells)):
				self.model.Add(clueCells[i] >= clueCells[j]).OnlyEnforceIf(maxVars[i])
				self.model.Add(clueCells[i] >= clueCells[j]).OnlyEnforceIf(minVars[j])
				self.model.Add(clueCells[i] <= clueCells[j]).OnlyEnforceIf(minVars[i])
				self.model.Add(clueCells[i] <= clueCells[j]).OnlyEnforceIf(maxVars[j])
				self.model.Add(clueCells[j]-clueCells[i] == value).OnlyEnforceIf([maxVars[j],minVars[i]])
				self.model.Add(clueCells[i]-clueCells[j] == value).OnlyEnforceIf([maxVars[i],minVars[j]])
		self.model.AddBoolOr(minVars)
		self.model.AddBoolOr(maxVars)

	def setFullRank(self,row1,col1,rc,value):
		if self.isFullRank is False:
			self.__setFullRank()
			
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		i = row if rc==sudoku.Row else col
		j = rc
		k = (0 if col == 0 else 1) if rc==sudoku.Row else (0 if row == 0 else 1)
		self.model.Add(self.rcRank[4*i+2*j+k] == value)

	def setParityParty(self,row1,col1,rc,value):
		if self.isParity is False:
			self.__setParity()
			
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		varBitmap = self.__varBitmap('ParityParty{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
		for i in range(self.boardWidth):
			self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(i)) == value).OnlyEnforceIf(varBitmap[i])
			if i > 1:
				for j in range(1,i-1):
					self.model.Add(self.cellParity[row][col] == self.cellParity[row+j*vStep][col+j*hStep]).OnlyEnforceIf(varBitmap[i])
				self.model.Add(self.cellParity[row][col] != self.cellParity[row+(i-1)*vStep][col+(i-1)*hStep]).OnlyEnforceIf(varBitmap[i])

####2x2 constraints
	def setQuadruple(self,row,col=-1,values=-1):
		if col == -1:
			T = self.__procCell(row)
			row = T[0]
			col = T[1]
			values = [T[i] for i in range(2,len(T))]
		for x in values:
			if values.count(x) > 2:
				print('Quadruple at {:d},{:d} cannot have more than two instances of {:d}'.format(row,col,x))
				sys.exit()
			else:
				# Regardless of whether a digit appears twice in quad, there is the possibility that digit DOES appear twice
				# If we do not control for this possibility, we may have our bits flopping between the two values, preventing
				# the script from determining a unique solution. So, we set up two variables. One to determine whether or
				# not the digit appears twice, and one to determine which diagonal the digits lie on.
				bitDouble = self.model.NewBoolVar('QuadrupleDigitDoubledQueryRow{:d}Col{:d}Value{:d}'.format(row,col,x))
				bitDiagonal = self.model.NewBoolVar('QuadrupleDiagonalQueryRow{:d}Col{:d}Value{:d}'.format(row,col,x))
				self.model.Add(self.cellValues[row][col] == x).OnlyEnforceIf([bitDouble,bitDiagonal])
				self.model.Add(self.cellValues[row+1][col+1] == x).OnlyEnforceIf([bitDouble,bitDiagonal])
				self.model.Add(self.cellValues[row][col+1] == x).OnlyEnforceIf([bitDouble,bitDiagonal.Not()])
				self.model.Add(self.cellValues[row+1][col] == x).OnlyEnforceIf([bitDouble,bitDiagonal.Not()])
				
				if values.count(x) == 2:
					# If the digit actually appears twice in the list, force bitDouble to be true
					self.model.AddBoolAnd([bitDouble])
				else:
					# Otherwise allow the possibility the digit appears only once.
					# These bits determine the location of the digit if it is NOT doubled.
					bit1 = self.model.NewBoolVar('Quadruple1Row{:d}Col{:d}Value{:d}'.format(row,col,x))
					bit2 = self.model.NewBoolVar('Quadruple2Row{:d}Col{:d}Value{:d}'.format(row,col,x))
					self.model.Add(self.cellValues[row][col] == x).OnlyEnforceIf([bitDouble.Not(),bit1,bit2])
					self.model.Add(self.cellValues[row][col+1] == x).OnlyEnforceIf([bitDouble.Not(),bit1,bit2.Not()])
					self.model.Add(self.cellValues[row+1][col+1] == x).OnlyEnforceIf([bitDouble.Not(),bit1.Not(),bit2.Not()])
					self.model.Add(self.cellValues[row+1][col] == x).OnlyEnforceIf([bitDouble.Not(),bit1.Not(),bit2])
					
	def setQuadrupleArray(self,cells):
		for x in cells: self.setQuadruple(x)
	
	def setQuadSum(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		# Quad sums: a dot at the corner of four cells indicate that one of the cells is the sum of the other three
		bit1 = self.model.NewBoolVar('QuadSumMaxVRow{:d}Col{:d}'.format(row,col))
		bit2 = self.model.NewBoolVar('QuadSumMaxHRow{:d}Col{:d}'.format(row,col))
		self.model.Add(self.cellValues[row][col] == self.cellValues[row][col+1]+self.cellValues[row+1][col]+self.cellValues[row+1][col+1]).OnlyEnforceIf([bit1,bit2])
		self.model.Add(self.cellValues[row][col+1] == self.cellValues[row][col]+self.cellValues[row+1][col]+self.cellValues[row+1][col+1]).OnlyEnforceIf([bit1,bit2.Not()])
		self.model.Add(self.cellValues[row+1][col+1] == self.cellValues[row][col]+self.cellValues[row+1][col]+self.cellValues[row][col+1]).OnlyEnforceIf([bit1.Not(),bit2.Not()])
		self.model.Add(self.cellValues[row+1][col] == self.cellValues[row][col]+self.cellValues[row+1][col+1]+self.cellValues[row][col+1]).OnlyEnforceIf([bit1.Not(),bit2])
		
	def setQuadSumArray(self,cells):
		for x in cells: self.setQuadSum(x)

	def setBattenburg(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		if self.isBattenburgInitialized is not True:
			self.battenburgCells = [(row,col)]
			self.isBattenburgInitialized = True
		else:
			self.battenburgCells.append((row,col))
			
		if self.isParity is False:
			self.__setParity()
			
		# Now that we can track parity globally, only need to check that the three pairs: top, right, and bottom are different parity.
		# This ensures either OE  or  EO
		#                     EO      OE
		self.model.Add(self.cellParity[row][col] != self.cellParity[row][col+1])
		self.model.Add(self.cellParity[row][col+1] != self.cellParity[row+1][col+1])
		self.model.Add(self.cellParity[row+1][col] != self.cellParity[row+1][col+1])
				
	def setBattenburgArray(self,cells):
		for x in cells: self.setBattenburg(x)
			
	def setBattenburgNegative(self):
		if self.isBattenburgInitialized is not True:
			self.battenburgCells = []
			self.isBattenburgInitialized = True
		self.isBattenburgNegative = True
		
		if self.isParity is False:
			self.__setParity()
			
	def setAntiBattenburg(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		# No need to set battenburgInitialized...if we call negative later, this will just be duplicated.
		bit1 = self.model.NewBoolVar('AntiBattenburgTopSameParityTestRow{:d}Col{:d}'.format(row,col))
		bit2 = self.model.NewBoolVar('AntiBattenburgRightSameParityTestRow{:d}Col{:d}'.format(row,col))
		bit3 = self.model.NewBoolVar('AntiBattenburgBottomSameParityTestRow{:d}Col{:d}'.format(row,col))
		self.model.Add(self.cellParity[row][col] == self.cellParity[row][col+1]).OnlyEnforceIf(bit1)
		self.model.Add(self.cellParity[row][col] != self.cellParity[row][col+1]).OnlyEnforceIf(bit1.Not())
		self.model.Add(self.cellParity[row][col+1] == self.cellParity[row+1][col+1]).OnlyEnforceIf(bit2)
		self.model.Add(self.cellParity[row][col+1] != self.cellParity[row+1][col+1]).OnlyEnforceIf(bit2.Not())
		self.model.Add(self.cellParity[row+1][col+1] == self.cellParity[row+1][col]).OnlyEnforceIf(bit3)
		self.model.Add(self.cellParity[row+1][col+1] != self.cellParity[row+1][col]).OnlyEnforceIf(bit3.Not())
		self.model.AddBoolOr([bit1,bit2,bit3])
		
	def setAntiBattenburgArray(self,cells):
		for x in cells: self.setAntiBattenburg(x)
		
	def __applyBattenburgNegative(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth-1):
				if (i,j) not in self.battenburgCells:
					self.setAntiBattenburg(i,j)

	def setEntropyQuad(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		# A 2x2 square of cells is entropic if it includes a low, middle, and high digit
		if self.isEntropyQuadInitialized is not True:
			self.entropyQuadCells = [(row,col)]
			self.isEntropyQuadInitialized = True
		else:
			self.entropyQuadCells.append((row,col))
			
		if self.isEntropy is False:
			self.__setEntropy()
		
		self.model.AddForbiddenAssignments([self.cellEntropy[row][col],self.cellEntropy[row][col+1],self.cellEntropy[row+1][col],self.cellEntropy[row+1][col+1]],[(0,0,0,0),(1,1,1,1),(2,2,2,2),(0,0,0,1),(0,0,1,0),(0,1,0,0),(1,0,0,0),(0,0,0,2),(0,0,2,0),(0,2,0,0),(2,0,0,0),(1,1,1,0),(1,1,0,1),(1,0,1,1),(0,1,1,1),(1,1,1,2),(1,1,2,1),(1,2,1,1),(2,1,1,1),(2,2,2,0),(2,2,0,2),(2,0,2,2),(0,2,2,2),(2,2,2,1),(2,2,1,2),(2,1,2,2),(1,2,2,2),(0,0,1,1),(0,0,2,2),(1,1,0,0),(1,1,2,2),(2,2,0,0),(2,2,1,1),(0,1,0,1),(0,2,0,2),(1,0,1,0),(1,2,1,2),(2,0,2,0),(2,1,2,1),(0,1,1,0),(0,2,2,0),(1,0,0,1),(1,2,2,1),(2,0,0,2),(2,1,1,2)])
		
	def setEntropyQuadArray(self,inlist):
		for x in inlist: self.setEntropyQuad(x)
		
	def setEntropyQuadNegative(self):
		if self.isEntropyQuadInitialized is not True:
			self.entropyQuadCells = []
			self.isEntropyQuadInitialized = True
		
		if self.isEntropy is False:
			self.__setEntropy()
			
		self.isEntropyQuadNegative = True

	def setAntiEntropyQuad(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
			
		if self.isEntropy is False:
			self.__setEntropy()
		
		self.model.AddAllowedAssignments([self.cellEntropy[row][col],self.cellEntropy[row][col+1],self.cellEntropy[row+1][col],self.cellEntropy[row+1][col+1]],[(0,0,0,0),(1,1,1,1),(2,2,2,2),(0,0,0,1),(0,0,1,0),(0,1,0,0),(1,0,0,0),(0,0,0,2),(0,0,2,0),(0,2,0,0),(2,0,0,0),(1,1,1,0),(1,1,0,1),(1,0,1,1),(0,1,1,1),(1,1,1,2),(1,1,2,1),(1,2,1,1),(2,1,1,1),(2,2,2,0),(2,2,0,2),(2,0,2,2),(0,2,2,2),(2,2,2,1),(2,2,1,2),(2,1,2,2),(1,2,2,2),(0,0,1,1),(0,0,2,2),(1,1,0,0),(1,1,2,2),(2,2,0,0),(2,2,1,1),(0,1,0,1),(0,2,0,2),(1,0,1,0),(1,2,1,2),(2,0,2,0),(2,1,2,1),(0,1,1,0),(0,2,2,0),(1,0,0,1),(1,2,2,1),(2,0,0,2),(2,1,1,2)])
		
	def setAntiEntropyQuadArray(self,inlist):
		for x in inlist: self.setAntiEntropyQuad(x)

	def __applyEntropyQuadNegative(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth-1):
				if (i,j) not in self.entropyQuadCells:
					self.setAntiEntropyQuad(i,j)
					
	def setParityQuad(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		# A 2x2 square of cells is entropic if it includes a low, middle, and high digit
		if self.isParityQuadInitialized is not True:
			self.parityQuadCells = [(row,col)]
			self.isParityQuadInitialized = True
		else:
			self.parityQuadCells.append((row,col))
			
		if self.isParity is False:
			self.__setParity()
		
		self.model.Add(sum(self.cellParity[row+i][col+j] for i in range(2) for j in range(2)) > 0)
		self.model.Add(sum(self.cellParity[row+i][col+j] for i in range(2) for j in range(2)) < 4)

	def setParityQuadArray(self,inlist):
		for x in inlist: self.setParityQuad(x)
		
	def setParityQuadNegative(self):
		if self.isParityQuadInitialized is not True:
			self.parityQuadCells = []
			self.isParityQuadInitialized = True
		
		if self.isParity is False:
			self.__setParity()
			
		self.isParityQuadNegative = True

	def setAntiParityQuad(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		if self.isParity is False:
			self.__setParity()
			
		c = self.model.NewBoolVar('AntiParityQuad')
		self.model.Add(sum(self.cellParity[row+i][col+j] for i in range(2) for j in range(2)) == 0).OnlyEnforceIf(c)
		self.model.Add(sum(self.cellParity[row+i][col+j] for i in range(2) for j in range(2)) == 4).OnlyEnforceIf(c.Not())
				
	def setAntiParityQuadArray(self,inlist):
		for x in inlist: self.setAntiParityQuad(x)

	def __applyParityQuadNegative(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth-1):
				if (i,j) not in self.parityQuadCells:
					self.setAntiParityQuad(i,j)
					
	def setEntropyBattenburg(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		# A 2x2 square of cells is an entropy battenburg if no two adjacent cells on the quad have the same rank
		if self.isEntropyBattenburgInitialized is not True:
			self.entropyBattenburgCells = [(row,col)]
			self.isEntropyBattenburgInitialized = True
		else:
			self.entropyBattenburgCells.append((row,col))
			
		if self.isEntropy is False:
			self.__setEntropy()
		
		self.model.Add(self.cellEntropy[row][col] != self.cellEntropy[row][col+1])
		self.model.Add(self.cellEntropy[row][col+1] != self.cellEntropy[row+1][col+1])
		self.model.Add(self.cellEntropy[row+1][col+1] != self.cellEntropy[row+1][col])
		self.model.Add(self.cellEntropy[row+1][col] != self.cellEntropy[row][col])
		
	def setEntropyBattenburgArray(self,inlist):
		for x in inlist: self.setEntropyBattenburg(x)
		
	def setAntiEntropyBattenburg(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		bit1 = self.model.NewBoolVar('AntiEntrBattRow{:d}Col{:d}V1'.format(row,col))
		bit2 = self.model.NewBoolVar('AntiEntrBattRow{:d}Col{:d}V2'.format(row,col))
		bit3 = self.model.NewBoolVar('AntiEntrBattRow{:d}Col{:d}V3'.format(row,col))
		bit4 = self.model.NewBoolVar('AntiEntrBattRow{:d}Col{:d}V4'.format(row,col))
		self.model.Add(self.cellEntropy[row][col] == self.cellEntropy[row][col+1]).OnlyEnforceIf(bit1)
		self.model.Add(self.cellEntropy[row][col] != self.cellEntropy[row][col+1]).OnlyEnforceIf(bit1.Not())
		self.model.Add(self.cellEntropy[row][col+1] == self.cellEntropy[row+1][col+1]).OnlyEnforceIf(bit2)
		self.model.Add(self.cellEntropy[row][col+1] != self.cellEntropy[row+1][col+1]).OnlyEnforceIf(bit2.Not())
		self.model.Add(self.cellEntropy[row+1][col+1] == self.cellEntropy[row+1][col]).OnlyEnforceIf(bit3)
		self.model.Add(self.cellEntropy[row+1][col+1] != self.cellEntropy[row+1][col]).OnlyEnforceIf(bit3.Not())
		self.model.Add(self.cellEntropy[row+1][col] == self.cellEntropy[row][col]).OnlyEnforceIf(bit4)
		self.model.Add(self.cellEntropy[row+1][col] != self.cellEntropy[row][col]).OnlyEnforceIf(bit4.Not())
		self.model.AddBoolOr([bit1,bit2,bit3,bit4])
		
	def setAntiEntropyBattenburgArray(self,inlist):
		for x in inlist: self.setAntiEntropyBattenburg(x)

	def setEntropyBattenburgNegative(self):
		if self.isEntropyBattenburgInitialized is not True:
			self.entropyBattenburgCells = []
			self.isEntropyBattenburgInitialized = True
		
		if self.isEntropy is False:
			self.__setEntropy()
			
		self.isEntropyBattenburgNegative = True
		
	def __applyEntropyBattenburgNegative(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth-1):
				if (i,j) not in self.entropyBattenburgCells:
					self.setAntiEntropyBattenburg(i,j)
					
	def setQuadMaxArrow(self,row,col=-1,dir1=-1,dir2=-1):
		# row,col defines the 2x2 to which the arrow applies
		# dir1,dir2 defines which cell the arrow points to
		if col == -1:
			(row,col,dir1,dir2) = self.__procCell(row)
		
		for i in range(2):
			for j in range(2):
				if i != dir1 or j != dir2:
					self.model.Add(self.cellValues[row+i][col+j] < self.cellValues[row+dir1][col+dir2])
					
	def setQuadMaxArrowArray(self,cells):
		for x in cells: self.setQuadMaxArrow(x)
		
	def setQuadMaxValue(self,row,col=-1,value=-1):
		# row,col defines the 2x2 to which the clue applies
		# value is the largest value which occurs in the quad
		if col == -1:
			(row,col,value) = self.__procCell(row)

		equalVars = [self.model.NewBoolVar('QuadMaxValueEqualRow{:d}Col{:d}'.format(row+i,col+j)) for i in range(2) for j in range(2)]
		for i in range(2):
			for j in range(2):
				self.model.Add(self.cellValues[row+i][col+j] == value).OnlyEnforceIf(equalVars[2*i+j])
				self.model.Add(self.cellValues[row+i][col+j] < value).OnlyEnforceIf(equalVars[2*i+j].Not())
		self.model.AddBoolOr(equalVars)
		
	def setQuadMaxValueArray(self,cells):
		for x in cells: self.setQuadMaxValue(x)
		
	def setQuadMaxParityValue(self,row,col=-1,values=-1,unique=True):
		# row,col defines the 2x2 to which the clue applies
		# value is the largest value *of its parity* which occurs in the quad
		if self.isParity is False:
			self.__setParity()
			
		if col == -1:
			T = self.__procCell(row)
			row = T[0]
			col = T[1]
			values = [T[i] for i in range(2,len(T))]
		else:
			row = row - 1
			col = col - 1
		pBits = [self.model.NewBoolVar('QuadMaxParityValue') for i in range(4)]
		pBitPairs = [[pBits[i],pBits[i].Not()] for i in range(4)]
		for i in range(4):
			self.model.Add(self.cellParity[row+(i//2)][col+(i%2)] == 1).OnlyEnforceIf(pBits[i].Not())
			self.model.Add(self.cellParity[row+(i//2)][col+(i%2)] == 0).OnlyEnforceIf(pBits[i])
		for x in values:
			vBits = [self.model.NewBoolVar('QuadMaxParityValue') for i in range(4)]
			for i in range(4):
				self.model.Add(self.cellValues[row+(i//2)][col+(i%2)] == x).OnlyEnforceIf(vBits[i])
				self.model.Add(self.cellValues[row+(i//2)][col+(i%2)] < x).OnlyEnforceIf([vBits[i].Not(),pBitPairs[i][x%2]])
				self.model.Add(self.cellValues[row+(i//2)][col+(i%2)] != x).OnlyEnforceIf([vBits[i].Not(),pBitPairs[i][x%2].Not()])
			self.model.AddBoolOr(vBits)	# Ensures the max value appears
		
			if unique is True:
				vInts = [self.model.NewIntVar(0,1,'QuadMaxParityValue') for i in range(4)]
				for i in range(4):
					self.model.Add(vInts[i] == 1).OnlyEnforceIf(vBits[i])
					self.model.Add(vInts[i] == 0).OnlyEnforceIf(vBits[i].Not())
				self.model.Add(sum(vInts) == 1)
		
	def setConsecutiveQuad(self,row,col=-1,value=-1):
		# Of the SIX pairs of cells, if value is 0 (white), exactly one pair is consecutive. If value is 1 (black), at least two pairs are consecutive. If value is 2 (anti), no pairs are consecutive
		
		if col == -1:
			(row,col,value) = self.__procCell(row)
		bits = [self.model.NewBoolVar('ConsecQuadRow{:d}Col{:d}'.format(row,col)) for i in range(6)]
		intVars = [self.model.NewIntVar(0,1,'ConsecQuadIntRow{:d}Col{:d}'.format(row,col)) for i in range(6)]
		c = [(0,0,0,1),(0,0,1,0),(0,0,1,1),(0,1,1,0),(0,1,1,1),(1,0,1,1)]
		for i in range(6):
			self.model.Add(intVars[i] == 1).OnlyEnforceIf(bits[i])
			self.model.Add(intVars[i] == 0).OnlyEnforceIf(bits[i].Not())
			gt = self.model.NewBoolVar('ConsecQuadGT')
			self.model.Add(self.cellValues[row+c[i][0]][col+c[i][1]] - self.cellValues[row+c[i][2]][col+c[i][3]] >= 0).OnlyEnforceIf(gt)
			self.model.Add(self.cellValues[row+c[i][0]][col+c[i][1]] - self.cellValues[row+c[i][2]][col+c[i][3]] < 0).OnlyEnforceIf(gt.Not())
			self.model.Add(self.cellValues[row+c[i][0]][col+c[i][1]] - self.cellValues[row+c[i][2]][col+c[i][3]] == 1).OnlyEnforceIf([bits[i],gt])
			self.model.Add(self.cellValues[row+c[i][0]][col+c[i][1]] - self.cellValues[row+c[i][2]][col+c[i][3]] == -1).OnlyEnforceIf([bits[i],gt.Not()])
			self.model.Add(self.cellValues[row+c[i][0]][col+c[i][1]] - self.cellValues[row+c[i][2]][col+c[i][3]] != 1).OnlyEnforceIf([bits[i].Not(),gt])
			self.model.Add(self.cellValues[row+c[i][0]][col+c[i][1]] - self.cellValues[row+c[i][2]][col+c[i][3]] != -1).OnlyEnforceIf([bits[i].Not(),gt.Not()])
		
		if value == sudoku.White:
			self.model.Add(sum(intVars) == 1)
		elif value == sudoku.Black:
			self.model.Add(sum(intVars) > 1)
		else:
			self.model.Add(sum(intVars) == 0)
	
	def setConsecutiveQuadWhite(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		self.setConsecutiveQuad(row,col,sudoku.White)
	
	def setConsecutiveQuadWhiteArray(self,cells):
		for x in cells: self.setConsecutiveQuadWhite(x)
		
	def setConsecutiveQuadBlack(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		self.setConsecutiveQuad(row,col,sudoku.Black)
	
	def setConsecutiveQuadBlackArray(self,cells):
		for x in cells: self.setConsecutiveQuadBlack(x)	
		
	def setConsecutiveQuadArray(self,cells):
		cellList = self.__procCellList(cells)
		for x in cellList:
			if x[2] == sudoku.White:
				self.setConsecutiveQuadWhite(x[0],x[1])
			else:
				self.setConsecutiveQuadBlack(x[0],x[1])

	def setAntiConsecutiveQuad(self,row,col=-1):
		# To label a single cell as specifically not having any consecutive pairs
		if col == -1:
			(row,col) = self.__procCell(row)
		self.setConsecutiveQuad(row,col,2)
		
	def setAntiConsecutiveQuadArray(self,cells):
		for x in cells: self.setAntiConsecutiveQuad(x)

	def setConsecutiveQuadNegative(self):
		if self.isConsecutiveQuadInitialized is not True:
			self.consecutiveQuadCells = []
			self.isConsecutiveQuadInitialized = True
		self.isConsecutiveQuadNegative = True
		
	def __applyConsecutiveQuadNegative(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth-1):
				if (i,j) not in self.consecutiveQuadCells:
					self.setAntiConsecutiveQuad(i,j)	
		
####Linear constraints
	def setArrow(self,inlist):
		inlist = self.__procCellList(inlist)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))))
		
	def setHeavyArrow(self,inlist,mult=2):
		inlist = self.__procCellList(inlist)
		self.model.Add(mult*self.cellValues[inlist[0][0]][inlist[0][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))))
		
	def setDoubleArrow(self,inlist):
		inlist = self.__procCellList(inlist)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] + self.cellValues[inlist[-1][0]][inlist[-1][1]]== sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist)-1)))

	def setPointingArrow(self,inlist):
		inlist = self.__procCellList(inlist)
		# Pointing arrow is an arrow, but it also points, extending in last direction, to its total sum
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))))
	
		vert = inlist[-1][0]-inlist[-2][0] # Vertical delta to compute extension direction
		horiz = inlist[-1][1]-inlist[-2][1] # Horizontal delta to compute extension direction
		
		tcells = [self.cellValues[inlist[-1][0]+k*vert][inlist[-1][1]+k*horiz] for k in range(1,self.boardWidth) if inlist[-1][0]+k*vert in range(self.boardWidth) and inlist[-1][1]+k*horiz in range(self.boardWidth)]
		tvars = [self.model.NewBoolVar('PointingArrowFinderHeadRow{:d}Col{:d}Cell{:d}'.format(inlist[0][0],inlist[0][1],i)) for i in range(len(tcells))]
		for j in range(len(tvars)):
			self.model.Add(tcells[j] == self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf(tvars[j])
			self.model.Add(tcells[j] != self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf(tvars[j].Not())
		self.model.AddBoolOr(tvars)
		
	def setMultiDigitSumArrow(self,inlist,n=1):
		# Arrow where the bulb is multiple digits. First n elements of the list are in the circle, most significant (100s or 10s, usually) to least.
		inlist = self.__procCellList(inlist)
		circle = self.cellValues[inlist[0][0]][inlist[0][1]]
		for i in range(1,n):
			circle = 10*circle + self.cellValues[inlist[i][0]][inlist[i][1]]
		self.model.Add(circle == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(n,len(inlist))))
	
	def setMissingArrow(self,inlist):
		# Arrow where one end or the other is the sum of the other cells along the arrow
		inlist = self.__procCellList(inlist)
		c = self.model.NewBoolVar('MissingArrow')
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist)))).OnlyEnforceIf(c)
		self.model.Add(self.cellValues[inlist[-1][0]][inlist[-1][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist)-1))).OnlyEnforceIf(c.Not())
		
	def setRepeatingArrow(self,inlist,repeat=2):
		inlist = self.__procCellList(inlist)
		bulb = inlist.pop(0)
		varBitmap = self.__varBitmap('RepeatingArrow',math.comb(len(inlist),repeat-1))
		varTrack = 0
		bulbVar = self.cellValues[bulb[0]][bulb[1]]
		
		cI = CombinationIterator(len(inlist)-1,repeat-1)
		comb = cI.getNext()
		while comb is not None:
			ind = [-1] + comb + [len(inlist)-1]
			for j in range(len(ind)-1):
				self.model.Add(sum(self.cellValues[inlist[k][0]][inlist[k][1]] for k in range(ind[j]+1,ind[j+1]+1)) == bulbVar).OnlyEnforceIf(varBitmap[varTrack])
			comb = cI.getNext()
			varTrack = varTrack + 1
	
	def setThermo(self,inlist,slow=False,missing=False):
		inlist = self.__procCellList(inlist)
		if missing is False:
			for j in range(len(inlist)-1):
				if slow is True:
					self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] <= self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
				else:
					self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
		else:
			c = self.model.NewBoolVar('MissingThermo')
			for j in range(len(inlist)-1):
				if slow is True:
					self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] <= self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(c)
					self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] >= self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(c.Not())
				else:
					self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(c)
					self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(c.Not())
			
	def setSlowThermo(self,inlist,missing=False):
		self.setThermo(inlist,True,missing)
	
	def setOddEvenThermo(self,inlist,slow=False,missing=False):
		if self.isParity is False:
			self.__setParity()
		self.setThermo(inlist,slow,missing)
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellParity[inlist[j][0]][inlist[j][1]] == self.cellParity[inlist[j+1][0]][inlist[j+1][1]])
			
	def setSlowOddEvenThermo(self,inlist,missing=False):
		self.setOddEvenThermo(inlist,True,missing)
		
	def setMissingThermo(self,inlist,slow=False):
		self.setThermo(inlist,slow,True)
			
	def setCountTheOddsLine(self,inlist):
		if self.isParity is False:
			self.__setParity()
			
		inlist = self.__procCellList(inlist)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == sum([self.cellParity[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))]))

	def setKeypadKnightLine(self,inlist):
		if self.boardWidth != 9:
			print('Keypad lines only supported on 9x9 board')
			sys.exit()
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.AddAllowedAssignments([self.cellValues[inlist[j][0]][inlist[j][1]],self.cellValues[inlist[j+1][0]][inlist[j+1][1]]],[(1,6),(1,8),(2,7),(2,9),(3,4),(3,8),(4,3),(4,9),(6,1),(6,7),(7,2),(7,6),(8,1),(8,3),(9,2),(9,4)])
			
	def setKeypadKingLine(self,inlist):
		if self.boardWidth != 9:
			print('Keypad lines only supported on 9x9 board')
			sys.exit()
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.AddAllowedAssignments([self.cellValues[inlist[j][0]][inlist[j][1]],self.cellValues[inlist[j+1][0]][inlist[j+1][1]]],[(1,2),(1,4),(1,5),(2,1),(2,4),(2,5),(2,6),(2,3),(3,2),(3,5),(3,6),(4,1),(4,2),(4,5),(4,8),(4,7),(5,1),(5,2),(5,3),(5,4),(5,6),(5,7),(5,8),(5,9),(6,3),(6,2),(6,5),(6,8),(6,9),(7,4),(7,5),(7,8),(8,7),(8,4),(8,5),(8,6),(8,9),(9,8),(9,5),(9,6)])
			
	def setPalindromeLine(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist) // 2):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] == self.cellValues[inlist[-j-1][0]][inlist[-j-1][1]])
			
	def setParindromeLine(self,inlist):
		if self.isParity is False:
			self.__setParity()
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist) // 2):
			self.model.Add(self.cellParity[inlist[j][0]][inlist[j][1]] == self.cellParity[inlist[-j-1][0]][inlist[-j-1][1]])
			
	def setWeakPalindromeLine(self,inlist):
		if self.boardWidth != 9:
			print('Keyboard lines only supported on 9x9 board')
			sys.exit()
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist) // 2):
			self.model.AddAllowedAssignments([self.cellValues[inlist[j][0]][inlist[j][1]],self.cellValues[inlist[-j-1][0]][inlist[-j-1][1]]],[(1,1),(1,3),(3,1),(3,3),(2,2),(2,4),(4,2),(4,4),(5,5),(5,7),(5,9),(7,5),(7,7),(7,9),(6,6),(6,8),(8,6),(8,8)])
	
	def setParityLine(self,inlist):
		if self.isParity is False:
			self.__setParity()
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellParity[inlist[j][0]][inlist[j][1]] != self.cellParity[inlist[j+1][0]][inlist[j+1][1]])
			
	def setRenbanLine(self,inlist):
		inlist = self.__procCellList(inlist)
		self.model.AddAllDifferent([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))])
		for x in range(len(inlist)):
			for y in range(len(inlist)):
				self.model.Add(self.cellValues[inlist[x][0]][inlist[x][1]]-self.cellValues[inlist[y][0]][inlist[y][1]] < len(inlist))
				
	def setNotRenbanLine(self,inlist):
		inlist = self.__procCellList(inlist)
		
		distBools = [self.model.NewBoolVar('NotRenbanDistinct') for i in range(len(inlist)) for j in range(len(inlist)) if i < j]
		varTrack = 0
		for i in range(len(inlist)):
			for j in range(i+1,len(inlist)):
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(distBools[varTrack])
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] != self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(distBools[varTrack].Not())
				varTrack = varTrack + 1
		
		diffBools = [self.model.NewBoolVar('NotRenbanDistinct') for i in range(len(inlist)) for j in range(len(inlist))]
		varTrack = 0
		for i in range(len(inlist)):
			for j in range(len(inlist)):
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] - self.cellValues[inlist[j][0]][inlist[j][1]] >= len(inlist)).OnlyEnforceIf(diffBools[varTrack])
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] - self.cellValues[inlist[j][0]][inlist[j][1]] < len(inlist)).OnlyEnforceIf(diffBools[varTrack].Not())
				varTrack = varTrack + 1
		self.model.AddBoolOr(distBools + diffBools)
				
	def setRunOnRenbanLine(self,inlist,n=5):
		# Each contiguous subsegment of length n is a Renban of length n
		# Note: we could just chunk this out as a bunch of overlapping Renbans, but that'll add a lot of repeated subtraction conditions
		# Let's do the first one that way, so we aren't duplicating quite as much code
		if len(inlist) >= n:
			self.setRenbanLine(inlist[0:n]) # Note: do this before doing procCellList, since the Renban call will proc it
		inlist = self.__procCellList(inlist)
		for i in range(n,len(inlist)):
			self.model.AddAllDifferent([self.cellValues[inlist[i-j][0]][inlist[i-j][1]] for j in range(n)])
			for j in range(n):
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]]-self.cellValues[inlist[i-j][0]][inlist[i-j][1]] < n)
				self.model.Add(self.cellValues[inlist[i-j][0]][inlist[i-j][1]]-self.cellValues[inlist[i][0]][inlist[i][1]] < n)
					
	def setMinWhispersLine(self,inlist,value):
		# Sets a whispers line where the minimum difference between two cells on the line is value
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			bit = self.model.NewBoolVar('MaxWhisperBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= value).OnlyEnforceIf(bit)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= -1*value).OnlyEnforceIf(bit.Not())
	
	def setMaxWhispersLine(self,inlist,value):
		# Sets a whispersline where the maximum difference between two cells on the line is value
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= value)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= -1*value)
	
	def setGermanWhispersLine(self,inlist):
		self.setMinWhispersLine(inlist,5)
			
	def setDutchWhispersLine(self,inlist):
		self.setMinWhispersLine(inlist,4)
			
	def setChineseWhispersLine(self,inlist):
		self.setMaxWhispersLine(inlist,2)
			
	def setEntropicLine(self,inlist):
		inlist = self.__procCellList(inlist)
		if self.isEntropy is False:
			self.__setEntropy()
		
		if len(inlist) == 2:
			self.model.Add(self.cellEntropy[inlist[0][0]][inlist[0][1]] != self.cellEntropy[inlist[1][0]][inlist[1][1]])
		else:
			for j in range(len(inlist)-2):
				self.model.AddAllDifferent([self.cellEntropy[inlist[j][0]][inlist[j][1]],self.cellEntropy[inlist[j+1][0]][inlist[j+1][1]],self.cellEntropy[inlist[j+2][0]][inlist[j+2][1]]])

	def setModularLine(self,inlist):
		inlist = self.__procCellList(inlist)
		if self.isModular is False:
			self.__setModular()
		
		if len(inlist) == 2:
			self.model.Add(self.cellModular[inlist[0][0]][inlist[0][1]] != self.cellModular[inlist[1][0]][inlist[1][1]])
		else:
			for j in range(len(inlist)-2):
				self.model.AddAllDifferent([self.cellModular[inlist[j][0]][inlist[j][1]],self.cellModular[inlist[j+1][0]][inlist[j+1][1]],self.cellModular[inlist[j+2][0]][inlist[j+2][1]]])
				
	def setBetweenLine(self,inlist):
		inlist = self.__procCellList(inlist)
		c = self.model.NewBoolVar('BetweenRow{:d}Col{:d}ToRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1],inlist[-1][0],inlist[-1][1]))
		
		# Case c true: first element of line is largest
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c)
		for j in range(1,len(inlist)-1):
			self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c)
			
		# Case c false: last element of line is largest
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] < self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c.Not())
		for j in range(1,len(inlist)-1):
			self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] < self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c.Not())
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c.Not())
			
	def setLockoutLine(self,inlist):
		inlist = self.__procCellList(inlist)
		c = self.model.NewBoolVar('LockoutRow{:d}Col{:d}ToRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1],inlist[-1][0],inlist[-1][1]))
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] - self.cellValues[inlist[-1][0]][inlist[-1][1]] >= 4).OnlyEnforceIf(c)
		self.model.Add(self.cellValues[inlist[-1][0]][inlist[-1][1]] - self.cellValues[inlist[0][0]][inlist[0][1]] >= 4).OnlyEnforceIf(c.Not())
		
		for j in range(1,len(inlist)-1):
			# c picks whether cell is greater than both endpoints, or less
			c = self.model.NewBoolVar('LockoutMidRow{:d}Col{:d}FromRow{:d}Col{:d}ToRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1],inlist[0][0],inlist[0][1],inlist[-1][0],inlist[-1][1]))
			self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[inlist[-1][0]][inlist[-1][1]] > self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] < self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c.Not())
			self.model.Add(self.cellValues[inlist[-1][0]][inlist[-1][1]] < self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c.Not())
			
	def setRegionSumLine(self,inlist):
		inlist = self.__procCellList(inlist)
		sumSets = []
		for region in self.regions:
			tempSum = [self.cellValues[x[0]][x[1]] for x in set(region) & set(inlist)]
			if len(tempSum) != 0: sumSets.append(tempSum)

		baseSum = sum(x for x in sumSets[0])
		for i in range(1,len(sumSets)):
			self.model.Add(sum(x for x in sumSets[i]) == baseSum)
			
	def setRegionSegmentSumLine(self,inlist):
		# This is used for variants where the sums for each segment of the line have the same sum
		# in each region. If a line enters a region twice, each segment must have the same sum as all
		# other segments...the visits do not aggregate
		inlist = self.__procCellList(inlist)
		
		sumSets = []
		currentRegionStart = 0
		for i in range(len(self.regions)):
			if len({inlist[0]} & set(self.regions[i])) > 0: currentRegion = i
		print(str(currentRegion))
		for j in range(1,len(inlist)):
			for i in range(len(self.regions)):
				if len({inlist[j]} & set(self.regions[i])) > 0: thisRegion = i
			if thisRegion != currentRegion:
				sumSets.append([self.cellValues[x[0]][x[1]] for x in inlist[currentRegionStart:j]])
				currentRegionStart = j
				currentRegion = thisRegion
		# Need to do it again since the last segment is left in the queue.	
		sumSets.append([self.cellValues[x[0]][x[1]] for x in inlist[currentRegionStart:]])

		baseSum = sum(sumSets[0])
		for i in range(1,len(sumSets)):
			self.model.Add(sum(sumSets[i]) == baseSum)

	def setDoublingLine(self,inlist):
		# Every digit that appears on a doubling line appears exactly twice
		inlist = self.__procCellList(inlist)
		
		vars = [[None for j in range(len(inlist))] for i in range(len(inlist))]
		for i in range(len(inlist)):
			for j in range(i+1,len(inlist)):
				cB = self.model.NewBoolVar('DoublingLineBool')
				cI = self.model.NewIntVar(0,1,'DoublingLineIntCell{:d}{:d}'.format(i,j))
				self.model.Add(cI == 1).OnlyEnforceIf(cB)		# Ties the two variables together
				self.model.Add(cI == 0).OnlyEnforceIf(cB.Not())	# Int version needed to add
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(cB)
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] != self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(cB.Not())
				vars[i][j] = cI
				vars[j][i] = cI
		
		for i in range(len(inlist)):
			self.model.Add(sum(vars[i][j] for j in range(len(inlist)) if j != i) == 1)	#For each cell along line, exactly one cell has a matching value
			
	def setShiftLine(self,inlist):
		# Like a palindrome, except one side of the line is uniformly one larger than its counterpart on the other side
		inlist = self.__procCellList(inlist)
		c = self.model.NewBoolVar('ShiftLineR{:d}C{:d}'.format(inlist[0][0],inlist[0][1]))
		for j in range(len(inlist) // 2):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] == self.cellValues[inlist[-j-1][0]][inlist[-j-1][1] + 1]).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + 1 == self.cellValues[inlist[-j-1][0]][inlist[-j-1][1]]).OnlyEnforceIf(c.Not())
			
	def setUpAndDownLine(self,inlist):
		inlist = self.__procCellList(inlist)
		c = self.model.NewBoolVar('UpAndDownLineR{:d}C{:d}'.format(inlist[0][0],inlist[0][1]))
		for i in range(len(inlist)-1):
			if i % 2 == 0:
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] > self.cellValues[inlist[i+1][0]][inlist[i+1][1]]).OnlyEnforceIf(c)
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < self.cellValues[inlist[i+1][0]][inlist[i+1][1]]).OnlyEnforceIf(c.Not())
			else:
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < self.cellValues[inlist[i+1][0]][inlist[i+1][1]]).OnlyEnforceIf(c)
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] > self.cellValues[inlist[i+1][0]][inlist[i+1][1]]).OnlyEnforceIf(c.Not())

	def setAverageLine(self,inlist):
		inlist = self.__procCellList(inlist)
		self.model.Add((len(inlist)-1)*self.cellValues[inlist[0][0]][inlist[0][1]] == sum([self.cellValues[inlist[i][0]][inlist[i][1]] for i in range(1,len(inlist))]))
		
	def setNabnerLine(self,inlist):
		# All cells on the line have a difference of at least 2, so we put each pair as its own line
		for i in range(len(inlist)):
			for j in range(i+1,len(inlist)):
				self.setMinWhispersLine([inlist[i],inlist[j]],2)
				
	def setParityCountLine(self,inlist):
		if self.isParity is False:
			self.__setParity()
		inlist = self.__procCellList(inlist)
		c = self.model.NewBoolVar('ParityCountLine')
		e = self.model.NewBoolVar('ParityCountLine')	# Variable to test if endpoints are equal, in which case we prevent c from flapping.
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] + self.cellValues[inlist[-1][0]][inlist[-1][1]] == len(inlist))
		self.model.Add(sum(self.cellParity[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))) == self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf(c)
		self.model.Add(sum(self.cellParity[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))) == self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf(c.Not())
		
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(e)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] != self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(e.Not())
		self.model.AddBoolAnd(c).OnlyEnforceIf(e)
		
	def set10Line(self,inlist,value=10):
		inlist = self.__procCellList(inlist)
		varBitmap = self.__varBitmap('10Line',2**(len(inlist)-1))
		varTrack = 0
		for i in range(len(inlist)):
			cI = CombinationIterator(len(inlist)-2,i)
			comb = cI.getNext()
			while comb is not None:
				ind = [-1] + comb + [len(inlist)-1]
				for j in range(len(ind)-1):
					self.model.Add(sum(self.cellValues[inlist[k][0]][inlist[k][1]] for k in range(ind[j]+1,ind[j+1]+1)) == value).OnlyEnforceIf(varBitmap[varTrack])
				comb = cI.getNext()
				varTrack = varTrack + 1
				
	def setClockLine(self,inlist):
		inlist = self.__procCellList(inlist)
		for i in range(len(inlist)-1):
			c = self.model.NewBoolVar('ClockLineDiff')
			g = self.model.NewBoolVar('ClockLineGT')
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] - self.cellValues[inlist[i+1][0]][inlist[i+1][1]] == 2).OnlyEnforceIf([c,g])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] - self.cellValues[inlist[i+1][0]][inlist[i+1][1]] == 7).OnlyEnforceIf([c.Not(),g])
			self.model.Add(self.cellValues[inlist[i+1][0]][inlist[i+1][1]] - self.cellValues[inlist[i][0]][inlist[i][1]] == 2).OnlyEnforceIf([c,g.Not()])
			self.model.Add(self.cellValues[inlist[i+1][0]][inlist[i+1][1]] - self.cellValues[inlist[i][0]][inlist[i][1]] == 7).OnlyEnforceIf([c.Not(),g.Not()])

####Model solving
	def applyNegativeConstraints(self):
		# This method is used to prepare the model for solution. If negative constraints have been set, i.e. all items not marked
		# cannot be marked. These constraints cannot be applied at time of assertion, since there may be new marks added after
		# the assertion. This function applies all negative constraints just prior to solving, and is called by the solver function.
		
		if self.isBattenburgNegative is True: self.__applyBattenburgNegative()
		if self.isKropkiNegative is True: self.__applyKropkiNegative()
		if self.isXVNegative is True: self.__applyXVNegative()
		if self.isXVXVNegative is True: self.__applyXVXVNegative()
		if self.isEntropyQuadNegative is True: self.__applyEntropyQuadNegative()
		if self.isEntropyBattenburgNegative is True: self.__applyEntropyBattenburgNegative()
		if self.isFriendlyNegative is True: self.__applyFriendlyNegative()
		if self.isRossiniNegative is True: self.__applyRossiniNegative()
		if self.isConsecutiveQuadNegative is True: self.__applyConsecutiveQuadNegative()
		if self.isParityQuadNegative is True: self.__applyParityQuadNegative()

	def findSolution(self,test=False):
		self.applyNegativeConstraints()
		self.solver = cp_model.CpSolver()
		consolidatedCellValues = []
		for tempArray in self.cellValues: consolidatedCellValues = consolidatedCellValues + tempArray
		solution_printer = SolutionPrinter(consolidatedCellValues)
		self.solveStatus = self.solver.Solve(self.model)
	
		if test is True:
			return self.testStringSolution()
		else:
			print('Solver status = %s' % self.solver.StatusName(self.solveStatus))
			if self.solveStatus == cp_model.OPTIMAL:
				print('Solution found!')
				self.printCurrentSolution()

	def countSolutions(self,printAll = False,debug = False,test=False):
		self.applyNegativeConstraints()
		self.solver = cp_model.CpSolver()
		consolidatedCellValues = []
		for tempArray in self.cellValues: consolidatedCellValues = consolidatedCellValues + tempArray
		if debug is True:
			solution_printer = SolutionPrinter(self.allVars)
		else:	
			solution_printer = SolutionPrinter(consolidatedCellValues)
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
		
	def addExcludedDigit(self,row,col=-1,value=-1):
		# Strictly for listing candidates, sets a value that has been excluded from a cell
		if col == -1:
			(row,col,value) = self.__procCell(row)
		digitList = list(self.digits)
		self.candTests[row][col][digitList.index(value)] = False
		
	def addExcludedDigitArray(self,list):
		for x in list: self.addExcludedDigit(x)
	
	def listCellCandidates(self,row,col=-1,quiet=False):
		if col == -1:
			(row,col) = self.__procCell(row)
			
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
		else:
			return good

##### Utilities
	def __varBitmap(self,string,num):
		# Utility function to create a list of Boolean variable propositions that encode num possibilities exactly.
		# string is used to label the variables
		# Implements model constraints to ensure "extra"
		
		n = math.ceil(math.log(num,2))
		bits = []
		for i in range(n):
			bits.append(self.model.NewBoolVar(string + 'BM{:d}'.format(i)))
		
		# Create full array of first n-1 variables. We need them all.
		var = [[bits[0]],[bits[0].Not()]]
		for i in range(1,n-1):
			for j in range(len(var)):
				var.append(var[j] + [bits[i].Not()])
				var[j].append(bits[i])
		
		# We repeat the same procedure, except when we are done, instead of appending new variable lists.
		# we create constraints to ensure these cases cannot happen
		
		for j in range(len(var)):
			if len(var) < num:
				var.append(var[j] + [bits[-1].Not()])
			else:
				# This ensures an unused combination of variables cannot occur
				#self.model.AddBoolAnd([bits[-1]]).OnlyEnforceIf(var[j] + [bits[-1].Not()])
				self.model.AddBoolAnd(var[j] + [bits[-1]]).OnlyEnforceIf(var[j] + [bits[-1].Not()])
				
			# Either way append to existing lists
			var[j].append(bits[-1])
			
		return var
		
	def __procCell(self,cell):
		# Utility function that processes an individual cell into a tuple format
		
		# Note: This function assumes that the first two elements are a row/column index, 1-base
		# so it converts them to 0-base.
		
		if type(cell) is tuple:
			myCell = cell 
		elif type(cell) is str:
			myCell = tuple(map(int,list(cell)))
		elif type(cell) is int:
			myCell = tuple(map(int,list(str(cell))))
			
		return tuple([myCell[i]-1 for i in range(2)] + [myCell[i] for i in range(2,len(myCell))])
			
	def __procCellList(self,inlist):
		# Utility function to process a list from one of several input formats into the tuple format
		# required by our functions
		return list(map(lambda x: self.__procCell(x),inlist))
		
	def getOrthogonalNeighbors(self,i,j):
		return [(i+k,j+m) for k in [-1,0,1] for m in [-1,0,1] if i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth and abs(k) != abs(m)]
		
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
		
		self.isXVInitialized = False
		self.isXVNegative = False
		
		self.isXVXVInitialized = False
		self.isXVXVNegative = False
		
		self.isEntropyQuadInitialized = False
		self.isEntropyQuadNegative = False
		
		self.isEntropyBattenburgInitialized = False
		self.isEntropyBattenburgNegative = False
		
		self.isConsecutiveQuadInitialized = False
		self.isConsecutiveQuadNegative = False
		
		self.isParityQuadInitialized = False
		self.isParityQuadNegative = False
		
		self.isParity = False
		self.isEntropy = False
		self.isModular = False
		self.isFullRank = False
		
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
		inlist = self.__procCellList(inlist)
		self.regions.append(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in self.regions[-1]])
		self.model.Add(sum(self.doubleInt[x[0]][x[1]] for x in inlist) == 1)	# Ensure one doubler per region
				
	def setTransform(self,row,col=-1):
		if col == -1:
			(row,col) = self._sudoku__procCell(row)
		self.model.AddBoolAnd([self.double[row][col]])
	
	def setNotTransform(self,row,col=-1):
		if col == -1:
			(row,col) = self._sudoku__procCell(row)
		self.model.AddBoolAnd([self.double[row][col].Not()])
	
	def setGiven(self,row,col=-1,value=-1):
		if col == -1:
			(row,col,value) = self._sudoku__procCell(row)
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
			(row,col,value) = self._sudoku__procCell(row)
		self.candTests[row][col][value-1] = False
		
	def addExcludedDigitArray(self,list):
		for x in list: self.addExcludedDigit(x)
	
	def listCellCandidates(self,row,col=-1,quiet=False):
		if col == -1:
			(row,col) = self._sudoku__procCell(row)
			
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
		cellTransformSudoku.__init__(self,boardSizeRoot,canRepeatDigits=canRepeatDigits,irregular=irregular,digitSet=digitSet)
		self.ratio = ratio
		self.shift = shift
		
	def transformDoublerCell(self,i,j):
		self.model.Add(self.cellValues[i][j] == self.ratio*self.baseValues[i][j]+self.shift).OnlyEnforceIf([self.double[i][j]])
		
	def transformDoublerValue(self,value):
		return {self.ratio*value+self.shift}
		
class japaneseSumSudoku(sudoku):
	"""A class used to implement Japanese Sum puzzles."""
	
	def __init__(self,boardSizeRoot,irregular=None,digitSet=None):
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
		
		self.isXVInitialized = False
		self.isXVNegative = False
		
		self.isXVXVInitialized = False
		self.isXVXVNegative = False
		
		self.isEntropyQuadInitialized = False
		self.isEntropyQuadNegative = False
		
		self.isEntropyBattenburgInitialized = False
		self.isEntropyBattenburgNegative = False
		
		self.isConsecutiveQuadInitialized = False
		self.isConsecutiveQuadNegative = False
		
		self.isParityQuadInitialized = False
		self.isParityQuadNegative = False
		
		self.isParity = False
		self.isEntropy = False
		self.isModular = False
		self.isFullRank = False
		
		if digitSet is None:
			self.digits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit

		self.model = cp_model.CpModel()
		self.cellValues = []
		
		# Create the variables containing the cell values
		for rowIndex in range(self.boardWidth):
			tempArray = []
			for colIndex in range(self.boardWidth):
				tempCell = self.model.NewIntVar(self.minDigit,self.maxDigit,'cellValue{:d}{:d}'.format(rowIndex,colIndex))
				if (self.maxDigit - self.minDigit) >= self.boardWidth:	#Digit set is not continguous, so force values
					self.model.AddAllowedAssignments([tempCell],[(x,) for x in digitSet])
				tempArray.append(tempCell)
			self.cellValues.insert(rowIndex,tempArray)
			
		# Create rules to ensure rows and columns have no repeats
		for rcIndex in range(self.boardWidth):
			self.model.AddAllDifferent([self.cellValues[rcIndex][crIndex] for crIndex in range(self.boardWidth)]) 	# Rows
			self.model.AddAllDifferent([self.cellValues[crIndex][rcIndex] for crIndex in range(self.boardWidth)]) 	# Columns

		# Now deal with regions. Default to boxes...leaving stub for irregular Sudoku for now
		self.regions = []
		if irregular is None:
			self._sudoku__setBoxes()
			
		# Finally, create array of shading Booleans to determine which cells are shaded.
		self.cellShaded = []
		
		for rowIndex in range(self.boardWidth):
			tempArray = []
			for colIndex in range(self.boardWidth):
				tempArray.append(self.model.NewBoolVar('cellShaded{:d}{:d}'.format(rowIndex,colIndex)))
			self.cellShaded.insert(rowIndex,tempArray)
			
	def setJapaneseSum(self,row1,col1,rc,value):
		# row,col are the coordinates of the cell next to the clue
		# rc is whether things are row/column
		# value is a list of sums of unshaded cells that need to be achieved. Use 0 for ?, cluing that a sum exists but is not given
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else 1
		vStep = 0 if rc == sudoku.Row else 1
		
		# Need variables to determine if the left/top cell is shaded, and if right/bottom cell is shaded, since that affects the combinatorics
		ltShaded = self.model.NewBoolVar('JapaneseSumLTRow{:d}Col{:d}'.format(row,col))
		rbShaded = self.model.NewBoolVar('JapaneseSumRBRow{:d}Col{:d}'.format(row,col))
		
		# First let's deal with the case where both ends are unshaded. It's easiest to see the combinatorics with examples:
		# One clue:    .........
		# Two clues:   ...xxx...
		# Three clues: ..x...x..
		# Four clues:  .x..x.xx.
		# Five clues:  .x.x.x.x.
		# The important thing to look at is the *changes* between shaded and unshded in these cases:
		# One clue: 0
		# Two clues: 2
		# Three clues: 4
		# Four clues: 6
		# Five clues: 8
		# So by engineering induction, the number of changes is 2*(# clues) - 2.
		# In theory, any combination of changes could lead to a possible solution, so we need to look at Binomial(boardWidth-1,2*(# clues)-2), since there
		# are boardWidth - 1 inter-cell gaps where a change can take place.
		
		if len(value) == 1 or (len(value) == (self.boardWidth+1)//2 and self.boardWidth%2 == 1):	# Hack since if there is only one combination varBitmap throws an error
			varBitmap = [[]]
		elif len(value) < (self.boardWidth+1)//2:
			varBitmap = self._sudoku__varBitmap('JapaneseSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),math.comb(self.boardWidth-1,2*len(value)-2))
			# Need to force these variables to a single value in the other cases
			self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded,rbShaded])
			self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded,rbShaded.Not()])
			self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded.Not(),rbShaded])
		else: # Do the die here, since if this case can't work, the others definitely can't
			print ("Japanese Sum in row {:d} column {:d} cannot be achieved in this grid size")
			sys.exit()

		cI = CombinationIterator(self.boardWidth-2,2*len(value)-2)
		comb = cI.getNext()
		varTrack = 0
		while comb is not None:
			shade = False
			unShadeIndex = 0
			ind = [-1] + comb + [self.boardWidth-1]
			for i in range(len(ind)-1):
				for j in range(ind[i]+1,ind[i+1]+1):
					if shade is True:
						self.model.AddBoolAnd([self.cellShaded[row+j*vStep][col+j*hStep]]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded.Not(),rbShaded.Not()])
					else:
						self.model.AddBoolAnd([self.cellShaded[row+j*vStep][col+j*hStep].Not()]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded.Not(),rbShaded.Not()])
				if shade is not True:
					if value[unShadeIndex] > 0:
						self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(ind[i]+1,ind[i+1]+1)) == value[unShadeIndex]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded.Not(),rbShaded.Not()])
					unShadeIndex = unShadeIndex + 1
				shade = not shade
			varTrack = varTrack + 1
			comb = cI.getNext()

		# Now the other cases. If just one end cell is shaded, we need to add one more change. If both unshaded, we add two more changes.
		# But other than that it should just be copy and paste. Part of me feels like I should functionize this instead of just copying. Nah...
		
		# ltShaded, rb not
		if len(value) <= self.boardWidth//2:
			if len(value) == self.boardWidth//2 and self.boardWidth%2 == 0:
				varBitmap = [[]]
			else:
				varBitmap = self._sudoku__varBitmap('JapaneseSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),math.comb(self.boardWidth-1,2*len(value)-1))
				# Need to force these variables to a single value in the other cases
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded,rbShaded])
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded.Not(),rbShaded.Not()])
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded.Not(),rbShaded])
			cI = CombinationIterator(self.boardWidth-2,2*len(value)-1)
			comb = cI.getNext()
			varTrack = 0
			while comb is not None:
				shade = True			# Note: we start shaded
				unShadeIndex = 0
				ind = [-1] + comb + [self.boardWidth-1]
				for i in range(len(ind)-1):
					for j in range(ind[i]+1,ind[i+1]+1):
						if shade is True:
							self.model.AddBoolAnd([self.cellShaded[row+j*vStep][col+j*hStep]]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded,rbShaded.Not()])
						else:
							self.model.AddBoolAnd([self.cellShaded[row+j*vStep][col+j*hStep].Not()]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded,rbShaded.Not()])
					if shade is not True:
						if value[unShadeIndex] > 0:
							self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(ind[i]+1,ind[i+1]+1)) == value[unShadeIndex]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded,rbShaded.Not()])
						unShadeIndex = unShadeIndex + 1
					shade = not shade
				varTrack = varTrack + 1
				comb = cI.getNext()

			# rbShaded, lt not
			if len(value) == self.boardWidth//2 and self.boardWidth%2 == 0:
				varBitmap = [[]]
			else:
				varBitmap = self._sudoku__varBitmap('JapaneseSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),math.comb(self.boardWidth-1,2*len(value)-1))
				# Need to force these variables to a single value in the other cases
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded,rbShaded])
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded,rbShaded.Not()])
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded.Not(),rbShaded.Not()])
			cI = CombinationIterator(self.boardWidth-2,2*len(value)-1)
			comb = cI.getNext()
			varTrack = 0
			while comb is not None:
				shade = False			# Note: we start unshaded
				unShadeIndex = 0
				ind = [-1] + comb + [self.boardWidth-1]
				for i in range(len(ind)-1):
					for j in range(ind[i]+1,ind[i+1]+1):
						if shade is True:
							self.model.AddBoolAnd([self.cellShaded[row+j*vStep][col+j*hStep]]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded.Not(),rbShaded])
						else:
							self.model.AddBoolAnd([self.cellShaded[row+j*vStep][col+j*hStep].Not()]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded.Not(),rbShaded])
					if shade is not True:
						if value[unShadeIndex] > 0:
							self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(ind[i]+1,ind[i+1]+1)) == value[unShadeIndex]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded.Not(),rbShaded])
						unShadeIndex = unShadeIndex + 1
					shade = not shade
				varTrack = varTrack + 1
				comb = cI.getNext()
		else:
			# These cases can't be realized...kill them
			self.model.AddBoolAnd([rbShaded]).OnlyEnforceIf([ltShaded,rbShaded.Not()])
			self.model.AddBoolAnd([ltShaded]).OnlyEnforceIf([ltShaded.Not(),rbShaded])

		# Both shaded
		if len(value) <= (self.boardWidth-1)//2:
			if len(value) == (self.boardWidth-1)//2 and self.boardWidth%2 == 1:
				varBitmap = [[]]
			else:
				varBitmap = self._sudoku__varBitmap('JapaneseSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),math.comb(self.boardWidth-1,2*len(value)))
				# Need to force these variables to a single value in the other cases
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded.Not(),rbShaded.Not()])
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded,rbShaded.Not()])
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf([ltShaded.Not(),rbShaded.Not()])
			cI = CombinationIterator(self.boardWidth-2,2*len(value))
			comb = cI.getNext()
			varTrack = 0
			while comb is not None:
				shade = True			# Note: we start unshaded
				unShadeIndex = 0
				ind = [-1] + comb + [self.boardWidth-1]
				for i in range(len(ind)-1):
					for j in range(ind[i]+1,ind[i+1]+1):
						if shade is True:
							self.model.AddBoolAnd([self.cellShaded[row+j*vStep][col+j*hStep]]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded,rbShaded])
						else:
							self.model.AddBoolAnd([self.cellShaded[row+j*vStep][col+j*hStep].Not()]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded,rbShaded])
					if shade is not True:
						if value[unShadeIndex] > 0:
							self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(ind[i]+1,ind[i+1]+1)) == value[unShadeIndex]).OnlyEnforceIf(varBitmap[varTrack] + [ltShaded,rbShaded])
						unShadeIndex = unShadeIndex + 1
					shade = not shade
				varTrack = varTrack + 1
				comb = cI.getNext()
		else:
			# This case can't be realized...kill it
			self.model.AddBoolAnd([rbShaded.Not()]).OnlyEnforceIf([ltShaded,rbShaded])
					
	def printCurrentSolution(self):
		colorama.init()
		dW = max([len(str(x)) for x in self.digits])
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if self.solver.Value(self.cellShaded[i][j]) == 1: # This one is shaded
					print(Fore.BLACK + Back.WHITE + '{:d}'.format(self.solver.Value(self.cellValues[i][j])).rjust(dW) + Fore.RESET + Back.RESET,end = " ")
				else:
					print('{:d}'.format(self.solver.Value(self.cellValues[i][j])).rjust(dW),end = " ")
			print()
		print()

class doubleDoku(sudoku):
	"""A class used to implement DoubleDoku puzzles, where boxes 5/6/8/9 of puzzle 1 are boxes 1/2/4/5 of puzzle 2"""

	def __init__(self,boardSizeRoot,irregular=None,digitSet=None):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot

		if digitSet is None:
			self.digits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit

		self.model = cp_model.CpModel()
		
		self.p1 = sudoku(boardSizeRoot,irregular=irregular,digitSet=self.digits,model=self.model)
		self.p2 = sudoku(boardSizeRoot,irregular=irregular,digitSet=self.digits,model=self.model)
		
		overlap = self.boardSizeRoot
		for i in range((self.boardSizeRoot-1)*self.boardSizeRoot):
			for j in range((self.boardSizeRoot-1)*self.boardSizeRoot):
				self.model.Add(self.p1.getCellVar(overlap+i,overlap+j) == self.p2.getCellVar(i,j))
		
	def setDoubleDokuConstraint(self,puzz,constraint,args):
		# Unified interface to apply constraints to sub-puzzles
		getattr(getattr(self,'p'+str(puzz)),'set'+constraint)(args)
	
	def findSolution(self,test=False):
		self.p1.applyNegativeConstraints()
		self.p2.applyNegativeConstraints()

		self.solver = cp_model.CpSolver()
		self.solveStatus = self.solver.Solve(self.model)
				
		if test is True:
			return self.testStringSolution()
		else:
			print('Solver status = %s' % self.solver.StatusName(self.solveStatus))
			if self.solveStatus == cp_model.OPTIMAL:
				print('Solution found!')
				self.printCurrentSolution()
				
	def countSolutions(self):
		self.p1.applyNegativeConstraints()
		self.p2.applyNegativeConstraints()
		
		self.solver = cp_model.CpSolver()
		consolidatedCellValues = []
		solution_printer = SolutionPrinter([])
		self.solveStatus = self.solver.SearchForAllSolutions(self.model, solution_printer)
		
		print('Solutions found : %i' % solution_printer.SolutionCount())
		if self.solveStatus == cp_model.OPTIMAL:
			print('Sample solution')
			self.printCurrentSolution()

	def printCurrentSolution(self):
		colorama.init()
		dW = max([len(str(x)) for x in self.digits])
		overlap = self.boardSizeRoot
		# First print board 1 rows, trailing board 2 as appropriate
		for i in range(self.boardWidth):
			# p1
			for j in range(self.boardWidth):
				if i < overlap or j < overlap:
					print('{:d}'.format(self.solver.Value(self.p1.getCellVar(i,j))).rjust(dW),end = " ")
				else:
					print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p1.getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			
			# If there is p2 stuff after this
			if i >= overlap:
				for j in range((self.boardSizeRoot-1)*self.boardSizeRoot,self.boardWidth):
					print('{:d}'.format(self.solver.Value(self.p2.getCellVar(i-overlap,j))).rjust(dW),end = " ")
			print()
			
		# Remainder of p2
		for i in range((self.boardSizeRoot-1)*self.boardSizeRoot,self.boardWidth):
			print (' '*((1+dW)*overlap), end = "")
			for j in range(self.boardWidth):
				print('{:d}'.format(self.solver.Value(self.p2.getCellVar(i,j))).rjust(dW),end = " ")
			print()
			
	def testStringSolution(self):
		testString = ''
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				testString = testString + '{:d}'.format(self.solver.Value(self.p1.getCellVar(i,j)))
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				testString = testString + '{:d}'.format(self.solver.Value(self.p2.getCellVar(i,j)))
		return testString

class samuraiSudoku(sudoku):
	"""A class used to implement Samurai Sudoku puzzles."""

	def __init__(self,boardSizeRoot,irregular=None,digitSet=None):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot

		if digitSet is None:
			self.digits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit

		self.model = cp_model.CpModel()
		
		self.p1 = sudoku(boardSizeRoot,irregular=irregular,digitSet=self.digits,model=self.model)
		self.p2 = sudoku(boardSizeRoot,irregular=irregular,digitSet=self.digits,model=self.model)
		self.p3 = sudoku(boardSizeRoot,irregular=irregular,digitSet=self.digits,model=self.model)
		self.p4 = sudoku(boardSizeRoot,irregular=irregular,digitSet=self.digits,model=self.model)
		self.p5 = sudoku(boardSizeRoot,irregular=irregular,digitSet=self.digits,model=self.model)
		
		overlap = self.boardWidth-self.boardSizeRoot-1
		for i in range(self.boardSizeRoot+1):
			for j in range(self.boardSizeRoot+1):
				self.model.Add(self.p1.getCellVar(overlap+i,overlap+j) == self.p3.getCellVar(i,j))
				self.model.Add(self.p2.getCellVar(overlap+i,j) == self.p3.getCellVar(i,overlap+j))
				self.model.Add(self.p4.getCellVar(i,overlap+j) == self.p3.getCellVar(overlap+i,j))
				self.model.Add(self.p5.getCellVar(i,j) == self.p3.getCellVar(overlap+i,overlap+j))
		
	def setSamuraiConstraint(self,puzz,constraint,args):
		# Unified interface to apply Samurai constraints to sub-puzzles
		getattr(getattr(self,'p'+str(puzz)),'set'+constraint)(args)
	
	def findSolution(self):
		self.p1.applyNegativeConstraints()
		self.p2.applyNegativeConstraints()
		self.p3.applyNegativeConstraints()
		self.p4.applyNegativeConstraints()
		self.p5.applyNegativeConstraints()

		self.solver = cp_model.CpSolver()
		self.solveStatus = self.solver.Solve(self.model)
				
		print('Solver status = %s' % self.solver.StatusName(self.solveStatus))
		if self.solveStatus == cp_model.OPTIMAL:
			print('Solution found!')
			self.printCurrentSolution()
				
	def countSolutions(self):
		self.p1.applyNegativeConstraints()
		self.p2.applyNegativeConstraints()
		self.p3.applyNegativeConstraints()
		self.p4.applyNegativeConstraints()
		self.p5.applyNegativeConstraints()
		
		self.solver = cp_model.CpSolver()
		consolidatedCellValues = []
		solution_printer = SolutionPrinter([])
		self.solveStatus = self.solver.SearchForAllSolutions(self.model, solution_printer)
		
		print('Solutions found : %i' % solution_printer.SolutionCount())
		if self.solveStatus == cp_model.OPTIMAL:
			print('Sample solution')
			self.printCurrentSolution()

	def printCurrentSolution(self):
		colorama.init()
		dW = max([len(str(x)) for x in self.digits])
		overlap = self.boardWidth-self.boardSizeRoot-1
		# First print boards 1 and 2, and their overlap with board 3
		for i in range(self.boardWidth):
			# p1
			for j in range(self.boardWidth):
				if i < overlap or j < overlap:
					print('{:d}'.format(self.solver.Value(self.p1.getCellVar(i,j))).rjust(dW),end = " ")
				else:
					print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p1.getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			# Between p1 and p2
			if i < overlap:
				print(' '*((1+dW)*(self.boardWidth-2*(self.boardSizeRoot+1))),end = '')
			else:
				for j in range(self.boardSizeRoot+1,overlap):
					print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p3.getCellVar(i-overlap,j))).rjust(dW)+Fore.RESET,end = " ")

			# p2
			for j in range(self.boardWidth):
				if i < overlap or j > self.boardSizeRoot:
					print('{:d}'.format(self.solver.Value(self.p2.getCellVar(i,j))).rjust(dW),end = " ")
				else:
					print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p2.getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			print()
			
		# Now we're in the middle where we're printing just board 3
		for i in range(self.boardSizeRoot+1,overlap):
			print(' '*((1+dW)*overlap),end = '')
			for j in range(self.boardWidth):
				print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p3.getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			print()
				
		# Now the bottom two grids, p4 and p5
		for i in range(self.boardWidth):
			# p4
			for j in range(self.boardWidth):
				if i > self.boardSizeRoot or j < overlap:
					print('{:d}'.format(self.solver.Value(self.p4.getCellVar(i,j))).rjust(dW),end = " ")
				else:
					print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p4.getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			# Between p4 and p5
			if i < self.boardSizeRoot + 1:
				for j in range(self.boardSizeRoot+1,overlap):
					print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p3.getCellVar(i+overlap,j))).rjust(dW)+Fore.RESET,end = " ")
			else:
				print(' '*((1+dW)*(self.boardWidth-2*(self.boardSizeRoot+1))),end = '')
					
			# p5
			for j in range(self.boardWidth):
				if i > self.boardSizeRoot or j > self.boardSizeRoot:
					print('{:d}'.format(self.solver.Value(self.p5.getCellVar(i,j))).rjust(dW),end = " ")
				else:
					print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p5.getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			print()
		print()
		
class schroedingerCellSudoku(sudoku):
	"""A class used to implement Schroedinger cell puzzles. These puzzles add an additional digit, usually 0, and one cell in each row, column and region is denoted a Schroedinger cell. Each Schroedinger cell has TWO digits, and the usual rules of every digit appearing once in each row, column and region are respected. Constraints respect Schroedinger cells in various ways."""	
	
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
		
		self.isXVInitialized = False
		self.isXVNegative = False
		
		self.isXVXVInitialized = False
		self.isXVXVNegative = False
		
		self.isEntropyQuadInitialized = False
		self.isEntropyQuadNegative = False
		
		self.isEntropyBattenburgInitialized = False
		self.isEntropyBattenburgNegative = False
		
		self.isConsecutiveQuadInitialized = False
		self.isConsecutiveQuadNegative = False
		
		self.isParityQuadInitialized = False
		self.isParityQuadNegative = False
		
		self.isParity = False
		self.isEntropy = False
		self.isModular = False
		self.isFullRank = False
		
		if digitSet is None:
			self.digits = {x for x in range(self.boardWidth+1)}		# Add additional digit from Schroedinger
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit
		self.schroedingerNotSetBase = self.maxDigit + 1				# We need to set a range of digits which are distinct for 
																	# all cells in the grid, and denote "no Schroedinger"
		self.maxSDigit = self.schroedingerNotSetBase+self.boardWidth*self.boardWidth
		self.model = cp_model.CpModel()
		self.listCandidatesVar = self.model.NewBoolVar('test')
		self.cellValues = []
		self.allVars = []
		self.candTests = [[[None for k in range(self.boardWidth)] for j in range(self.boardWidth)] for i in range(self.boardWidth)]
		self.candToExclude=[]		
		
		# Create the variables containing the cell values
		for rowIndex in range(self.boardWidth):
			tempArrayCell = []
			for colIndex in range(self.boardWidth):
				tempCell = self.model.NewIntVar(self.minDigit,self.maxDigit,'cellValue{:d}{:d}'.format(rowIndex,colIndex))
				if (self.maxDigit - self.minDigit) >= self.boardWidth:	# If base digit set is not continguous, force values
					self.model.AddAllowedAssignments([tempCell],[(x,) for x in self.digits])
					# Note: no need to force values on cellValues, because they will be tied to base
				tempArrayCell.append(tempCell)
			self.cellValues.insert(rowIndex,tempArrayCell)
						
		# Now the Schroedinger stuff
		self.sCell = []
	
		for i in range(self.boardWidth):
			tempSCellArray = []
			for j in range(self.boardWidth):
				c = self.model.NewBoolVar('sCell{:d}{:d}'.format(i,j))
				tempSCellArray.append(c)
			self.sCell.insert(i,tempSCellArray)
		
		# Next, create integer versions of sCell variables to check conditions
		self.sCellInt = []
  
		for i in range(self.boardWidth):
			tempSCellArray = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(0,1,'sCellInt{:d}{:d}'.format(i,j))
				tempSCellArray.append(c)
			self.sCellInt.insert(i,tempSCellArray)

		# Next, create variables to hold the alternate values for sCells.
		# Note: the values are allowed to get so large so that we can determine with an arithmetic condition 
		# whether or not an sCell is actually set, which will be useful in some circumstances.
		self.sCellValues = []
  
		for i in range(self.boardWidth):
			tempSCellArray = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(self.minDigit,self.maxSDigit,'sCellValues{:d}{:d}'.format(i,j))
				tempSCellArray.append(c)
			self.sCellValues.insert(i,tempSCellArray)

		# Finally, create variables to hold a different version of the values which are useful for summing constraints
		self.sCellSums = []
  
		for i in range(self.boardWidth):
			tempSCellArray = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(self.minDigit,self.maxDigit,'sCellSums{:d}{:d}'.format(i,j))
				tempSCellArray.append(c)
			self.sCellSums.insert(i,tempSCellArray)
		
		# Schroedinger conditions	
		# First we tie the values of the Schroedinger cells to the Booleans
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				# When sCells are not set, values are above range. When sCell is set, this provides a canonical ordering between the "normal" digit and the sCell one
				self.model.Add(self.sCellValues[i][j] > self.cellValues[i][j])
				# If this is an S-cell, force the value to be in the normal range, not the "unset"
				self.model.Add(self.sCellValues[i][j] < self.schroedingerNotSetBase).OnlyEnforceIf(self.sCell[i][j])
				# If this is not an S-cell, force the value to be a unique digit in the over-digit range
				self.model.Add(self.sCellValues[i][j] == self.schroedingerNotSetBase+(i*self.boardWidth)+j).OnlyEnforceIf([self.sCell[i][j].Not()])
				
		# Similarly we tie the values for summing into the Booleans
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				self.model.Add(self.sCellSums[i][j] == self.sCellValues[i][j]).OnlyEnforceIf(self.sCell[i][j])
				self.model.Add(self.sCellSums[i][j] == 0).OnlyEnforceIf(self.sCell[i][j].Not())
			
		# Now tie sCell and sCellInt variables
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				self.model.Add(self.sCellInt[i][j] == 1).OnlyEnforceIf([self.sCell[i][j]])
				self.model.Add(self.sCellInt[i][j] == 0).OnlyEnforceIf([self.sCell[i][j].Not()])
			
		# Now we ensure there is only one sCell per row and column
		for i in range(self.boardWidth):
			self.model.Add(sum(self.sCellInt[i][j] for j in range(self.boardWidth)) == 1)
			self.model.Add(sum(self.sCellInt[j][i] for j in range(self.boardWidth)) == 1)

		# Now uniqueness on rows and columns. By setting up our variables in this manner, we have ensured that the set of
		# cellValues and sCellValues in a row/columnL
		# a.) is a set of 2*boardWidth distinct digits
		# b.) contains all of the base digits...boardWidth of the base digits are in cellValues, and the extra must be in 
		#     the S-cell.
		for i in range(self.boardWidth):
			self.model.AddAllDifferent([self.cellValues[i][j] for j in range(self.boardWidth)] + [self.sCellValues[i][j] for j in range(self.boardWidth)]) 	# Rows
			self.model.AddAllDifferent([self.cellValues[j][i] for j in range(self.boardWidth)] + [self.sCellValues[j][i] for j in range(self.boardWidth)]) 	# Columns

		# NOW deal with regions. Default to boxes. Need to get all variables set up.
		self.regions = []
		if irregular is None:
			self.__setBoxes()
	
	def __setBoxes(self):
		# Create rules to ensure boxes have no repeats in the BASE digits
		for rowBox in range(self.boardSizeRoot):
			for colBox in range(self.boardSizeRoot):
				tempCellArray = []
				tempCellIndexArray = []
				tempSCellIntArray = []
				tempSCellValueArray = []
				for rowIndex in range(self.boardSizeRoot):
					for colIndex in range(self.boardSizeRoot):
						tempCellArray.append(self.cellValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
						tempCellIndexArray.append((self.boardSizeRoot*rowBox+rowIndex,self.boardSizeRoot*colBox+colIndex))
						tempSCellIntArray.append(self.sCellInt[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
						tempSCellValueArray.append(self.sCellValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
				self.model.AddAllDifferent(tempCellArray+tempSCellValueArray)	# Ensures square regions have all different values
				self.regions.append(tempCellIndexArray)			# Set squares up as regions for region sum rules
				self.model.Add(sum(tempSCellIntArray) == 1)	# Ensure there is only one Schroedinger cell per square
				
	def setRegion(self,inlist):
		# Allow setting of irregular regions
		inlist = self.__procCellList(inlist)
		self.regions.append(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in inlist])
		self.model.Add(sum(self.sCellInt[x[0]][x[1]] for x in inlist) == 1)	# Ensure one S-cell per region

	def __setParity(self):
		# Set up variables to track parity constraints
		self.cellParity = []
		self.sCellParity = []
		
		maxDiff = self.maxDigit-self.minDigit
		for i in range(self.boardWidth):
			t = []
			sT = []
			for j in range(self.boardWidth):
				div = self.model.NewIntVar(0,2*maxDiff,'ParityDiv')
				sDiv = self.model.NewIntVar(0,2*self.maxSDigit,'ParityDiv')
				mod = self.model.NewIntVar(0,1,'parityValue{:d}{:d}'.format(i,j))
				sMod = self.model.NewIntVar(0,1,'parityValue{:d}{:d}'.format(i,j))
				t.append(mod)
				sT.append(sMod)
				self.model.Add(2*div <= self.cellValues[i][j])
				self.model.Add(2*div+2 > self.cellValues[i][j])
				self.model.Add(mod == self.cellValues[i][j]-2*div)
				
				self.model.Add(2*sDiv <= self.sCellValues[i][j])
				self.model.Add(2*sDiv+2 > self.sCellValues[i][j])
				self.model.Add(sMod == self.sCellValues[i][j]-2*sDiv).OnlyEnforceIf(self.sCell[i][j])
				self.model.Add(sMod == mod).OnlyEnforceIf(self.sCell[i][j].Not())	# If not an s-cell, force it to match the real digit
																					# so comparisons with non-existent s-Cells match the main
			self.cellParity.insert(i,t)
			self.sCellParity.insert(i,sT)
		
		self.isParity = True
		
	def __setEntropy(self):
		# Set up variables to track entropy and modular constraints
		self.cellEntropy = []
		self.sCellEntropy = []
		
		for i in range(self.boardWidth):
			t = []
			sT = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(self.minDigit // 3 - 1,self.maxDigit // 3,'entropyValue{:d}{:d}'.format(i,j))
				sC = self.model.NewIntVar(self.minDigit // 3 - 1,self.maxDigit // 3,'entropyValue{:d}{:d}'.format(i,j))
				t.append(c)
				sT.append(sC)
				self.model.Add(3*c+1 <= self.cellValues[i][j])
				self.model.Add(3*c+4 > self.cellValues[i][j])
				self.model.Add(3*sC+1 <= self.sCellValues[i][j])
				self.model.Add(3*sC+4 > self.sCellValues[i][j])
			self.cellEntropy.insert(i,t)
			self.sCellEntropy.insert(i,sT)
		
		self.isEntropy = True
		
	def printCurrentSolution(self):
		dW = max([2*len(str(x)) for x in self.digits]) + 1
		colorama.init()
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if self.solver.Value(self.sCellInt[i][j]) == 1: # This one is the S-Cell
					print(('{:d}'.format(self.solver.Value(self.cellValues[i][j])) + Fore.RED + ' {:d}'.format(self.solver.Value(self.sCellValues[i][j]))).rjust(dW) + Fore.RESET,end = " ")
				else:
					print('{:d}'.format(self.solver.Value(self.cellValues[i][j])).center(dW),end = " ")
			print()
		print()
		
	def testStringSolution(self):
		testString = ''
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if self.solver.Value(self.sCellInt[i][j]) == 1: # This one is doubled!
					testString = testString + '{:d}'.format(self.solver.Value(self.cellValues[i][j]))+'*{:d}*'.format(self.solver.Value(self.sCellValues[i][j]))
				else:
					testString = testString + '{:d}'.format(self.solver.Value(self.cellValues[i][j]))
		return testString
		
	def listCellCandidates(self,row,col=-1,quiet=False):
		if col == -1:
			(row,col) = self.__procCell(row)
			
		good = []
		sCell = False
		nonSCell = False
		for x in self.digits:
			ok = False
			# Not an S-Cell
			myCon1 = self.model.AddBoolAnd([self.sCell[row][col].Not()])
			myCon2 = self.model.Add(self.cellValues[row][col] == x)
			self.applyNegativeConstraints()
			solver = cp_model.CpSolver()
			solveStatus = solver.Solve(self.model)
			if solveStatus == cp_model.OPTIMAL:
				ok = True
				nonSCell = True
			myCon1.Proto().Clear()
			myCon2.Proto().Clear()
				
			# As an S-cell
			myCon1 = self.model.AddBoolAnd([self.sCell[row][col]])
			myCon2 = self.model.Add(self.cellValues[row][col] == x).OnlyEnforceIf(self.listCandidatesVar)
			myCon3 = self.model.Add(self.sCellValues[row][col] == x).OnlyEnforceIf(self.listCandidatesVar.Not())
			self.applyNegativeConstraints()
			solver = cp_model.CpSolver()
			solveStatus = solver.Solve(self.model)
			if solveStatus == cp_model.OPTIMAL:
				ok = True
				sCell = True
			myCon1.Proto().Clear()
			myCon2.Proto().Clear()
			myCon3.Proto().Clear()

			if ok is True:
				good.append('{:d}'.format(x))
			else:
				good.append(' ')
				self.candToExclude.append([str(row+1),str(col+1),str(x)])
				
		if sCell is True and nonSCell is False:
			good = list(map(lambda s: Back.BLUE + s + Back.RESET,good))
		if sCell is False and nonSCell is True:
			good = list(map(lambda s: Back.RED + s + Back.RESET,good))
			
		if quiet is False:
			print('Possible values for cell {:d},{:d}: '.format(row+1,col+1) + ''.join(list(map(str,good))))
		else:
			return good

	def sSubsets(self,inlist):
		sCandidates = [[]]
		listr = [[]]
		listc = [[]]
		listb = [[]]
		for el in inlist:
			rowInd = el[0] // self.boardSizeRoot	# Determines box row: 0,1,2 -> 0; 3,4,5 -> 1, 6,7,8 -> 2
			colInd = el[1] // self.boardSizeRoot	# Determines box col: 0,1,2 -> 0; 3,4,5 -> 1, 6,7,8 -> 2
			elb = 3*rowInd + colInd					# Determines 0-base box index
			
			for i in range(len(sCandidates)):
				if el[0] not in listr[i] and el[1] not in listc[i] and elb not in listb[i]:
					sCandidates += [sCandidates[i]+[el]]
					listr += [listr[i]+[el[0]]]
					listc += [listr[i]+[el[1]]]
					listb += [listr[i]+[elb]]
		return sCandidates
		
	def setXSudokuMain(self,allDigits=True):
		self.model.AddAllDifferent([self.cellValues[i][i] for i in range(self.boardWidth)] + [self.sCellValues[i][i] for i in range(self.boardWidth)])
		if allDigits is True:
			self.model.Add(sum([self.sCellInt[i][i] for i in range(self.boardWidth)]) == 1)
		
	def setXSudokuOff(self,allDigits=True):
		self.model.AddAllDifferent([self.cellValues[i][self.boardWidth-1-i] for i in range(self.boardWidth)] + [self.sCellValues[i][self.boardWidth-1-i] for i in range(self.boardWidth)])
		if allDigits is True:
			self.model.Add(sum([self.sCellInt[i][self.boardWidth-1-i] for i in range(self.boardWidth)]) == 1)
		
	def setAntiKing(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth-1):
				self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+1][j+1],self.sCellValues[i][j],self.sCellValues[i+1][j+1]])
			for j in range(1,self.boardWidth):
				self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+1][j-1],self.sCellValues[i][j],self.sCellValues[i+1][j-1]])

	def setAntiKnight(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth):
				if j > 1:
					self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+1][j-2],self.sCellValues[i][j],self.sCellValues[i+1][j-2]])
				if j > 0 and i < self.boardWidth-2:
					self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+2][j-1],self.sCellValues[i][j],self.sCellValues[i+2][j-1]])
				if j < self.boardWidth-1 and i < self.boardWidth-2:
					self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+2][j+1],self.sCellValues[i][j],self.sCellValues[i+2][j+1]])
				if j < self.boardWidth-2:
					self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[i+1][j+2],self.sCellValues[i][j],self.sCellValues[i+1][j+2]])

	def setDisjointGroups(self,allDigits=True):
		for i in range(self.boardSizeRoot):
			for j in range(self.boardSizeRoot):
				self.model.AddAllDifferent([self.cellValues[self.boardSizeRoot*k+i][self.boardSizeRoot*l+j] for k in range(self.boardSizeRoot) for l in range(self.boardSizeRoot)] + [self.sCellValues[self.boardSizeRoot*k+i][self.boardSizeRoot*l+j] for k in range(self.boardSizeRoot) for l in range(self.boardSizeRoot)])
				if allDigits is True:
					self.model.Add(sum([self.sCellInt[self.boardSizeRoot*k+i][self.boardSizeRoot*l+j] for k in range(self.boardSizeRoot) for l in range(self.boardSizeRoot)]) == 1)
				
	def setNonConsecutive(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth-1):
				self.model.Add(self.cellValues[i][j] - self.cellValues[i][j+1] != 1)
				self.model.Add(self.cellValues[i][j+1] - self.cellValues[i][j] != 1)
				self.model.Add(self.cellValues[i][j] - self.sCellValues[i][j+1] != 1).OnlyEnforceIf(self.sCell[i][j+1])
				self.model.Add(self.sCellValues[i][j+1] - self.cellValues[i][j] != 1).OnlyEnforceIf(self.sCell[i][j+1])
				self.model.Add(self.sCellValues[i][j] - self.cellValues[i][j+1] != 1).OnlyEnforceIf(self.sCell[i][j])
				self.model.Add(self.cellValues[i][j+1] - self.sCellValues[i][j] != 1).OnlyEnforceIf(self.sCell[i][j])
				self.model.Add(self.cellValues[j][i] - self.cellValues[j+1][i] != 1)
				self.model.Add(self.cellValues[j+1][i] - self.cellValues[j][i] != 1)
				self.model.Add(self.sCellValues[j][i] - self.cellValues[j+1][i] != 1).OnlyEnforceIf(self.sCell[j][i])
				self.model.Add(self.cellValues[j+1][i] - self.sCellValues[j][i] != 1).OnlyEnforceIf(self.sCell[j][i])
				self.model.Add(self.cellValues[j][i] - self.sCellValues[j+1][i] != 1).OnlyEnforceIf(self.sCell[j+1][i])
				self.model.Add(self.sCellValues[j+1][i] - self.cellValues[j][i] != 1).OnlyEnforceIf(self.sCell[j+1][i])
				
	def setWindoku(self,allDigits=True):
		if (self.boardWidth != 9):
			print('Cannot use Windoku on non-9x9 board.')
			sys.exit()
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(1,4) for j in range(1,4)] + [self.sCellValues[i][j] for i in range(1,4) for j in range(1,4)])
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(1,4) for j in range(5,8)] + [self.sCellValues[i][j] for i in range(1,4) for j in range(5,8)])
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(5,8) for j in range(1,4)] + [self.sCellValues[i][j] for i in range(5,8) for j in range(1,4)])
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(5,8) for j in range(5,8)] + [self.sCellValues[i][j] for i in range(5,8) for j in range(5,8)])
		if allDigits is True:
			self.model.Add(sum([self.sCellInt[i][j] for i in range(1,4) for j in range(1,4)]) == 1)
			self.model.Add(sum([self.sCellInt[i][j] for i in range(1,4) for j in range(5,8)]) == 1)
			self.model.Add(sum([self.sCellInt[i][j] for i in range(5,8) for j in range(1,4)]) == 1)
			self.model.Add(sum([self.sCellInt[i][j] for i in range(5,8) for j in range(5,8)]) == 1)

	def setUnicornDigit(self,value):
		# A unicorn digit is one such that for any instance of that digit in the grid, all of the cells a knight's move away are different
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				c = self.model.NewBoolVar('UnicornDigitD{:d}R{:d}C{:d}'.format(value,i,j))
				cs = self.model.NewBoolVar('UnicornDigitSelforSD{:d}R{:d}C{:d}'.format(value,i,j))
				self.model.Add(self.cellValues[i][j] == value).OnlyEnforceIf([c,cs])
				self.model.Add(self.sCellValues[i][j] == value).OnlyEnforceIf([c,cs.Not()])

				# Curses...lack of OnlyEnforceIf on AddAllDifferent strikes again. Gotta do it the long way
				kCells = [self.cellValues[i+k][j+m] for k in [-2,-1,1,2] for m in [-2,-1,1,2] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth] + [self.sCellValues[i+k][j+m] for k in [-2,-1,1,2] for m in [-2,-1,1,2] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth]
				for k in range(len(kCells)):
					for m in range(k+1,len(kCells)):
						self.model.Add(kCells[k] != kCells[m]).OnlyEnforceIf(c)

				self.model.Add(self.cellValues[i][j] != value).OnlyEnforceIf(c.Not())
				self.model.Add(self.sCellValues[i][j] != value).OnlyEnforceIf(c.Not())
				self.model.AddBoolAnd([cs]).OnlyEnforceIf(c.Not())
				
	def setGiven(self,spec):
		T = self._sudoku__procCell(spec)
		row = T[0]
		col = T[1]
		values = [T[i] for i in range(2,len(T))]
		if len(values) == 1:
			self.model.Add(self.cellValues[row][col] == values[0])
			self.model.AddBoolAnd([self.sCell[row][col].Not()])
		elif values[0] == values[1]:
			c = self.model.NewBoolVar('SCell')
			self.model.Add(self.cellValues[row][col] == values[0]).OnlyEnforceIf(c)
			self.model.Add(self.sCellValues[row][col] == values[0]).OnlyEnforceIf(c.Not())
		else:
			l = min(values)
			h = max(values)
			self.model.AddBoolAnd([self.sCell[row][col]])
			self.model.Add(self.cellValues[row][col] == l)
			self.model.Add(self.sCellValues[row][col] == h)
	
	def setIsSCell(self,row,col=-1):
		if col == -1:
			(row,col) = self._sudoku__procCell(row)
		self.model.AddBoolAnd([self.sCell[row][col]])
	
	def setIsSCellArray(self,list):
		for x in list: self.setIsSCell(x)
		
	def setIsNotSCell(self,row,col=-1):
		if col == -1:
			(row,col) = self._sudoku__procCell(row)
		self.model.AddBoolAnd([self.sCell[row][col].Not()])
		
	def setIsNotSCellArray(self,list):
		for x in list: self.setIsNotSCell(x)

	def setEvenOdd(self,row,col=-1,parity=-1):
		if col == -1:
			(row,col,parity) = self.__procCell(row)
		if self.isParity is False:
			self.__setParity()
		self.model.Add(self.cellParity[row][col] == parity)
		self.model.Add(self.sCellParity[row][col] == parity)
		
	def setOddEven(self,row,col=-1,parity=-1):
		self.setEvenOdd(row,col,parity)

	def setMinMaxCell(self,row,col=-1,minmax=-1):
		if col == -1:
			(row,col,minmax) = self.__procCell(row)
		if row > 0:
			self.model.Add(self.cellValues[row][col] < self.cellValues[row-1][col]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row-1][col])
			self.model.Add(self.sCellValues[row][col] < self.cellValues[row-1][col]).OnlyEnforceIf(self.sCell[row][col]) if minmax == 0 else self.model.Add(self.sCellValues[row][col] > self.cellValues[row-1][col]).OnlyEnforceIf(self.sCell[row][col])
			self.model.Add(self.cellValues[row][col] < self.sCellValues[row-1][col]).OnlyEnforceIf(self.sCell[row-1][col]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.sCellValues[row-1][col]).OnlyEnforceIf(self.sCell[row-1][col])
		if row < self.boardWidth-1:
			self.model.Add(self.cellValues[row][col] < self.cellValues[row+1][col]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row+1][col])
			self.model.Add(self.sCellValues[row][col] < self.cellValues[row+1][col]).OnlyEnforceIf(self.sCell[row][col]) if minmax == 0 else self.model.Add(self.sCellValues[row][col] > self.cellValues[row+1][col]).OnlyEnforceIf(self.sCell[row][col])
			self.model.Add(self.cellValues[row][col] < self.sCellValues[row+1][col]).OnlyEnforceIf(self.sCell[row+1][col]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.sCellValues[row+1][col]).OnlyEnforceIf(self.sCell[row+1][col])
		if col > 0:
			self.model.Add(self.cellValues[row][col] < self.cellValues[row][col-1]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row][col-1])
			self.model.Add(self.sCellValues[row][col] < self.cellValues[row][col-1]).OnlyEnforceIf(self.sCell[row][col]) if minmax == 0 else self.model.Add(self.sCellValues[row][col] > self.cellValues[row][col-1]).OnlyEnforceIf(self.sCell[row][col])
			self.model.Add(self.cellValues[row][col] < self.sCellValues[row][col-1]).OnlyEnforceIf(self.sCell[row][col-1]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.sCellValues[row][col-1]).OnlyEnforceIf(self.sCell[row][col-1])
		if col < self.boardWidth-1:
			self.model.Add(self.cellValues[row][col] < self.cellValues[row][col+1]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row][col+1])
			self.model.Add(self.sCellValues[row][col] < self.cellValues[row][col+1]).OnlyEnforceIf(self.sCell[row][col]) if minmax == 0 else self.model.Add(self.sCellValues[row][col] > self.cellValues[row][col+1]).OnlyEnforceIf(self.sCell[row][col])
			self.model.Add(self.cellValues[row][col] < self.sCellValues[row][col+1]).OnlyEnforceIf(self.sCell[row][col+1]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.sCellValues[row][col+1]).OnlyEnforceIf(self.sCell[row][col+1])
		
	def setKropkiWhite(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self._sudoku__procCell(row)
		if self.isKropkiInitialized is not True:
			self.kropkiCells = [(row,col,hv)]
			self.isKropkiInitialized = True
		else:
			self.kropkiCells.append((row,col,hv))
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		# Note: both cells cannot be Schroedinger
		bc1c2 = self.model.NewBoolVar('LargerValue')
		bc1s2 = self.model.NewBoolVar('LargerValue')
		bs1c2 = self.model.NewBoolVar('LargerValue')
		
		# Regardless of whether either cell is Schroedinger, this is true
		self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == self.kropkiDiff).OnlyEnforceIf(bc1c2)
		self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == -1*self.kropkiDiff).OnlyEnforceIf(bc1c2.Not())
		
		# If cell 2 is Schroedinger
		self.model.Add(self.cellValues[row][col] - self.sCellValues[row+hv][col+(1-hv)] == self.kropkiDiff).OnlyEnforceIf([bc1s2,self.sCell[row+hv][col+(1-hv)]])
		self.model.Add(self.cellValues[row][col] - self.sCellValues[row+hv][col+(1-hv)] == -1*self.kropkiDiff).OnlyEnforceIf([bc1s2.Not(),self.sCell[row+hv][col+(1-hv)]])
		self.model.AddBoolAnd([bc1s2]).OnlyEnforceIf(self.sCell[row+hv][col+(1-hv)].Not())
		
		# If cell 1 is Schroedinger
		self.model.Add(self.sCellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == self.kropkiDiff).OnlyEnforceIf([bs1c2,self.sCell[row][col]])
		self.model.Add(self.sCellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == -1*self.kropkiDiff).OnlyEnforceIf([bs1c2.Not(),self.sCell[row][col]])
		self.model.AddBoolAnd([bs1c2]).OnlyEnforceIf(self.sCell[row][col].Not())		
		
	def setKropkiBlack(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self._sudoku__procCell(row)
		if self.isKropkiInitialized is not True:
			self.kropkiCells = [(row,col,hv)]
			self.isKropkiInitialized = True
		else:
			self.kropkiCells.append((row,col,hv))
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bc1c2 = self.model.NewBoolVar('LargerValue')
		bc1s2 = self.model.NewBoolVar('LargerValue')
		bs1c2 = self.model.NewBoolVar('LargerValue')
		
		# Regardless of whether either cell is Schroedinger, this is true
		self.model.Add(self.cellValues[row][col] == self.kropkiRatio*self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf(bc1c2)
		self.model.Add(self.kropkiRatio*self.cellValues[row][col] == self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf(bc1c2.Not())
		
		# If cell 2 is Schroedinger
		self.model.Add(self.cellValues[row][col] == self.kropkiRatio*self.sCellValues[row+hv][col+(1-hv)]).OnlyEnforceIf([bc1s2,self.sCell[row+hv][col+(1-hv)]])
		self.model.Add(self.kropkiRatio*self.cellValues[row][col] == self.sCellValues[row+hv][col+(1-hv)]).OnlyEnforceIf([bc1s2.Not(),self.sCell[row+hv][col+(1-hv)]])
		self.model.AddBoolAnd([bc1s2]).OnlyEnforceIf(self.sCell[row+hv][col+(1-hv)].Not())
		
		# If cell 1 is Schroedinger
		self.model.Add(self.sCellValues[row][col] == self.kropkiRatio*self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf([bs1c2,self.sCell[row][col]])
		self.model.Add(self.kropkiRatio*self.sCellValues[row][col] == self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf([bs1c2.Not(),self.sCell[row][col]])
		self.model.AddBoolAnd([bs1c2]).OnlyEnforceIf(self.sCell[row][col].Not())	
		
		bit = self.model.NewBoolVar('KropkiBlackBiggerDigitRow{:d}Col{:d}HV{:d}'.format(row,col,hv))
		self.model.Add(self.cellValues[row][col] == self.kropkiRatio*self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf(bit)
		self.model.Add(self.kropkiRatio*self.cellValues[row][col] == self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf(bit.Not())
		
	def setXVV(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self._sudoku__procCell(row)
		if self.isXVInitialized is not True:
			self.xvCells = [(row,col,hv)]
			self.isXVInitialized = True
		else:
			self.xvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == 5)
		
	def setXVX(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self._sudoku__procCell(row)
		if self.isXVInitialized is not True:
			self.xvCells = [(row,col,hv)]
			self.isXVInitialized = True
		else:
			self.xvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == 10)

	def setAntiXV(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] != 5)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] != 10)
	
	def setXVXVV(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self._sudoku__procCell(row)
		if self.isXVXVInitialized is not True:
			self.xvxvCells = [(row,col,hv)]
			self.isXVXVInitialized = True
		else:
			self.xvxvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bit = self.model.NewBoolVar('XVXV515Row{:d}Col{:d}'.format(row,col))
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == 5).OnlyEnforceIf(bit)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == 15).OnlyEnforceIf(bit.Not())
		
	def setXVXVX(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self._sudoku__procCell(row)
		if self.isXVXVInitialized is not True:
			self.xvxvCells = [(row,col,hv)]
			self.isXVXVInitialized = True
		else:
			self.xvxvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bit = self.model.NewBoolVar('XVXV1015Row{:d}Col{:d}'.format(row,col))
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == 10).OnlyEnforceIf(bit)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == 15).OnlyEnforceIf(bit.Not())

	def setNeighborSum(self,row,col=-1,sSum=False):
		# Cell whose value is the sum of its orthogonally adjacent neighbors
		if col == -1:
			(row,col) = self._sudoku__procCell(row)
		sCells = [self.cellValues[row+k][col+m] for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m) and row+k >= 0 and row+k < self.boardWidth and col+m >= 0 and col+m < self.boardWidth] + [self.sCellSums[row+k][col+m] for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m) and row+k >= 0 and row+k < self.boardWidth and col+m >= 0 and col+m < self.boardWidth]
		
		self.model.Add(sum(sCells) == self.cellValues[row][col]+self.sCellSums[row][col])
		
		if sSum is False:
			# In this case, since two digits can't be the same sum, we forbid there being an sCell here.
			# There's no need to change the sum condition, since this Boolean will ulltimately force sCellSums[row][col] == 0
			self.model.AddBoolAnd([self.sCell[row][col].Not()])
	
	def setNeighbourSum(self,row,col=-1,sSum=False):
		if col == -1:
			(row,col) = self._sudoku__procCell(row)
		self.setNeighborSum(row,col,sSum)
			
	def setFriendly(self,row,col=-1):
		if col == -1:
			(row,col) = self._sudoku__procCell(row)
			
		if self.isFriendlyInitialized is not True:
			self.friendlyCells = [(row,col)]
			self.isFriendlyInitialized = True
		else:
			self.friendlyCells.append((row,col))
			
		rowMatch = self.model.NewBoolVar('FriendlyRowRow{:d}Col{:d}'.format(row,col))
		colMatch = self.model.NewBoolVar('FriendlyColRow{:d}Col{:d}'.format(row,col))
		boxMatch = self.model.NewBoolVar('FriendlyBoxRow{:d}Col{:d}'.format(row,col))
		rowSMatch = self.model.NewBoolVar('FriendlySRowRow{:d}Col{:d}'.format(row,col))
		colSMatch = self.model.NewBoolVar('FriendlySColRow{:d}Col{:d}'.format(row,col))
		boxSMatch = self.model.NewBoolVar('FriendlySBoxRow{:d}Col{:d}'.format(row,col))
		
		self.model.Add(self.cellValues[row][col] == row+1).OnlyEnforceIf(rowMatch)
		self.model.Add(self.cellValues[row][col] != row+1).OnlyEnforceIf(rowMatch.Not())
		self.model.Add(self.cellValues[row][col] == col+1).OnlyEnforceIf(colMatch)
		self.model.Add(self.cellValues[row][col] != col+1).OnlyEnforceIf(colMatch.Not())
		self.model.Add(self.sCellValues[row][col] == row+1).OnlyEnforceIf([rowSMatch,self.sCell[row][col]])
		self.model.Add(self.sCellValues[row][col] != row+1).OnlyEnforceIf([rowSMatch.Not(),self.sCell[row][col]])
		self.model.Add(self.sCellValues[row][col] == col+1).OnlyEnforceIf([colSMatch,self.sCell[row][col]])
		self.model.Add(self.sCellValues[row][col] != col+1).OnlyEnforceIf([colSMatch.Not(),self.sCell[row][col]])
		
		rowInd = row // self.boardSizeRoot	# Determines box row: 0,1,2 -> 0; 3,4,5 -> 1, 6,7,8 -> 2
		colInd = col // self.boardSizeRoot	# Determines box col: 0,1,2 -> 0; 3,4,5 -> 1, 6,7,8 -> 2
		box = 3*rowInd + colInd				# Determines 0-base box index
		
		self.model.Add(self.cellValues[row][col] == box+1).OnlyEnforceIf(boxMatch)
		self.model.Add(self.cellValues[row][col] != box+1).OnlyEnforceIf(boxMatch.Not())
		self.model.Add(self.sCellValues[row][col] == box+1).OnlyEnforceIf([boxSMatch,self.sCell[row][col]])
		self.model.Add(self.sCellValues[row][col] != box+1).OnlyEnforceIf([boxSMatch.Not(),self.sCell[row][col]])
		
		self.model.AddBoolOr([rowMatch,colMatch,boxMatch])
		self.model.AddBoolOr([rowSMatch,colSMatch,boxSMatch])
		self.model.AddBoolAnd([rowSMatch,colSMatch,boxSMatch]).OnlyEnforceIf(self.sCell[row][col].Not())
		
	def setCage(self,inlist,value = None):
		inlist = self._sudoku__procCellList(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in inlist] + [self.sCellValues[x[0]][x[1]] for x in inlist])
		if value is not None:
			self.model.Add(sum([self.cellValues[x[0]][x[1]] for x in inlist] + [self.sCellSums[x[0]][x[1]] for x in inlist]) == value)
			
	def setRepeatingCage(self,inlist,value):
		inlist = self._sudoku__procCellList(inlist)
		self.model.Add(sum([self.cellValues[x[0]][x[1]] for x in inlist] + [self.sCellSums[x[0]][x[1]] for x in inlist]) == value)
		
	def setBlockCage(self,inlist,values):
		# A block cage is an area with a list of values that cannot appear in that area
		inlist = self.__procCellList(inlist)
		if isinstance(values,list):
			myValues = values
		else:
			myValues = [int(x) for x in str(values)]
		
		for i in range(len(inlist)):
			for j in range(len(myValues)):
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] != myValues[j])
				self.model.Add(self.sCellValues[inlist[i][0]][inlist[i][1]] != myValues[j])
				
	def setLittleKiller(self,row1,col1,row2,col2,value):
		# row1,col1 is the position of the first cell in the sum
		# row2,col2 is the position of the second cell in the sum
		
		# Note: leave cell specs 1-based, since the call to setRepeatingCage will 0-base them
		hStep = col2 - col1
		vStep = row2 - row1
		cells = [(row1+vStep*k,col1+hStep*k) for k in range(self.boardWidth) if row1+vStep*k-1 in range(self.boardWidth) and col1+hStep*k-1 in range(self.boardWidth)]
		self.setRepeatingCage(cells,value)
		
	def setXSum(self,row1,col1,rc,value,sSum=False):
		#row,col are the coordinates of the cell containing the length, value is the sum
		#rc: 0 -> if adding in row, 1 -> if adding in column. Needed for corner cells.
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		if value == 0:
			# The only way this can happen is if the index is 0, which has to be an allowable digit. We can't use the noral code, since we'll get a null sum
			if 0 not in self.digits:
				print('Cannot have an X-Sum 0 without a 0 digit. INFEASIBLE')
				sys.exit()
			else:
				self.model.Add(self.cellValues[row][col] == 0)
		else:
			allowableDigits = [x for x in self.digits if x >= 1 and x <=self.boardWidth]
			varBitmap = self._sudoku__varBitmap('XSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits))
			
			for i in range(len(allowableDigits)):
				self.model.Add(self.cellValues[row][col]+self.sCellSums[row][col] == allowableDigits[i]).OnlyEnforceIf(varBitmap[i])
				self.model.Add(sum([self.cellValues[row+j*vStep][col+j*hStep] for j in range(allowableDigits[i])] + [self.sCellSums[row+j*vStep][col+j*hStep] for j in range(allowableDigits[i])]) == value).OnlyEnforceIf(varBitmap[i])
			
			if sSum is False:
				self.model.AddBoolAnd([self.sCell[row][col].Not()])
			
	def setNumberedRoom(self,row1,col1,rc,value):
		# row,col are the coordinates of the cell containing the index of the target cell
		# rc is whether things are row/column
		# value is the target value to place
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)	
		
		self.model.AddBoolAnd([self.sCell[row][col].Not()])
		allowableDigits = [x for x in self.digits if x >= 1 and x <=self.boardWidth]
		varBitmap = self._sudoku__varBitmap('NumRoomPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits))
		
		for i in range(len(allowableDigits)):
			self.model.Add(self.cellValues[row][col] == allowableDigits[i]).OnlyEnforceIf(varBitmap[i])
			bit = self.model.NewBoolVar('cs')
			self.model.Add(self.cellValues[row+(allowableDigits[i]-1)*vStep][col+(allowableDigits[i]-1)*hStep] == value).OnlyEnforceIf(varBitmap[i]+[bit])
			self.model.Add(self.sCellValues[row+(allowableDigits[i]-1)*vStep][col+(allowableDigits[i]-1)*hStep] == value).OnlyEnforceIf(varBitmap[i]+[bit.Not()])
			self.model.AddBoolAnd([bit]).OnlyEnforceIf(self.sCell[row+(allowableDigits[i]-1)*vStep][col+(allowableDigits[i]-1)*hStep].Not())
			
	def setRenbanLine(self,inlist):
		inlist = self._sudoku__procCellList(inlist)
		# First the easy part: ensure all of the digits are different. The unassigned S-Cells will not get in the way, and we want to ensure the assigned ones are different from the regular cell values. So this is safe regardless of which are the S-cells
		self.model.AddAllDifferent([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))] + [self.sCellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))])
		
		# Now the consecutive condition. To do this, we need to know exactly which are the S-cells
		sCandidates = self.sSubsets(inlist)
		varBitmap = self._sudoku__varBitmap('RenbanLine',len(sCandidates))
		for i in range(len(sCandidates)):
			# First set up S-cell Booleans to match the candidate list
			self.model.AddBoolAnd([self.sCell[x[0]][x[1]] for x in sCandidates[i]]).OnlyEnforceIf(varBitmap[i])
			self.model.AddBoolAnd([self.sCell[x[0]][x[1]].Not() for x in inlist if x not in sCandidates[i]]).OnlyEnforceIf(varBitmap[i])
			
			# Now prepare the list of variables which need to be consecutive
			varList = [self.cellValues[x[0]][x[1]] for x in inlist] + [self.sCellValues[x[0]][x[1]] for x in sCandidates[i]]
			for x in varList:
				for y in varList:
					self.model.Add(x-y < len(varList)).OnlyEnforceIf(varBitmap[i])
					
	def setArrow(self,inlist,sSum=False):
		inlist = self._sudoku__procCellList(inlist)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] + self.sCellSums[inlist[0][0]][inlist[0][1]] == sum([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))] + [self.sCellSums[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))]))
		if sSum is False:
			self.model.AddBoolAnd([self.sCell[inlist[0][0]][inlist[0][1]].Not()])
			
	def setDoubleArrow(self,inlist,sSum=False):
		inlist = self._sudoku__procCellList(inlist)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] + self.sCellSums[inlist[0][0]][inlist[0][1]] + self.cellValues[inlist[-1][0]][inlist[-1][1]] + self.sCellSums[inlist[-1][0]][inlist[-1][1]] == sum([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist)-1)] + [self.sCellSums[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist)-1)]))
		if sSum is False:
			self.model.AddBoolAnd([self.sCell[inlist[0][0]][inlist[0][1]].Not()])
			self.model.AddBoolAnd([self.sCell[inlist[-1][0]][inlist[-1][1]].Not()])
			
	def setThermo(self,inlist):
		inlist = self._sudoku__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.sCellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(self.sCell[inlist[j+1][0]][inlist[j+1][1]])
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(self.sCell[inlist[j][0]][inlist[j][1]])
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] < self.sCellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf([self.sCell[inlist[j][0]][inlist[j][1]],self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
			
	def setSlowThermo(self,inlist):
		inlist = self._sudoku__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] <= self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] <= self.sCellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(self.sCell[inlist[j+1][0]][inlist[j+1][1]])
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] <= self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(self.sCell[inlist[j][0]][inlist[j][1]])
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] <= self.sCellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf([self.sCell[inlist[j][0]][inlist[j][1]],self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
			
	def setBetweenLine(self,inlist):
		inlist = self._sudoku__procCellList(inlist)
		c = self.model.NewBoolVar('BetweenRow{:d}Col{:d}ToRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1],inlist[-1][0],inlist[-1][1]))
		
		# Case c true: first element of line is largest. In the S-cell case, the Schroedinger value is always larger than the normal value, so if the constraint is met with respect to the cell value, it will also be met with respect to the S-value. So as long as the cell value is greater than the other end (and its potential S-cell, which we need to control for), we're OK.
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.sCellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf([c,self.sCell[inlist[-1][0]][inlist[-1][1]]])
		
		for j in range(1,len(inlist)-1):
			self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.sCellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf([c,self.sCell[inlist[j][0]][inlist[j][1]]])
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.sCellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf([c,self.sCell[inlist[-1][0]][inlist[-1][1]]])
			# Since S-cell is bigger, other inequality is satisfied by default
			
		# Case c false: last element of line is largest. In this case, we'll just do all four potential comparisons
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] < self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c.Not())
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] < self.sCellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf([c.Not(),self.sCell[inlist[-1][0]][inlist[-1][1]]])
		self.model.Add(self.sCellValues[inlist[0][0]][inlist[0][1]] < self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf([c.Not(),self.sCell[inlist[0][0]][inlist[0][1]]])
		self.model.Add(self.sCellValues[inlist[0][0]][inlist[0][1]] < self.sCellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf([c.Not(),self.sCell[inlist[0][0]][inlist[0][1]],self.sCell[inlist[-1][0]][inlist[-1][1]]])
		
		for j in range(1,len(inlist)-1):
			self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] < self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c.Not())
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c.Not())
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf([c.Not(),self.sCell[inlist[j][0]][inlist[j][1]]])
			self.model.Add(self.sCellValues[inlist[0][0]][inlist[0][1]] < self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf([c.Not(),self.sCell[inlist[0][0]][inlist[0][1]]])
			
	def setVault(self,inlist):
		# Digits in a vault cannot appear in any cell outside the vault but orthogonally adjacent ot a cell in it.
		inlist = self._sudoku__procCellList(inlist)
		adjCells = set()
		for i in range(len(inlist)):
			adjCells = adjCells.union({(inlist[i][0],inlist[i][1]-1),(inlist[i][0],inlist[i][1]+1),(inlist[i][0]+1,inlist[i][1]),(inlist[i][0]-1,inlist[i][1])})
		adjCells = adjCells & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth) if (i,j) not in inlist}

		for x in inlist:
			for y in adjCells:
				self.model.Add(self.cellValues[x[0]][x[1]] != self.cellValues[y[0]][y[1]])
				self.model.Add(self.cellValues[x[0]][x[1]] != self.sCellValues[y[0]][y[1]])
				self.model.Add(self.sCellValues[x[0]][x[1]] != self.cellValues[y[0]][y[1]])
				self.model.Add(self.sCellValues[x[0]][x[1]] != self.sCellValues[y[0]][y[1]])
				
	def setParityLine(self,inlist):
		if self.isParity is False:
			self.__setParity()
		inlist = self._sudoku__procCellList(inlist)
		for j in range(len(inlist)):
			self.model.Add(self.cellParity[inlist[j][0]][inlist[j][1]] == self.sCellParity[inlist[j][0]][inlist[j][1]])
		
		for j in range(len(inlist)-1):
			self.model.Add(self.cellParity[inlist[j][0]][inlist[j][1]] != self.cellParity[inlist[j+1][0]][inlist[j+1][1]])

	def setRegionSumLine(self,inlist):
		inlist = self._sudoku__procCellList(inlist)
		sumSets = []
		for region in self.regions:
			tempSum = [self.cellValues[x[0]][x[1]] + self.sCellSums[x[0]][x[1]] for x in set(region) & set(inlist)]
			if len(tempSum) != 0: sumSets.append(tempSum)

		baseSum = sum(sumSets[0])
		for i in range(1,len(sumSets)):
			self.model.Add(sum(sumSets[i]) == baseSum)
			
	def setRegionSegmentSumLine(self,inlist):
		# This is used for variants where the sums for each segment of the line have the same sum
		# in each region. If a line enters a region twice, each segment must have the same sum as all
		# other segments...the visits do not aggregate
		inlist = self._sudoku__procCellList(inlist)
		sumSets = []
		currentRegionStart = 0
		for i in range(len(self.regions)):
			if len({inlist[0]} & set(self.regions[i])) > 0: currentRegion = i
		for j in range(1,len(inlist)):
			for i in range(len(self.regions)):
				if len({inlist[j]} & set(self.regions[i])) > 0: thisRegion = i
			if thisRegion != currentRegion:
				sumSets.append([self.cellValues[x[0]][x[1]] + self.sCellSums[x[0]][x[1]] for x in inlist[currentRegionStart:j]])
				currentRegionStart = j
				currentRegion = thisRegion
		# Need to do it again since the last segment is left in the queue.	
		sumSets.append([self.cellValues[x[0]][x[1]] + self.sCellSums[x[0]][x[1]] for x in inlist[currentRegionStart:]])

		baseSum = sum(sumSets[0])
		for i in range(1,len(sumSets)):
			self.model.Add(sum(sumSets[i]) == baseSum)
			
class superpositionSudoku(schroedingerCellSudoku):
	'''This class is a version of Schrödinger cell sudoku, but the constraints take a harder line on the double-digit cells to 
	   look more like classical superposition. Whenever an S-cell is used on a constraint, there must be an assignment of Schrödinger cells that makes the constraint work, for both possible values. So for example, if an S-cell is on a Renban line with 3, 4, and 5, the Schrödinger cell must be 2/6, since either assignment independently could satisfy the constraint. It could not be 1/2, for assigning it to be 1 would leave the set of digits discontiguous. Constraints that order, such as between lines or thermos, can be inherited intact, but summing constraints need to be revised.'''
	   
	def __setSuperpositionArrow(self,inlist,singleDouble):
		# Single/double determines if this is a single or double arrow
		inlist = self._sudoku__procCellList(inlist)
		# This is really effin' complicated, so I want to write down how I plan to do it.
		# Step 1: Break into cases based on where the Schroedinger cells are on the line. I thought I couldn't do this with
		#         varBitmap, but I can since I'm going to be reusing my case variables.
		# Step 2: Given a particular combination of S-cells, we need to calculate all possible sums on the line, so
		#         there are going to be 2^#S possibilities. Normally one would think to use #S variables to encode this, BUT
		#         these variables are not dependent...it is absolutely possible (and in fact required) that several of these
		#		  variables will be simultaneously true. So we go with one variable per.
		# Step 3: In each combination, for each cell/sCell pair active, we split all of the 2^#S variables into cases, whether they
		#         indicate that the cell is used in a successful sum, or the sCell is. Ultimately, we need the "or" of these variables
		#         to be true, i.e., there exists some assignment of values using each of the possible values which yields a true sum
		
		sCandidates = self.sSubsets(inlist)
		varBitmap = self._sudoku__varBitmap('sDAS',len(sCandidates))
		
		# Now for the set of vars we need to case the combinations. We can reuse these across cases!
		cVars = [self.model.NewBoolVar('sDAS{:d}'.format(i)) for i in range(2**max([len(x) for x in sCandidates]))]
			
		# Let's build some arrays for easy indexing...we aren't creating anything here, just organizing to make our loops go cleaner
		summand = [[self.cellValues[inlist[j][0]][inlist[j][1]],self.sCellValues[inlist[j][0]][inlist[j][1]]] for j in range(len(inlist))]
		fS = [1] + [-1 for i in range(1,len(inlist)-1)]			# This is a multiplication factor for each summand to distinguish
																# the ends from the middle. Instead of casing on whether end cells
																# are Schroedinger or not, just multiply everyting by its factor and sum to 0.
		if singleDouble == 1:
			fS.append(-1)										# This gives a single arrow...first is sum of the rest
		else:
			fS.append(1)										# Double arrow case
			
		for i in range(len(sCandidates)):
			# First set up S-cell Booleans to match the candidate list
			self.model.AddBoolAnd([self.sCell[x[0]][x[1]] for x in sCandidates[i]]).OnlyEnforceIf(varBitmap[i])
			self.model.AddBoolAnd([self.sCell[x[0]][x[1]].Not() for x in inlist if x not in sCandidates[i]]).OnlyEnforceIf(varBitmap[i])
			
			# Before we forget, peg the variables we don't need
			self.model.AddBoolAnd([cVars[j] for j in range(2**len(sCandidates[i]),len(cVars))]).OnlyEnforceIf(varBitmap[i])
			
			# Create a structure to store the sum equation variables associated with use of each cell/sCell value
			cellBools = [[[],[]] for j in range(len(sCandidates[i]))]

			# Non-Schroedinger sum - this is going to be the same over all of the Schroedinger possibilities, so just do it once
			nSS = sum([fS[j]*self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist)) if inlist[j] not in sCandidates[i]])

			# Set up sub-summand and fS lists which are indexed to the sCandidates[i] list
			myS = [summand[inlist.index(sCandidates[i][j])] for j in range(len(sCandidates[i]))]
			myF = [fS[inlist.index(sCandidates[i][j])] for j in range(len(sCandidates[i]))]

			# Alright, now the possible sums
			for j in range(2**len(sCandidates[i])):
				ind = list(map(int,list(format(j,'0'+str(len(sCandidates[i]))+'b'))))	# Convert to a list of binary integers
				self.model.Add(nSS + sum(myF[k]*myS[k][ind[k]] for k in range(len(sCandidates[i]))) == 0).OnlyEnforceIf(varBitmap[i] + [cVars[j]])	# Here's the actual sum constraint that is enforced
				self.model.Add(nSS + sum(myF[k]*myS[k][ind[k]] for k in range(len(sCandidates[i]))) != 0).OnlyEnforceIf(varBitmap[i] + [cVars[j].Not()])
				for k in range(len(sCandidates[i])):
					cellBools[k][ind[k]].append(cVars[j])		# Append the variable to the correct variable list

			# All of the sum variables are built...now we just enforce that at least one is feasible
			for j in range(len(sCandidates[i])):
				for k in range(2):
					self.model.AddBoolOr(cellBools[j][k]).OnlyEnforceIf(varBitmap[i])
			if len(sCandidates[i]) == 0:	# Need special case, since previous loop will be null
					self.model.AddBoolAnd([cVars[0]]).OnlyEnforceIf(varBitmap[i])
					
	def setArrow(self,inlist):
		self.__setSuperpositionArrow(inlist,1)
		
	def setDoubleArrow(self,inlist):
		self.__setSuperpositionArrow(inlist,2)
		
	def setRenbanLine(self,inlist):
		inlist = self._sudoku__procCellList(inlist)
		# First the easy part: ensure all of the digits are different. The unassigned S-Cells will not get in the way, and we want to ensure the assigned ones are different from the regular cell values. So this is safe regardless of which are the S-cells
		self.model.AddAllDifferent([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))] + [self.sCellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))])
		
		# Now the consecutive condition. To do this, we need to know exactly which are the S-cells
		sCandidates = self.sSubsets(inlist)
		varBitmap = self._sudoku__varBitmap('RenbanLine',len(sCandidates))
		cVars = [self.model.NewBoolVar('Renban{:d}'.format(i)) for i in range(2**max([len(x) for x in sCandidates]))]
		digitAlt = [[self.cellValues[inlist[j][0]][inlist[j][1]],self.sCellValues[inlist[j][0]][inlist[j][1]]] for j in range(len(inlist))]
			# Digit alternatives per cell for easy indexing
		
		for i in range(len(sCandidates)):
			# First set up S-cell Booleans to match the candidate list
			self.model.AddBoolAnd([self.sCell[x[0]][x[1]] for x in sCandidates[i]]).OnlyEnforceIf(varBitmap[i])
			self.model.AddBoolAnd([self.sCell[x[0]][x[1]].Not() for x in inlist if x not in sCandidates[i]]).OnlyEnforceIf(varBitmap[i])
			self.model.AddBoolAnd([cVars[j] for j in range(2**len(sCandidates[i]),len(cVars))]).OnlyEnforceIf(varBitmap[i])	# Peg unneeded
			
			# Create a structure to store the difference equation variables associated with use of each cell/sCell value
			cellBools = [[[],[]] for j in range(len(sCandidates[i]))]

			# Set up sub-digit lists which are indexed to the sCandidates[i] list
			myD = [digitAlt[inlist.index(sCandidates[i][j])] for j in range(len(sCandidates[i]))]
			
			# Now prepare the list of variables which need to be consecutive
			for j in range(2**len(sCandidates[i])):
				ind = list(map(int,list(format(j,'0'+str(len(sCandidates[i]))+'b'))))	# Convert to a list of binary integers
				varList = [self.cellValues[x[0]][x[1]] for x in inlist if x not in sCandidates[i]] + [myD[k][ind[k]] for k in range(len(sCandidates[i]))]
				for x in varList:
					for y in varList:
						self.model.Add(x-y < len(varList)).OnlyEnforceIf(varBitmap[i] + [cVars[j]])
				for k in range(len(sCandidates[i])):
					cellBools[k][ind[k]].append(cVars[j])
					
			for j in range(len(sCandidates[i])):
				for k in range(2):
					self.model.AddBoolOr(cellBools[j][k]).OnlyEnforceIf(varBitmap[i])
			if len(sCandidates[i]) == 0:	# Need special case, since previous loop will be null
					self.model.AddBoolAnd([cVars[0]]).OnlyEnforceIf(varBitmap[i])
					
class scarySudoku(sudoku):
	"""A class used to implement scary puzzles."""	
	
	def __init__(self,boardSizeRoot,irregular=None,digitSet=None,diff=3,noDiag=False,allDifferent=False,antiKing=False):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot
		self.diff = diff

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
		
		self.isXVInitialized = False
		self.isXVNegative = False
		
		self.isXVXVInitialized = False
		self.isXVXVNegative = False
		
		self.isEntropyQuadInitialized = False
		self.isEntropyQuadNegative = False
		
		self.isEntropyBattenburgInitialized = False
		self.isEntropyBattenburgNegative = False
		
		self.isConsecutiveQuadInitialized = False
		self.isConsecutiveQuadNegative = False
		
		self.isParityQuadInitialized = False
		self.isParityQuadNegative = False
		
		self.isParity = False
		self.isEntropy = False
		self.isModular = False
		self.isFullRank = False
		
		if digitSet is None:
			self.digits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit

		self.model = cp_model.CpModel()
		self.cellValues = [] 		# Since this array is used throughout for the constraints, we'll make this the modified
		
		# Create the variables containing the cell values
		for rowIndex in range(self.boardWidth):
			tempArrayCell = []
			for colIndex in range(self.boardWidth):
				tempCell = self.model.NewIntVar(self.minDigit,self.maxDigit,'cellBase{:d}{:d}'.format(rowIndex,colIndex))
				if (self.maxDigit - self.minDigit) >= self.boardWidth:	# If base digit set is not continguous, force values
					self.model.AddAllowedAssignments([tempCell],[(x,) for x in self.digits])
					# Note: no need to force values on cellValues, because they will be tied to base
				tempArrayCell.append(tempCell)
			self.cellValues.insert(rowIndex,tempArrayCell)
						
		# Create rules to ensure rows and columns have no repeats for the digits
		for rcIndex in range(self.boardWidth):
			self.model.AddAllDifferent([self.cellValues[rcIndex][crIndex] for crIndex in range(self.boardWidth)]) 	# Rows
			self.model.AddAllDifferent([self.cellValues[crIndex][rcIndex] for crIndex in range(self.boardWidth)]) 	# Columns

		self.regions = []
		if irregular is None:
			self._sudoku__setBoxes()
			for i in range(len(self.regions)):
				self.model.Add(sum(self.scaryInt[x[0]][x[1]] for x in self.regions[i]) == 1)

		# Create variables to track which cells are scary
		self.scary = []
		self.scaryInt = []	
		
		for i in range(self.boardWidth):
			tempScaryArray = []
			tempScaryIntArray = []
			for j in range(self.boardWidth):
				c = self.model.NewBoolVar('scary{:d}{:d}'.format(i,j))
				cI = self.model.NewIntVar(0,1,'scaryInt{:d}{:d}'.format(i,j))
				self.model.Add(cI == 1).OnlyEnforceIf(c)
				self.model.Add(cI == 0).OnlyEnforceIf(c.Not())
				tempScaryArray.append(c)
				tempScaryIntArray.append(cI)
			self.scary.insert(i,tempScaryArray)
			self.scaryInt.insert(i,tempScaryIntArray)

		# Now we ensure there is only one scary cell per row, column, and box
		for i in range(self.boardWidth):
			self.model.Add(sum(self.scaryInt[i][j] for j in range(self.boardWidth)) == 1)
			self.model.Add(sum(self.scaryInt[j][i] for j in range(self.boardWidth)) == 1)
				
		if noDiag is True:
			for j in range(self.boardWidth):
				# Top row, down left
				cells = {(k,j-k) for k in range(self.boardWidth)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)}
				self.model.Add(sum(self.scaryInt[x[0]][x[1]] for x in cells) <= 1)
				# Top row, down right
				cells = {(k,j+k) for k in range(self.boardWidth)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)}
				self.model.Add(sum(self.scaryInt[x[0]][x[1]] for x in cells) <= 1)
				# Bottom row, up left
				cells = {(self.boardWidth-1-k,j-k) for k in range(self.boardWidth)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)}
				self.model.Add(sum(self.scaryInt[x[0]][x[1]] for x in cells) <= 1)
				# Bottom row, up right
				cells = {(self.boardWidth-1-k,j+k) for k in range(self.boardWidth)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)}
				self.model.Add(sum(self.scaryInt[x[0]][x[1]] for x in cells) <= 1)
				
		if antiKing is True:
			for i in range(self.boardWidth):
				for j in range(self.boardWidth):
					cells = {(i+k,j+m) for k in {-1,1} for m in {-1,1}} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)}
					self.model.AddBoolAnd([self.scary[x[0]][x[1]].Not() for x in cells]).OnlyEnforceIf(self.scary[i][j])
				
		if allDifferent is True:
			for i in range(self.boardWidth):
				for j in range(self.boardWidth):
					for k in range(self.boardWidth):
						for l in range(self.boardWidth):
							if k>i or l>j:
								self.model.Add(self.cellValues[i][j] != self.cellValues[k][l]).OnlyEnforceIf([self.scary[i][j],self.scary[k][l]])
					
		# Now the actual scary condition
		for row in range(self.boardWidth):
			for col in range(self.boardWidth):
				nCells = {(row+i,col+j) for i in [-1,0,1] for j in [-1,0,1] if (i,j) != (0,0)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)}
				for x in nCells:
					c = self.model.NewBoolVar('ScaryCell')
					self.model.Add(self.cellValues[row][col] - self.cellValues[x[0]][x[1]] >= self.diff).OnlyEnforceIf([self.scary[row][col],c])
					self.model.Add(self.cellValues[x[0]][x[1]] - self.cellValues[row][col] >= self.diff).OnlyEnforceIf([self.scary[row][col],c.Not()])
					self.model.AddBoolAnd([c]).OnlyEnforceIf(self.scary[row][col].Not())

	def setRegion(self,inlist):
		# Allow setting of irregular regions
		inlist = self._sudoku__procCellList(inlist)
		self.regions.append(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in self.regions[-1]])
		self.model.Add(sum(self.scaryInt[x[0]][x[1]] for x in inlist) == 1)	# Ensure one scary cell per region

	def printCurrentSolution(self):
		dW = max([len(str(x)) for x in self.digits])
		colorama.init()
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if self.solver.Value(self.scaryInt[i][j]) == 1: # This one is doubled!
					print(Fore.RED + '{:d}'.format(self.solver.Value(self.cellValues[i][j])).rjust(dW) + Fore.RESET,end = " ")
				else:
					print('{:d}'.format(self.solver.Value(self.cellValues[i][j])).rjust(dW),end = " ")
			print()
		print()