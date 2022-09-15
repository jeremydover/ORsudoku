from __future__ import print_function
import sys
import math
import colorama
from ortools.sat.python import cp_model
from array import *
from colorama import Fore,Back

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
	"""Print intermediate solutions."""
	def __init__(self, variables):
		cp_model.CpSolverSolutionCallback.__init__(self)
		self.__variables = variables
		self.__solution_count = 0
		self.__printAll = False

	def setPrintAll(self):
		self.__printAll = True
		
	def OnSolutionCallback(self):
		self.__solution_count += 1
		cntr = 0
				
		if self.__printAll is True:
			for v in self.__variables:
				print('%i' % (self.Value(v)), end = ' ')
				cntr += 1
				if cntr == 9:
					print ()
					cntr = 0
			print()

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
	Left = 0	# Constant to determine direction arrow on 2x2 points
	Right = 1	# Constant to determine direction arrow on 2x2 points
	
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
		
		self.isParity = False
		self.isEntropy = False
		self.isModular = False
		
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
			self.__setBoxes()
			
	def __setBoxes(self):
		# Create rules to ensure boxes have no repeats
		for rowBox in range(self.boardSizeRoot):
			for colBox in range(self.boardSizeRoot):
				tempCellArray = []
				for rowIndex in range(self.boardSizeRoot):
					for colIndex in range(self.boardSizeRoot):
						tempCellArray.append(self.cellValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
				self.model.AddAllDifferent(tempCellArray)					# Squares
				self.regions.append(tempCellArray)

	def setRegion(self,inlist):
		# Allow setting of irregular regions
		inlist = self.__procCellList(inlist)
		self.regions.append([self.cellValues[x[0]][x[1]] for x in inlist])
		self.model.AddAllDifferent(self.regions[-1])
		
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
				self.model.Add(c == self.cellValues[i][j] - 3*self.cellEntropy[i][j])
			self.cellModular.insert(i,t)
		
		self.isModular = True

	def getCellVar(self,i,j):
		# Returns the model variable associated with a cell valuable. Useful when tying several puzzles together, e.g. Samurai
		return self.cellValues[i][j]
				
####Global constraints

	def setXSudokuMain(self):
		self.model.AddAllDifferent([self.cellValues[i][i] for i in range(self.boardWidth)])
		
	def setXSudokuOff(self):
		self.model.AddAllDifferent([self.cellValues[i][self.boardWidth-1-i] for i in range(self.boardWidth)])
		
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
				
	def setNonConsecutive(self):
		forbiddenAssignments = [(a,a+1) for a in range(1,self.boardWidth)] + [(a,a-1) for a in range(2,self.boardWidth+1)]
		print(forbiddenAssignments)
		for i in range(self.boardWidth):
			for j in range(self.boardWidth-1):
				self.model.AddForbiddenAssignments([self.cellValues[i][j],self.cellValues[i][j+1]],forbiddenAssignments)
				self.model.AddForbiddenAssignments([self.cellValues[j][i],self.cellValues[j+1][i]],forbiddenAssignments)
				
	def setWindoku(self):
		if (self.boardWidth != 9):
			print('Cannot use Windoku on non-9x9 board.')
			sys.exit()
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(1,4) for j in range(1,4)])
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(1,4) for j in range(5,8)])
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(5,8) for j in range(1,4)])
		self.model.AddAllDifferent([self.cellValues[i][j] for i in range(5,8) for j in range(5,8)])
		
	def __setIndexCell(self,row,col,rc,pm):
		# This is the atomic call to set an index condition. Dealing with whether it's a whole row, whether or not there's a negative
		# constraint is dealt with higher level functions. This is not generally meant to be set outside the class.
		# row,col is exactly what you think
		# rc determines whether the cell is indexing its row or its column: 0 -> row, 1 -> column
		# pm determines whether this is a positive or a negative constraint on the index cell: +1 or -1 values
		
		varBitmap = self.__varBitmap('IndexRow{:d}Col{:d}'.format(row,col),self.boardWidth)
					
		if pm == 1:
			for k in range(self.boardWidth):
				self.model.Add(self.cellValues[row][col] == k+1).OnlyEnforceIf(varBitmap[k])
				if rc == sudoku.Row:
					self.model.Add(self.cellValues[row][k] == col+1).OnlyEnforceIf(varBitmap[k])
				else:
					self.model.Add(self.cellValues[k][col] == row+1).OnlyEnforceIf(varBitmap[k])
		else:
			for k in range(self.boardWidth):
				self.model.Add(self.cellValues[row][col] == k+1).OnlyEnforceIf(varBitmap[k])
				if rc == sudoku.Row:
					self.model.Add(self.cellValues[row][k] != col+1).OnlyEnforceIf(varBitmap[k])
				else:
					self.model.Add(self.cellValues[k][col] != row+1).OnlyEnforceIf(varBitmap[k])
	
	def setIndexRow(self,row1,neg=False,inlist1=[]):
		# This sets up an indexing row. Each cell indexes the *column* so don't be surprised when we call 
		# the cell method with rc=1.
		# Row is the row number
		# neg is whether or not there is a negative constraint on cells not in the index list
		# inlist is the list of cells that index vs. not index in the negative constraint scenario
		
		# Convert 1-base to 0-base
		row0 = row1 - 1
		inlist0 = [x-1 for x in inlist1]
		
		for i in range(self.boardWidth):
			if neg is True and i not in inlist0:
				self.__setIndexCell(row0,i,sudoku.Col,-1)
			else:
				self.__setIndexCell(row0,i,sudoku.Col,1)
				
	def setIndexColumn(self,col1,neg=False,inlist1=[]):
		# This sets up an indexing column. Each cell indexes the *row* so don't be surprised when we call 
		# the cell method with rc=0.
		# Row is the column number
		# neg is whether or not there is a negative constraint on cells not in the index list
		# inlist is the list of cells that index vs. not index in the negative constraint scenario
		
		# Convert 1-base to 0-base
		col0 = col1 - 1
		inlist0 = [x-1 for x in inlist1]
		
		for i in range(self.boardWidth):
			if neg is True and i not in inlist0:
				self.__setIndexCell(i,col0,sudoku.Row,-1)
			else:
				self.__setIndexCell(i,col0,sudoku.Row,1)

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
		self.setEntropyQuadArray([(i,j) for i in range(self.boardWidth-1) for j in range(self.boardWidth-1)])

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
		
	def setMinArray(self,cells):
		for x in cells: self.setMinCell(x)
		
	def setMaxArray(self,cells):
		for x in cells: self.setMaxCell(x)
		
	def setEvenOdd(self,row,col=-1,parity=-1):
		if col == -1:
			(row,col,parity) = self.__procCell(row)
		self.model.AddModuloEquality(parity,self.cellValues[row][col],2)
		
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
		
	def setNeighborSum(self,row,col=-1):
		# Cell whose value is the sum of its orthogonally adjacent neighbors
		if col == -1:
			(row,col) = self.__procCell(row)
		sCells = [self.cellValues[row+k][col+m] for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m) and row+k >= 0 and row+k < self.boardWidth and col+m >= 0 and col+m < self.boardWidth]
		self.model.Add(sum(sCells) == self.cellValues[row][col])
	setNeighbourSum	= setNeighborSum
	
	def setNeighborSumArray(self,cells):
		for x in cells: self.setNeighborSum(x)
	setNeighbourSumArray = setNeighborSumArray
	
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
		
	def setFriendlyNegative(self):
		if self.isFriendlyInitialized is not True:
			self.friendlyCells = []
			self.isFriendlyInitialized = True
		self.isFriendlyNegative = True
		
	def __applyFriendlyNegative(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if (i,j) not in self.friendlyCells:
					self.model.Add(self.cellValues[i][j] != i+1)
					self.model.Add(self.cellValues[i][j] != j+1)
					rowInd = i // self.boardSizeRoot
					colInd = j // self.boardSizeRoot
					box = 3*rowInd + colInd
					self.model.Add(self.cellValues[i][j] != box+1)

	def setPencilmarks(self,row1,col1=-1,values=-1):
		# A block cage is an area with a list of values that cannot appear in that area
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
		
	def __applyKropkiNegative(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if i < 8 and (i,j,1) not in self.kropkiCells:
					self.model.Add(self.cellValues[i][j] - self.cellValues[i+1][j] != self.kropkiDiff)
					self.model.Add(self.cellValues[i][j] - self.cellValues[i+1][j] != -1*self.kropkiDiff)
					self.model.Add(self.cellValues[i][j] != self.kropkiRatio*self.cellValues[i+1][j])
					self.model.Add(self.kropkiRatio*self.cellValues[i][j] != self.cellValues[i+1][j])
				if j < 8 and (i,j,0) not in self.kropkiCells:
					self.model.Add(self.cellValues[i][j] - self.cellValues[i][j+1] != self.kropkiDiff)
					self.model.Add(self.cellValues[i][j] - self.cellValues[i][j+1] != -1*self.kropkiDiff)
					self.model.Add(self.cellValues[i][j] != self.kropkiRatio*self.cellValues[i][j+1])
					self.model.Add(self.kropkiRatio*self.cellValues[i][j] != self.cellValues[i][j+1])
	
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
				
	def setXVNegative(self):
		if self.isXVInitialized is not True:
			self.xvCells = []
			self.isXVInitialized = True
		self.isXVNegative = True
		
	def __applyXVNegative(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if i < 8 and (i,j,1) not in self.xvCells:
					self.model.Add(self.cellValues[i][j] + self.cellValues[i+1][j] != 5)
					self.model.Add(self.cellValues[i][j] + self.cellValues[i+1][j] != 10)
				if j < 8 and (i,j,0) not in self.xvCells:
					self.model.Add(self.cellValues[i][j] + self.cellValues[i][j+1] != 5)
					self.model.Add(self.cellValues[i][j] + self.cellValues[i][j+1] != 10)
					
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

	def setXVXVNegative(self):
		if self.isXVXVInitialized is not True:
			self.xvxvCells = []
			self.isXVXVInitialized = True
		self.isXVXVNegative = True
		
	def __applyXVXVNegative(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if i < 8 and (i,j,1) not in self.xvxvCells:
					self.model.Add(self.cellValues[i][j] + self.cellValues[i+1][j] != 5)
					self.model.Add(self.cellValues[i][j] + self.cellValues[i+1][j] != 10)
					self.model.Add(self.cellValues[i][j] + self.cellValues[i+1][j] != 15)
				if j < 8 and (i,j,0) not in self.xvxvCells:
					self.model.Add(self.cellValues[i][j] + self.cellValues[i][j+1] != 5)
					self.model.Add(self.cellValues[i][j] + self.cellValues[i][j+1] != 10)
					self.model.Add(self.cellValues[i][j] + self.cellValues[i][j+1] != 15)

	def setCloneRegion(self,inlist):
		inlist = list(map(self.__procCellList,inlist))
		for j in range(1,len(inlist)):
			for k in range(len(inlist[0])):
				self.model.Add(self.cellValues[inlist[0][k][0]][inlist[0][k][1]] == self.cellValues[inlist[j][k][0]][inlist[j][k][1]])
				
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

####Externally-clued constraints
	def setLittleKiller(self,row1,col1,row2,col2,value):
		# row1,col1 is the position of the first cell in the sum
		# row2,col2 is the position of the second cell in the sum
		
		# Note: leave cell specs 1-based, since the call to setRepeatingCage will 0-base them
		hStep = col2 - col1
		vStep = row2 - row1
		cells = [(row1+vStep*k,col1+hStep*k) for k in range(self.boardWidth) if row1+vStep*k-1 in range(self.boardWidth) and col1+hStep*k-1 in range(self.boardWidth)]
		self.setRepeatingCage(cells,value)
		
	def setXSum(self,row1,col1,rc,value):
		#row,col are the coordinates of the cell containing the length, value is the sum
		#rc: 0 -> if adding in row, 1 -> if adding in column. Needed for corner cells.
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		allowableDigits = [x for x in self.digits if x >= 1 and x <=self.boardWidth]
		varBitmap = self.__varBitmap('XSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits))
		
		for i in range(len(allowableDigits)):
			self.model.Add(self.cellValues[row][col] == allowableDigits[i]).OnlyEnforceIf(varBitmap[i])
			self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(allowableDigits[i])) == value).OnlyEnforceIf(varBitmap[i])
				
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
							
	def setNumberedRoom(self,row1,col1,rc,value):
		# row,col are the coordinates of the cell containing the index of the target cell
		# rc is whether things are row/column
		# value is the target value to place
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)	
		
		allowableDigits = [x for x in self.digits if x >= 1 and x <=self.boardWidth]
		varBitmap = self.__varBitmap('NumRoomPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits))
		
		for i in range(len(allowableDigits)):
			self.model.Add(self.cellValues[row][col] == allowableDigits[i]).OnlyEnforceIf(varBitmap[i])
			self.model.Add(self.cellValues[row+(allowableDigits[i]-1)*vStep][col+(allowableDigits[i]-1)*hStep] == value).OnlyEnforceIf(varBitmap[i])
			
	def setSandwichSum(self,row1,col1,rc,value):
		# row,col are the coordinates of the cell containing the index of the target cell
		# rc is whether things are row/column
		# value is the sum of values between the lowest and higest digits (usually 1 and 9)
		
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
				self.model.Add(firstCell - secondCell == self.maxDigit - self.minDigit).OnlyEnforceIf(varBitmap[j] + [lgr,adj])
				self.model.Add(secondCell - firstCell == self.maxDigit - self.minDigit).OnlyEnforceIf(varBitmap[j] + [lgr.Not(),adj])
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
				self.model.Add(firstCell - secondCell == self.maxDigit - self.minDigit).OnlyEnforceIf(varBitmap[varTrack] + [lgr,adj.Not()])
				self.model.Add(secondCell - firstCell == self.maxDigit - self.minDigit).OnlyEnforceIf(varBitmap[varTrack] + [lgr.Not(),adj.Not()])
				self.model.Add(sum(self.cellValues[row+m*vStep][col+m*hStep] for m in range(j+1,k)) == value).OnlyEnforceIf(varBitmap[varTrack] + [adj.Not()])
				varTrack = varTrack + 1
					
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
		
		# List of cell variables in the row/column we're looking at
		candCells = {self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.boardWidth)}
		for i in range(len(self.regions)):
			if len({self.cellValues[row][col]} & set(self.regions[i])) > 0: currentRegion = i
			
		clueCells = list(candCells & set(self.regions[currentRegion]))
		vars = [[self.model.NewBoolVar('OutsideClue') for i in range(len(clueCells))] for j in range(len(valueList))]
		for j in range(len(valueList)):
			for i in range(len(clueCells)):
				self.model.Add(clueCells[i] == valueList[j]).OnlyEnforceIf(vars[j][i])
				self.model.Add(clueCells[i] != valueList[j]).OnlyEnforceIf(vars[j][i].Not())
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
					((ce == self.Edge) and (i % (self.boardSizeRoot-1) == 0 and j % (self.boardSizeRoot-1) == 0)):	# Moddle, edge, and corner square
						for k in valueList: self.model.Add(self.cellValues[ulRow+i][ulCol+j] != k)
						
	def setRossini(self,row1,col1,rc,udlr):
		# row,col is the cell next to the clue
		# rc is whether things are row/column
		# udlr determines whether the arrow points up/down or left/right
		# value is optional. By default the increase condition holds in the first region, but if value is set it will hold
		# only for a fixed number of cells.
		
		# Convert from 1-base to 0-base
		row = row1 - 1
		col = col1 - 1
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)

		if self.isRossiniInitialized is not True:
			self.rossiniCells = [(row,col,rc)]
			self.isRossiniInitialized = True
		else:
			self.rossiniCells.append((row,col,rc))
			
		if self.rossiniLength == -1:	# We are using the default region-based cluing
			for i in range(len(self.regions)):
				if len({self.cellValues[row][col]} & set(self.regions[i])) > 0: region = i
			clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.boardWidth) if len({self.cellValues[row+i*vStep][col+i*hStep]} & set(self.regions[region])) > 0]
		else:
			clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.rossiniLength)]
			
		# So this is weird in external cluing, that the arrows are absolute with respect to the grid. So a left arrow on a row, regardless
		# of which side it is on, indicates the values increase from right to left. In this case, arrows on right or bottom are in the
		# "wrong" order, since they proceed from the edge into the grid (which is usually what you want.) So we reverse the array in these cases.
		
		if (rc == self.Row and col != 0) or (rc == self.Col and row != 0):
			clueCells.reverse()
			
		if udlr == self.Top:		# Same value as self.Left
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
								if len({self.cellValues[row][col]} & set(self.regions[m])) > 0: region = m
							clueCells = [self.cellValues[row+m*vStep][col+m*hStep] for m in range(self.boardWidth) if len({self.cellValues[row+m*vStep][col+m*hStep]} & set(self.regions[region])) > 0]
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
		
	def __applyEntropyQuadNegative(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth-1):
				if (i,j) not in self.entropyQuadCells:
					self.model.AddAllowedAssignments([self.cellEntropy[i][j],self.cellEntropy[i][j+1],self.cellEntropy[i+1][j],self.cellEntropy[i+1][j+1]],[(0,0,0,0),(1,1,1,1),(2,2,2,2),(0,0,0,1),(0,0,1,0),(0,1,0,0),(1,0,0,0),(0,0,0,2),(0,0,2,0),(0,2,0,0),(2,0,0,0),(1,1,1,0),(1,1,0,1),(1,0,1,1),(0,1,1,1),(1,1,1,2),(1,1,2,1),(1,2,1,1),(2,1,1,1),(2,2,2,0),(2,2,0,2),(2,0,2,2),(0,2,2,2),(2,2,2,1),(2,2,1,2),(2,1,2,2),(1,2,2,2),(0,0,1,1),(0,0,2,2),(1,1,0,0),(1,1,2,2),(2,2,0,0),(2,2,1,1),(0,1,0,1),(0,2,0,2),(1,0,1,0),(1,2,1,2),(2,0,2,0),(2,1,2,1),(0,1,1,0),(0,2,2,0),(1,0,0,1),(1,2,2,1),(2,0,0,2),(2,1,1,2)])
					
	def setEntropyBattenburg(self,row,col=-1):
		if col == -1:
			(row,col) = self.__procCell(row)
		# A 2x2 square of cells is entropic if it includes a low, middle, and high digit
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
					bit1 = self.model.NewBoolVar('EntrBattNegRow{:d}Col{:d}V1'.format(i,j))
					bit2 = self.model.NewBoolVar('EntrBattNegRow{:d}Col{:d}V2'.format(i,j))
					bit3 = self.model.NewBoolVar('EntrBattNegRow{:d}Col{:d}V3'.format(i,j))
					bit4 = self.model.NewBoolVar('EntrBattNegRow{:d}Col{:d}V4'.format(i,j))
					self.model.Add(self.cellEntropy[i][j] == self.cellEntropy[i][j+1]).OnlyEnforceIf(bit1)
					self.model.Add(self.cellEntropy[i][j] != self.cellEntropy[i][j+1]).OnlyEnforceIf(bit1.Not())
					self.model.Add(self.cellEntropy[i][j+1] == self.cellEntropy[i+1][j+1]).OnlyEnforceIf(bit2)
					self.model.Add(self.cellEntropy[i][j+1] != self.cellEntropy[i+1][j+1]).OnlyEnforceIf(bit2.Not())
					self.model.Add(self.cellEntropy[i+1][j+1] == self.cellEntropy[i+1][j]).OnlyEnforceIf(bit3)
					self.model.Add(self.cellEntropy[i+1][j+1] != self.cellEntropy[i+1][j]).OnlyEnforceIf(bit3.Not())
					self.model.Add(self.cellEntropy[i+1][j] == self.cellEntropy[i][j]).OnlyEnforceIf(bit4)
					self.model.Add(self.cellEntropy[i+1][j] != self.cellEntropy[i][j]).OnlyEnforceIf(bit4.Not())
					self.model.AddBoolOr([bit1,bit2,bit3,bit4])
					
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
		
