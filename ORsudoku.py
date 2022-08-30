from __future__ import print_function
import sys
import math
from ortools.sat.python import cp_model
from array import *


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
	"""Print intermediate solutions."""
	def __init__(self, variables):
		cp_model.CpSolverSolutionCallback.__init__(self)
		self.__variables = variables
		self.__solution_count = 0

	def OnSolutionCallback(self):
		self.__solution_count += 1
		cntr = 0
		printAll = True
		
		if printAll is True:
			for v in self.__variables:
				print('%i' % (self.Value(v)), end = ' ')
				cntr += 1
				if cntr == 9:
					print ()
					cntr = 0

	def SolutionCount(self):
		return self.__solution_count

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
		
		white/black - same as XV, but for Kropkis
		
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
	
	def __init__(self,boardSizeRoot,irregular=None):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot

		self.isBattenburgInitialized = False
		self.isBattenburgNegative = False
		
		self.isKropkiInitialized = False
		self.isKropkiNegative = False
		
		self.isXVInitialized = False
		self.isXVNegative = False
		
		self.isXVXVInitialized = False
		self.isXVXVNegative = False
		
		self.isEntropyQuadInitialized = False
		self.isEntropyQuadNegative = False
		
		self.isEntropyBattenburgInitialized = False
		self.isEntropyBattenburgNegative = False
		
		self.isEntropy = False
		self.isModular = False

		self.model = cp_model.CpModel()
		self.cellValues = []
		
		# Create the variables containing the cell values
		for rowIndex in range(self.boardWidth):
			tempArray = []
			for colIndex in range(self.boardWidth):
				tempCell = self.model.NewIntVar(1,self.boardWidth,'cellValue{:d}{:d}'.format(rowIndex,colIndex))
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
		else:
			sys.exit()
			
	def __setBoxes(self):
		# Create rules to ensure boxes have no repeats
		for rowBox in range(self.boardSizeRoot):
			for colBox in range(self.boardSizeRoot):
				tempCellArray = []
				tempIndexArray = []
				for rowIndex in range(self.boardSizeRoot):
					for colIndex in range(self.boardSizeRoot):
						tempCellArray.append(self.cellValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
						tempIndexArray.append((self.boardSizeRoot*rowBox+rowIndex,self.boardSizeRoot*colBox+colIndex))
				self.model.AddAllDifferent(tempCellArray)					# Squares
				self.regions.append(tempIndexArray)

	def __setEntropy(self):
		# Set up variables to track entropy and modular constraints
		self.cellEntropy = []
		
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(0,self.boardSizeRoot-1,'entropyValue{:d}{:d}'.format(i,j))
				t.append(c)
				self.model.Add(3*c+1 <= self.cellValues[i][j])
				self.model.Add(3*c+4 > self.cellValues[i][j])
			self.cellEntropy.insert(i,t)
		
		self.isEntropy = True
		
	def __setModular(self):
		# Set up variables to track modular constraints
		if self.isEntropy is False:
			self.setEntropy()
		
		self.cellModular = []
		
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(0,self.boardSizeRoot-1,'modularValue{:d}{:d}'.format(i,j))
				t.append(c)
				self.model.Add(c == self.cellValues[i][j] - self.boardSizeRoot*self.cellEntropy[i][j])
			self.cellModular.insert(i,t)
		
		self.isModular = True
		
		
		
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
		# constraint is dealt with higher level functions. This is not generally meany to be set outside the class.
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
	
	def setIndexRow(self,row,neg=False,inlist=[]):
		# This sets up an indexing row. Each cell indexes the *column* so don't be surprised when we call 
		# the cell method with rc=1.
		# Row is the row number
		# neg is whether or not there is a negative constraint on cells not in the index list
		# inlist is the list of cells that index vs. not index in the negative constraint scenario
		
		for i in range(self.boardWidth):
			if neg is True and i not in inlist:
				self.__setIndexCell(row,i,sudoku.Col,-1)
			else:
				self.__setIndexCell(row,i,sudoku.Col,1)
				
	def setIndexColumn(self,col,neg=False,inlist=[]):
		# This sets up an indexing column. Each cell indexes the *row* so don't be surprised when we call 
		# the cell method with rc=0.
		# Row is the column number
		# neg is whether or not there is a negative constraint on cells not in the index list
		# inlist is the list of cells that index vs. not index in the negative constraint scenario
		
		for i in range(self.boardWidth):
			if neg is True and i not in inlist:
				self.__setIndexCell(i,col,sudoku.Row,-1)
			else:
				self.__setIndexCell(i,col,sudoku.Row,1)

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

####Single cell constraints
	def setGiven(self,row,col=-1,value=-1):
		if col == -1:
			(row,col,value) = self.__procCell(row,3)
		self.model.Add(self.cellValues[row][col] == value)
	
	def setGivenArray(self,cells):
		for x in cells:	self.setGiven(x)

	def setMinMaxCell(self,row,col=-1,minmax=-1):
		if col == -1:
			(row,col,minmax) = self.__procCell(row,3)
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
			(row,col,parity) = self.__procCell(row,3)
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
			(row,col,hv) = self.__procCell(row,3)
		if self.isKropkiInitialized is not True:
			self.kropkiCells = [(row,col,hv)]
			self.isKropkiInitialized = True
		else:
			self.kropkiCells.append((row,col,hv))
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bit = self.model.NewBoolVar('KropkiWhiteBiggerDigitRow{:d}Col{:d}HV{:d}'.format(row,col,hv))
		self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == 1).OnlyEnforceIf(bit)
		self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == -1).OnlyEnforceIf(bit.Not())
		
	def setKropkiBlack(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row,3)
		if self.isKropkiInitialized is not True:
			self.kropkiCells = [(row,col,hv)]
			self.isKropkiInitialized = True
		else:
			self.kropkiCells.append((row,col,hv))
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bit = self.model.NewBoolVar('KropkiBlackBiggerDigitRow{:d}Col{:d}HV{:d}'.format(row,col,hv))
		self.model.Add(self.cellValues[row][col] == 2*self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf(bit)
		self.model.Add(2*self.cellValues[row][col] == self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf(bit.Not())
		
	def setKropkiWhiteArray(self,cells):
		for x in cells: self.setKropkiWhite(x)
		
	def setKropkiBlackArray(self,cells):
		for x in cells: self.setKropkiBlack(x)
		
	def setKropkiArray(self,cells):
		cellList = self.__procCellList(cells,4)
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
					self.model.Add(self.cellValues[i][j] - self.cellValues[i+1][j] != 1)
					self.model.Add(self.cellValues[i][j] - self.cellValues[i+1][j] != -1)
					self.model.Add(self.cellValues[i][j] != 2*self.cellValues[i+1][j])
					self.model.Add(2*self.cellValues[i][j] != self.cellValues[i+1][j])
				if j < 8 and (i,j,0) not in self.kropkiCells:
					self.model.Add(self.cellValues[i][j] - self.cellValues[i][j+1] != 1)
					self.model.Add(self.cellValues[i][j] - self.cellValues[i][j+1] != -1)
					self.model.Add(self.cellValues[i][j] != 2*self.cellValues[i][j+1])
					self.model.Add(2*self.cellValues[i][j] != self.cellValues[i][j+1])
					
	def setXVV(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row,3)
		if self.isXVInitialized is not True:
			self.xvCells = [(row,col,hv)]
			self.isXVInitialized = True
		else:
			self.xvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] == 5)
		
	def setXVX(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self.__procCell(row,3)
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
		cellList = self.__procCellList(cells,4)
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
			(row,col,hv) = self.__procCell(row,3)
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
			(row,col,hv) = self.__procCell(row,3)
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
		cellList = self.__procCellList(cells,4)
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
		
	def setEntropkiWhite(self,row,col=-1,hv=-1):
		if self.isEntropy is False:
			self.__setEntropy()
		if col == -1:
			(row,col,hv) = self.__procCell(row,3)
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellEntropy[row][col] != self.cellEntropy[row+hv][col+(1-hv)])
		
	def setEntropkiBlack(self,row,col=-1,hv=-1):
		if self.isEntropy is False:
			self.__setEntropy()
		if col == -1:
			(row,col,hv) = self.__procCell(row,3)
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellEntropy[row][col] == self.cellEntropy[row+hv][col+(1-hv)])

	def setEntropkiWhiteArray(self,cells):
		for x in cells: self.setEntropkiWhite(x)
		
	def setEntropkiBlackArray(self,cells):
		for x in cells: self.setEntropkiBlack(x)
		
	def setEntropkiArray(self,cells):
		cellList = self.__procCellList(cells,4)
		for x in cellList:
			if x[3] == sudoku.White:
				self.setEntropkiWhite(x[0],x[1],x[2])
			else:
				self.setEntropkiBlack(x[0],x[1],x[2])
		