####Linear constraints
	def setArrow(self,inlist):
		inlist = self.__procCellList(inlist)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))))
		
	def setDoubleArrow(self,inlist):
		inlist = self.__procCellList(inlist)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] + self.cellValues[inlist[-1][0]][inlist[-1][1]]== sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist)-1)))

	def setPointingArrow(self,inlist):
		inlist = self.__procCellList(inlist)
		# Pointing arrow is an arrow, but it also pointsm extending in last direction, to its total sum
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
		
	def setThermo(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			
	def setSlowThermo(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] <= self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			
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
					
				
	def setGermanWhispersLine(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			bit = self.model.NewBoolVar('GermanWhisperBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= 5).OnlyEnforceIf(bit)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= -5).OnlyEnforceIf(bit.Not())
			
	def setDutchWhispersLine(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			bit = self.model.NewBoolVar('DutchWhisperBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= 4).OnlyEnforceIf(bit)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= -4).OnlyEnforceIf(bit.Not())
			
	def setChineseWhispersLine(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= 2)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= -2)
			
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
		varlist = set(map(lambda s:self.cellValues[s[0]][s[1]],inlist))
		sumSets = []
		for region in self.regions:
			tempSum = set(region) & set(varlist)
			if len(tempSum) != 0: sumSets.append(tempSum)

		baseSum = sum(x for x in sumSets[0])
		for i in range(1,len(sumSets)):
			self.model.Add(sum(x for x in sumSets[i]) == baseSum)
			
	def setRegionSegmentSumLine(self,inlist):
		# This is used for variants where the sums for each segment of the line have the same sum
		# in each region. If a line enters a region twice, each segment must have the same sum as all
		# other segments...the visits do not aggregate
		inlist = self.__procCellList(inlist)
		varlist = list(map(lambda s:self.cellValues[s[0]][s[1]],inlist))
		
		sumSets = []
		currentRegionStart = 0
		for i in range(len(self.regions)):
			if len({varlist[0]} & set(self.regions[i])) > 0: currentRegion = i
		for j in range(1,len(varlist)):
			for i in range(len(self.regions)):
				if len({varlist[j]} & set(self.regions[i])) > 0: thisRegion = i
			if thisRegion != currentRegion:
				sumSets.append(varlist[currentRegionStart:j])
				currentRegionStart = j
				currentRegion = thisRegion
		# Need to do it again since the last segment is left in the queue.	
		sumSets.append(varlist[currentRegionStart:])

		baseSum = sum(x for x in sumSets[0])
		for i in range(1,len(sumSets)):
			self.model.Add(sum(x for x in sumSets[i]) == baseSum)

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

	def countSolutions(self,printAll = False):
		self.applyNegativeConstraints()
		self.solver = cp_model.CpSolver()
		consolidatedCellValues = []
		for tempArray in self.cellValues: consolidatedCellValues = consolidatedCellValues + tempArray
		solution_printer = SolutionPrinter(consolidatedCellValues)
		if printAll is True: solution_printer.setPrintAll()
		self.solveStatus = self.solver.SearchForAllSolutions(self.model, solution_printer)
		
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
		
	def __varBitmap(self,string,num):
		# Utility function to create a list of Boolean vaariable propositions that encode num possibilities exactly.
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
		
class doublerSudoku(sudoku):
	"""A class used to implement doubler puzzles. A doubler puzzle has a doubler in each row, column and region. Moreover, each digit is doubled exactly one time. The digit entered is used to determine normal Sudoku contraints, i.e., one of each digit per row, column and region. But for each other constraint, its value needs to be doubled."""	
	
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
		
		self.isParity = False
		self.isEntropy = False
		self.isModular = False
		
		if digitSet is None:
			self.digits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit

		self.model = cp_model.CpModel()
		self.cellValues = [] 		# Since this array is used throughout for the constraints, we'll make this the doubled values
		self.baseValues = []
		
		# Create the variables containing the cell values
		for rowIndex in range(self.boardWidth):
			tempArrayCell = []
			tempArrayBase = []
			for colIndex in range(self.boardWidth):
				tempBase = self.model.NewIntVar(self.minDigit,self.maxDigit,'cellValue{:d}{:d}'.format(rowIndex,colIndex))
				tempCell = self.model.NewIntVar(min(0,2*self.minDigit),max(0,2*self.maxDigit),'cellValue{:d}{:d}'.format(rowIndex,colIndex))
				if (self.maxDigit - self.minDigit) >= self.boardWidth:	# If base digit set is not continguous, force values
					self.model.AddAllowedAssignments([tempBase],[(x,) for x in digitSet])
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
		# First we tie the values of the underlying digits to their apparent values
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				self.model.Add(self.cellValues[i][j] == 2*self.baseValues[i][j]).OnlyEnforceIf([self.double[i][j]])
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
	
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				for k in range(self.boardWidth):
					for l in range(self.boardWidth):
						if k>i or l>j:
							self.model.Add(self.baseValues[i][j] != self.baseValues[k][l]).OnlyEnforceIf([self.double[i][j],self.double[k][l]]) 
			
	def __setBoxes(self):
		# Create rules to ensure boxes have no repeats in the BASE digits
		for rowBox in range(self.boardSizeRoot):
			for colBox in range(self.boardSizeRoot):
				tempBaseArray = []
				tempCellArray = []
				tempDoubleArray = []
				for rowIndex in range(self.boardSizeRoot):
					for colIndex in range(self.boardSizeRoot):
						tempBaseArray.append(self.baseValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
						tempCellArray.append(self.cellValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
						tempDoubleArray.append(self.doubleInt[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
				self.model.AddAllDifferent(tempBaseArray)	# Ensures square regions have all different values
				self.regions.append(tempCellArray)			# Set squares up as regions for region sum rules
				self.model.Add(sum(tempDoubleArray) == 1)	# Ensure there is only one doubler per square
				
	def setRegion(self,inlist):
		# Allow setting of irregular regions
		inlist = self.__procCellList(inlist)
		self.regions.append([self.baseValues[x[0]][x[1]] for x in inlist])
		self.model.AddAllDifferent(self.regions[-1])
		self.model.Add(sum(self.doubleInt[x[0]][x[1]] for x in inlist) == 1)	# Ensure one doubler per region
					
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
		
		self.isParity = False
		self.isEntropy = False
		self.isModular = False
		
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