####Externally-clued constraints
	def setLittleKiller(self,row1,col1,row2,col2,value):
		# row1,col1 is the position of the first cell in the sum
		# row2,col2 is the position of the second cell in the sum
		
		hStep = col2 - col1
		vStep = row2 - row1
		cells = [(row1+vStep*k,col1+hStep*k) for k in range(self.boardWidth) if row1+vStep*k in range(self.boardWidth) and col1+hStep*k in range(self.boardWidth)]
		self.setRepeatingCage(cells,value)
		
	def setXSum(self,row,col,rc,value):
		#row,col are the coordinates of the cell containing the length, value is the sum
		#rc: 0 -> if adding in row, 1 -> if adding in column. Needed for corner cells.
	
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		varBitmap = self.__varBitmap('XSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth-1)
		
		if value == (self.boardWidth*(self.boardWidth+1) // 2):
			self.model.Add(self.cellValues[row][col] == self.boardWidth)
		else:
			for i in range(self.boardWidth-1):
				self.model.Add(self.cellValues[row][col] == i+1).OnlyEnforceIf(varBitmap[i])
				self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(i+1)) == value).OnlyEnforceIf(varBitmap[i])
				
	def setXKropki(self,row,col,rc,wb,neg=False):
		# row,col are the coordinates of the cell containing the Kropki position, so no 9s allowed
		# rc is whether the cell is poiting to the row or column 0->row, 1->column
		# wb whether kropki is white or black, 0->white,1->black
		# neg: True if Kropki implies no other Kropkis can occur in row/col
			
		varBitmap = self.__varBitmap('XKropkiPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth-1)
		lgr = self.model.NewBoolVar('XKropkiLargerRow{:d}Col{:d}RC{:d}'.format(row,col,rc))
		
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)		
		
		for i in range(self.boardWidth-1):
			self.model.Add(self.cellValues[row][col] == i+1).OnlyEnforceIf(varBitmap[i])
			for j in range(self.boardWidth-1):
				firstCell = self.cellValues[row+j*vStep][col+j*hStep]
				secondCell = self.cellValues[row+(j+1)*vStep][col+(j+1)*hStep]				
				if j == i:
					# First case: difference 1
					if wb == sudoku.white:
						self.model.Add(firstCell - secondCell == 1).OnlyEnforceIf(varBitmap[i] + [lgr])
						self.model.Add(secondCell - firstCell == 1).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
					# Ratio 2
					else:
						self.model.Add(firstCell - 2*secondCell == 0).OnlyEnforceIf(varBitmap[i] + [lgr])
						self.model.Add(secondCell - 2*firstCell == 0).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
				else:
					# Nothing forced...unless negative constraint
					if neg is True:
						if wb == sudoku.white:
							self.model.Add(firstCell - secondCell != 1).OnlyEnforceIf(varBitmap[i] + [lgr])
							self.model.Add(secondCell - firstCell != 1).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
						else:
							self.model.Add(firstCell - 2*secondCell != 0).OnlyEnforceIf(varBitmap[i] + [lgr])
							self.model.Add(secondCell - 2*firstCell != 0).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
							
	def setNumberedRoom(self,row,col,rc,value):
		# row,col are the coordinates of the cell containing the index of the target cell
		# rc is whether things are row/column
		# value is the target value to place
		varBitmap = self.__varBitmap('NumRoomPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth-1)
		lgr = self.model.NewBoolVar('XKropkiLargerRow{:d}Col{:d}RC{:d}'.format(row,col,rc))

		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)	
		
		for i in range(self.boardWidth-1):
			self.model.Add(self.cellValues[row][col] == i+1).OnlyEnforceIf(varBitmap[i])
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == value).OnlyEnforceIf(varBitmap[i])
			
	def setSandwichSum(self,row,col,rc,value):
		# row,col are the coordinates of the cell containing the index of the target cell
		# rc is whether things are row/column
		# value is the sum of values between 1 and 9
		hStep = 0 if rc == sudoku.Col else (1 if col == 0 else -1)
		vStep = 0 if rc == sudoku.Row else (1 if row == 0 else -1)
		
		if value == 0:
			#In this case the 1 and 9 are right next to each other, which can only occur in 8 ways.
			varBitmap = self.__varBitmap('SandwichPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth-1)
			lgr = self.model.NewBoolVar('SandwichLargerRow{:d}Col{:d}RC{:d}'.format(row,col,rc))
					
			for j in range(self.boardWidth-1):
				firstCell = self.cellValues[row+j*vStep][col+j*hStep]
				secondCell = self.cellValues[row+(j+1)*vStep][col+(j+1)*hStep]
				# Note: Difference of 8 forces a 1/9 pair
				self.model.Add(firstCell - secondCell == 8).OnlyEnforceIf(varBitmap[j] + [lgr])
				self.model.Add(secondCell - firstCell == 8).OnlyEnforceIf(varBitmap[j] + [lgr.Not()])
		
		else:
			#In this case there are spaces. Combinatorics helps here...there are 9 choose 2 minus (9-1) pairs of positions
			#where they can go. Man this new varBitmap function makes this easier..save a whole page of code
			varBitmap = self.__varBitmap('SandwichPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth*(self.boardWidth-1) // 2 - (self.boardWidth-1))
			lgr = self.model.NewBoolVar('SandwichLargerRow{:d}Col{:d}RC{:d}'.format(row,col,rc))
			
			varTrack = 0
			for j in range(self.boardWidth-2):
				for k in range(j+2,self.boardWidth):
					firstCell = self.cellValues[row+j*vStep][col+j*hStep]
					secondCell = self.cellValues[row+k*vStep][col+k*hStep]
					self.model.Add(firstCell - secondCell == 8).OnlyEnforceIf(varBitmap[varTrack] + [lgr])
					self.model.Add(secondCell - firstCell == 8).OnlyEnforceIf(varBitmap[varTrack] + [lgr.Not()])
					self.model.Add(sum(self.cellValues[row+m*vStep][col+m*hStep] for m in range(j+1,k)) == value).OnlyEnforceIf(varBitmap[varTrack])
					varTrack = varTrack + 1
		
####2x2 constraints
	def setQuadruple(self,row,col=-1,values=-1):
		if col == -1:
			# In this case we do not know the length of the field because of the indeterminate number of given digits in the quad
			# We can still use procCell to make it a tuple, but we'll need to use the string form if in row 0
			T = self.__procCell(row,0)	#Note: we cannot do any zero fill because of the data structure
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
		# We calculate the differences between the top two cells, the two right cells, and the bottom two, and ensure all are odd.
		# This ensures either OE  or  EO
		#                     EO      OE
		diff1 = self.model.NewIntVar(-8,8,'BattenburgTopRow{:d}Col{:d}'.format(row,col))
		diff2 = self.model.NewIntVar(-8,8,'BattenburgRightRow{:d}Col{:d}'.format(row,col))
		diff3 = self.model.NewIntVar(-8,8,'BattenburgBottomRow{:d}Col{:d}'.format(row,col))
		self.model.Add(diff1 == self.cellValues[row][col] - self.cellValues[row][col+1])
		self.model.Add(diff2 == self.cellValues[row][col+1] - self.cellValues[row+1][col+1])
		self.model.Add(diff3 == self.cellValues[row+1][col+1] - self.cellValues[row+1][col])
		self.model.AddModuloEquality(1,diff1,2)
		self.model.AddModuloEquality(1,diff2,2)
		self.model.AddModuloEquality(1,diff3,2)
		
	def setBattenburgArray(self,cells):
		for x in cells: self.setBattenburg(x)
			
	def setBattenburgNegative(self):
		if self.isBattenburgInitialized is not True:
			self.battenburgCells = []
			self.isBattenburgInitialized = True
		self.isBattenburgNegative = True
		
	def __applyBattenburgNegative(self):
		for i in range(self.boardWidth-1):
			for j in range(self.boardWidth-1):
				if (i,j) not in self.battenburgCells:
					diff1 = self.model.NewIntVar(0,16,'BattenburgNegativeTopDifference+8Row{:d}Col{:d}'.format(i,j))
					diff2 = self.model.NewIntVar(0,16,'BattenburgNegativeRightDifference+8Row{:d}Col{:d}'.format(i,j))
					diff3 = self.model.NewIntVar(0,16,'BattenburgNegativeBottomDifference+8Row{:d}Col{:d}'.format(i,j))
					div1 = self.model.NewIntVar(0,8,'BattenburgNegativeTopDiv2Row{:d}Col{:d}'.format(i,j))
					div2 = self.model.NewIntVar(0,8,'BattenburgNegativeRightDiv2Row{:d}Col{:d}'.format(i,j))
					div3 = self.model.NewIntVar(0,8,'BattenburgNegativeBottomDiv2Row{:d}Col{:d}'.format(i,j))
					mod1 = self.model.NewIntVar(0,1,'BattenburgNegativeTopMod2Row{:d}Col{:d}'.format(i,j))
					mod2 = self.model.NewIntVar(0,1,'BattenburgNegativeRightMod2Row{:d}Col{:d}'.format(i,j))
					mod3 = self.model.NewIntVar(0,1,'BattenburgNegativeBottomMod2Row{:d}Col{:d}'.format(i,j))
					self.model.Add(diff1 == self.cellValues[i][j] - self.cellValues[i][j+1] + 8)
					self.model.Add(diff2 == self.cellValues[i][j+1] - self.cellValues[i+1][j+1] + 8)
					self.model.Add(diff3 == self.cellValues[i+1][j+1] - self.cellValues[i+1][j] + 8)
					self.model.Add(2*div1 <= diff1)
					self.model.Add(2*(div1+1) > diff1)
					self.model.Add(2*div2 <= diff2)
					self.model.Add(2*(div2+1) > diff2)
					self.model.Add(2*div3 <= diff3)
					self.model.Add(2*(div3+1) > diff3)
					self.model.Add(mod1 == diff1-2*div1)
					self.model.Add(mod2 == diff2-2*div2)
					self.model.Add(mod3 == diff3-2*div3)
					bit1 = self.model.NewBoolVar('BattenburgNegativeTopSameParityTestRow{:d}Col{:d}'.format(i,j))
					bit2 = self.model.NewBoolVar('BattenburgNegativeRightSameParityTestRow{:d}Col{:d}'.format(i,j))
					bit3 = self.model.NewBoolVar('BattenburgNegativeBottomSameParityTestRow{:d}Col{:d}'.format(i,j))
					self.model.Add(mod1 == 0).OnlyEnforceIf(bit1)
					self.model.Add(mod1 == 1).OnlyEnforceIf(bit1.Not())
					self.model.Add(mod2 == 0).OnlyEnforceIf(bit2)
					self.model.Add(mod2 == 1).OnlyEnforceIf(bit2.Not())
					self.model.Add(mod3 == 0).OnlyEnforceIf(bit3)
					self.model.Add(mod3 == 1).OnlyEnforceIf(bit3.Not())
					self.model.AddBoolOr([bit1,bit2,bit3])

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

####Linear constraints
	def setArrow(self,inlist):
		inlist = self.__procCellList(inlist)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))))
		
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
		
	def setThermo(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			
	def setKeyboardKnightLine(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.AddAllowedAssignments([self.cellValues[inlist[j][0]][inlist[j][1]],self.cellValues[inlist[j+1][0]][inlist[j+1][1]]],[(1,6),(1,8),(2,7),(2,9),(3,4),(3,8),(4,3),(4,9),(6,1),(6,7),(7,2),(7,6),(8,1),(8,3),(9,2),(9,4)])
			
	def setKeyboardKingLine(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.AddAllowedAssignments([self.cellValues[inlist[j][0]][inlist[j][1]],self.cellValues[inlist[j+1][0]][inlist[j+1][1]]],[(1,2),(1,4),(1,5),(2,1),(2,4),(2,5),(2,6),(2,3),(3,2),(3,5),(3,6),(4,1),(4,2),(4,5),(4,8),(4,7),(5,1),(5,2),(5,3),(5,4),(5,6),(5,7),(5,8),(5,9),(6,3),(6,2),(6,5),(6,8),(6,9),(7,4),(7,5),(7,8),(8,7),(8,4),(8,5),(8,6),(8,9),(9,8),(9,5),(9,6)])
			
	def setPalindromeLine(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist) // 2):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] == self.cellValues[inlist[-j-1][0]][inlist[-j-1][1]])
			
	def setWeakPalindromeLine(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist) // 2):
			self.model.AddAllowedAssignments([self.cellValues[inlist[j][0]][inlist[j][1]],self.cellValues[inlist[-j-1][0]][inlist[-j-1][1]]],[(1,1),(1,3),(3,1),(3,3),(2,2),(2,4),(4,2),(4,4),(5,5),(5,7),(5,9),(7,5),(7,7),(7,9),(6,6),(6,8),(8,6),(8,8)])
	
	def setParityLine(self,inlist):
		inlist = self.__procCellList(inlist)
		for j in range(len(inlist)-1):
			diff = self.model.NewIntVar(-8,8,'ParityLineRow{:d}Col{:d}toRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1],inlist[j+1][0],inlist[j+1][1]))
			self.model.Add(diff == self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			self.model.AddModuloEquality(1,diff,2)
			
	def setRenbanLine(self,inlist):
		inlist = self.__procCellList(inlist)
		self.model.AddAllDifferent([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))])
		for x in range(len(inlist)):
			for y in range(len(inlist)):
				self.model.Add(self.cellValues[inlist[x][0]][inlist[x][1]]-self.cellValues[inlist[y][0]][inlist[y][1]] < len(inlist))
				
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
		sumSets = []
		for r in self.regions:
			tempSum = [x for x in inlist if x in r]
			if len(tempSum) != 0: sumSets.append(tempSum)
		
		baseSum = sum(self.cellValues[x[0]][x[1]] for x in sumSets[0])
		for i in range(1,len(sumSets)):
			self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in sumSets[i]) == baseSum)
			
	def setRegionSegmentSumLine(self,inlist):
		inlist = self.__procCellList(inlist)
		# This is used for variants where the sums for each segment of the line have the same sum
		# in each region. If a line enters a region twice, each segment must have the same sum as all
		# other segments...the visits do not aggregate
		sumSets = []
		currentRegionStart = 0
		for i in range(len(self.regions)):
			if inlist[0] in self.regions[i]: currentRegion = i
		for j in range(1,len(inlist)):
			for i in range(len(self.regions)):
				if inlist[j] in self.regions[i]: thisRegion = i
			if thisRegion != currentRegion:
				sumSets.append(inlist[currentRegionStart:j])
				currentRegionStart = j
				currentRegion = thisRegion
		# Need to do it again since the last segment is left in the queue.	
		sumSets.append(inlist[currentRegionStart:])

		baseSum = sum(self.cellValues[x[0]][x[1]] for x in sumSets[0])
		for i in range(1,len(sumSets)):
			self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in sumSets[i]) == baseSum)

####Model solving
	def __applyNegativeConstraints(self):
		# This method is used to prepare the model for solution. If negative constraints have been set, i.e. all items not marked
		# cannot be marked. These constraints cannot be applied at time of assertion, since there may be new marks added after
		# the assertion. This function applies all negative constraints just prior to solving, and is called by the solver function.
		
		if self.isBattenburgNegative is True: self.__applyBattenburgNegative()
		if self.isKropkiNegative is True: self.__applyKropkiNegative()
		if self.isXVNegative is True: self.__applyXVNegative()
		if self.isXVXVNegative is True: self.__applyXVXVNegative()
		if self.isEntropyQuadNegative is True: self.__applyEntropyQuadNegative()
		if self.isEntropyBattenburgNegative is True: self.__applyEntropyBattenburgNegative()

	def findSolution(self):
		self.__applyNegativeConstraints()
		solver = cp_model.CpSolver()
		consolidatedCellValues = []
		for tempArray in self.cellValues: consolidatedCellValues = consolidatedCellValues + tempArray
		solution_printer = SolutionPrinter(consolidatedCellValues)
		self.solveStatus = solver.Solve(self.model)
		
		print()
		print('Solutions found : %i' % solution_printer.SolutionCount())
		print('Status = %s' % solver.StatusName(self.solveStatus))
		if self.solveStatus == cp_model.OPTIMAL:
			print("OPTIMAL Solution")
			for rowIndex in range(self.boardWidth):
				for colIndex in range(self.boardWidth):
					print('{:d}'.format(solver.Value(self.cellValues[rowIndex][colIndex])),end = " ")
				print()

	def countSolutions(self):
		self.__applyNegativeConstraints()
		solver = cp_model.CpSolver()
		consolidatedCellValues = []
		for tempArray in self.cellValues: consolidatedCellValues = consolidatedCellValues + tempArray
		solution_printer = SolutionPrinter(consolidatedCellValues)
		self.solveStatus = solver.SearchForAllSolutions(self.model, solution_printer)
		
		print()
		print('Solutions found : %i' % solution_printer.SolutionCount())
		print('Status = %s' % solver.StatusName(self.solveStatus))
		if self.solveStatus == cp_model.OPTIMAL:
			for rowIndex in range(self.boardWidth):
				for colIndex in range(self.boardWidth):
					print('{:d}'.format(solver.Value(self.cellValues[rowIndex][colIndex])),end = " ")
				print()

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
		
	def __procCell(self,cell,n=2):
		# Utility function that processes an individual cell into a tuple format if needed
		# Pads with leading zeros up to length n
		if type(cell) is tuple:
			return cell
		elif type(cell) is str:
			return tuple(map(int,list(cell.zfill(n))))
		elif type(cell) is int:
			return tuple(map(int,list(str(cell).zfill(n))))
			
	def __procCellList(self,inlist,n=2):
		# Utility function to process a list from one of several input formats into the tuple format
		# required by our functions
		return list(map(lambda x: self.__procCell(x,n),inlist))
