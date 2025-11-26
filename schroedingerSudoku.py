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

class schroedingerCellSudoku(sudoku):
	"""A class used to implement Schroedinger cell puzzles. These puzzles add an additional digit, usually 0, and one cell in each row, column and region is denoted a Schroedinger cell. Each Schroedinger cell has TWO digits, and the usual rules of every digit appearing once in each row, column and region are respected. Constraints respect Schroedinger cells in various ways."""	
	
	def __init__(self,boardSizeRoot,canRepeatDigits=False,irregular=None,digitSet=None):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot

		self._constraintInitialized = []
		self._constraintNegative = []
		self._propertyInitialized = []
		
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
						
		# Add main variables to allVars
		for temp in self.cellValues:
			self.allVars = self.allVars + temp

		# Now the Schroedinger stuff
		self.sCell = []
	
		for i in range(self.boardWidth):
			tempSCellArray = []
			for j in range(self.boardWidth):
				c = self.model.NewBoolVar('sCell{:d}{:d}'.format(i,j))
				tempSCellArray.append(c)
			self.sCell.insert(i,tempSCellArray)
		
		# Add sCell variables to allVars
		for temp in self.sCell:
			self.allVars = self.allVars + temp

		# Next, create integer versions of sCell variables to check conditions
		self.sCellInt = []
  
		for i in range(self.boardWidth):
			tempSCellArray = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(0,1,'sCellInt{:d}{:d}'.format(i,j))
				tempSCellArray.append(c)
			self.sCellInt.insert(i,tempSCellArray)

		# Add sCellInt variables to allVars
		for temp in self.sCellInt:
			self.allVars = self.allVars + temp

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

		# Add s-values to all vars
		for temp in self.sCellValues:
			self.allVars = self.allVars + temp

		# Finally, create variables to hold a different version of the values which are useful for summing constraints
		self.sCellSums = []
  
		for i in range(self.boardWidth):
			tempSCellArray = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(self.minDigit,self.maxDigit,'sCellSums{:d}{:d}'.format(i,j))
				tempSCellArray.append(c)
			self.sCellSums.insert(i,tempSCellArray)
		
		# Add sCellSums variables to allVars
		for temp in self.sCellSums:
			self.allVars = self.allVars + temp

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
		inlist = self._procCellList(inlist)
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
		
		self._propertyInitialized.append('Parity')
		
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
		
		self._propertyInitialized.append('Entropy')
		
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
		
	def preparePrintVariables(self):
		consolidatedCellValues = []
		for tempArray in self.cellValues:
			consolidatedCellValues = consolidatedCellValues + tempArray
		for tempArray in self.sCellSums:
			consolidatedCellValues = consolidatedCellValues + tempArray
		return consolidatedCellValues

	def listCellCandidates(self,row,col=-1,quiet=False):
		if col == -1:
			(row,col) = self._procCell(row)
			
		good = []
		sCell = False
		nonSCell = False
		self.listCandidatesVar = self.model.NewBoolVar('test')
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

	def setSchroedingerAntiKing(self):
		# Asserts that no two S-cells can be a king's move apart, i.e. not diagonally adjacent
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				diagNeighbors = {(i-1,j-1),(i-1,j+1),(i+1,j-1),(i+1,j+1)} & {(k,m) for k in range(self.boardWidth) for m in range(self.boardWidth)}
				self.model.AddBoolAnd([self.sCell[x[0]][x[1]].Not() for x in diagNeighbors]).OnlyEnforceIf(self.sCell[i][j])

	def setSchroedingerAntiKnight(self):
		# Asserts that no two S-cells can be a knight's move apart, i.e. not diagonally adjacent
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				knNeighbors = {(i-2,j-1),(i-2,j+1),(i+2,j-1),(i+2,j+1),(i+1,j-2),(i+1,j+2),(i-1,j-2),(i-1,j+2)} & {(k,m) for k in range(self.boardWidth) for m in range(self.boardWidth)}
				self.model.AddBoolAnd([self.sCell[x[0]][x[1]].Not() for x in knNeighbors]).OnlyEnforceIf(self.sCell[i][j])

	def setAntiKnight(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				kCells = [(i+k,j+m) for k in [1,2] for m in [-2,-1,1,2] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth]
				for k in kCells:
					self.model.AddAllDifferent([self.cellValues[i][j],self.cellValues[k[0]][k[1]],self.sCellValues[i][j],self.sCellValues[k[0]][k[1]]])
					
	def setKnightMare(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				ij = self.cellValues[i][j] + self.sCellValues[i][j]
				kCells = [self.cellValues[i+k][j+m]+self.sCellValues[i+k][j+m] for k in [1,2] for m in [-2,-1,1,2] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth]
				for k in kCells:
					self.model.Add(ij + k != 5)
					self.model.Add(ij + k != 15)

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
		T = self._procCell(spec)
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
			(row,col) = self._procCell(row)
		self.model.AddBoolAnd([self.sCell[row][col]])
	
	def setIsSCellArray(self,list):
		for x in list: self.setIsSCell(x)
		
	def setIsNotSCell(self,row,col=-1):
		if col == -1:
			(row,col) = self._procCell(row)
		self.model.AddBoolAnd([self.sCell[row][col].Not()])
		
	def setIsNotSCellArray(self,list):
		for x in list: self.setIsNotSCell(x)

	def setEvenOdd(self,row,col=-1,parity=-1):
		if col == -1:
			(row,col,parity) = self._procCell(row)
		if 'Parity' not in self._propertyInitialized:
			self.__setParity()
		self.model.Add(self.cellParity[row][col] == parity)
		self.model.Add(self.sCellParity[row][col] == parity)
		
	def setOddEven(self,row,col=-1,parity=-1):
		self.setEvenOdd(row,col,parity)

	def setMinMaxCell(self,row,col=-1,minmax=-1):
		if col == -1:
			(row,col,minmax) = self._procCell(row)
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
			(row,col,hv) = self._procCell(row)
		self._initializeKropkiWhite()
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
			(row,col,hv) = self._procCell(row)
		self._initializeKropkiBlack()
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
		
	def setRomanSum(self,row,col=-1,hv=-1,value=-1):
		if col == -1:
			(row,col,hv,value) = self._procCell(row)
		self._initializeRomanSum()
		self.romanSumCells.append((row,col,hv))

		if value not in self.romanSumValues:
			self.romanSumValues.append(value)
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == value)

	def setAntiRomanSum(self,row,col=-1,hv=-1,value=-1):
		if col == -1:
			(row,col,hv,value) = self._procCell(row)
		self._initializeRomanSum()
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] != value)

	def setAntiRomanSums(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self._procCell(row)
		if 'RomanSum' not in self._constraintInitialized:
			pass
		else:
			for value in self.romanSumValues:
				self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] != value)

	def setXVXVV(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self._procCell(row)
		if 'XVXV' not in self._constraintInitialized:
			self.xvxvCells = [(row,col,hv)]
			self._constraintInitialized.append('XVXV')
		else:
			self.xvxvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bit = self.model.NewBoolVar('XVXV515Row{:d}Col{:d}'.format(row,col))
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == 5).OnlyEnforceIf(bit)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == 15).OnlyEnforceIf(bit.Not())
		
	def setXVXVX(self,row,col=-1,hv=-1):
		if col == -1:
			(row,col,hv) = self._procCell(row)
		if 'XVXV' not in self._constraintInitialized:
			self.xvxvCells = [(row,col,hv)]
			self._constraintInitialized.append('XVXV')
		else:
			self.xvxvCells.append((row,col,hv))
			
		# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
		bit = self.model.NewBoolVar('XVXV1015Row{:d}Col{:d}'.format(row,col))
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == 10).OnlyEnforceIf(bit)
		self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] + self.sCellSums[row][col] + self.sCellSums[row+hv][col+(1-hv)] == 15).OnlyEnforceIf(bit.Not())

	def setNeighborSum(self,row,col=-1,sSum=False):
		# Cell whose value is the sum of its orthogonally adjacent neighbors
		if col == -1:
			(row,col) = self._procCell(row)
		sCells = [self.cellValues[row+k][col+m] for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m) and row+k >= 0 and row+k < self.boardWidth and col+m >= 0 and col+m < self.boardWidth] + [self.sCellSums[row+k][col+m] for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m) and row+k >= 0 and row+k < self.boardWidth and col+m >= 0 and col+m < self.boardWidth]
		
		self.model.Add(sum(sCells) == self.cellValues[row][col]+self.sCellSums[row][col])
		
		if sSum is False:
			# In this case, since two digits can't be the same sum, we forbid there being an sCell here.
			# There's no need to change the sum condition, since this Boolean will ulltimately force sCellSums[row][col] == 0
			self.model.AddBoolAnd([self.sCell[row][col].Not()])
	
	def setNeighbourSum(self,row,col=-1,sSum=False):
		if col == -1:
			(row,col) = self._procCell(row)
		self.setNeighborSum(row,col,sSum)
			
	def setFriendly(self,row,col=-1):
		if col == -1:
			(row,col) = self._procCell(row)
			
		if 'Friendly' not in self._constraintInitialized:
			self.friendlyCells = [(row,col,hv)]
			self._constraintInitialized.append('Friendly')
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
		inlist = self._procCellList(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in inlist] + [self.sCellValues[x[0]][x[1]] for x in inlist])
		if value is not None:
			self.model.Add(sum([self.cellValues[x[0]][x[1]] for x in inlist] + [self.sCellSums[x[0]][x[1]] for x in inlist]) == value)
			
	def setRepeatingCage(self,inlist,value):
		inlist = self._procCellList(inlist)
		self.model.Add(sum([self.cellValues[x[0]][x[1]] for x in inlist] + [self.sCellSums[x[0]][x[1]] for x in inlist]) == value)
		
	def setAmbiguousCage(self,inlist,values,repeating=False):
		inlist = self._procCellList(inlist)
		if not repeating:
			self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in inlist] + [self.sCellValues[x[0]][x[1]] for x in inlist])
		varBitmap = self._varBitmap('AmbiguousCageRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1]),len(values))
		for i in range(len(values)):
			self.model.Add(sum([self.cellValues[x[0]][x[1]] for x in inlist] + [self.sCellSums[x[0]][x[1]] for x in inlist]) == values[i]).OnlyEnforceIf(varBitmap[i])

	def setBlockCage(self,inlist,values):
		# A block cage is an area with a list of values that cannot appear in that area
		inlist = self._procCellList(inlist)
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
			varBitmap = self._varBitmap('XSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits))
			
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
		varBitmap = self._varBitmap('NumRoomPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits))
		
		for i in range(len(allowableDigits)):
			self.model.Add(self.cellValues[row][col] == allowableDigits[i]).OnlyEnforceIf(varBitmap[i])
			bit = self.model.NewBoolVar('cs')
			self.model.Add(self.cellValues[row+(allowableDigits[i]-1)*vStep][col+(allowableDigits[i]-1)*hStep] == value).OnlyEnforceIf(varBitmap[i]+[bit])
			self.model.Add(self.sCellValues[row+(allowableDigits[i]-1)*vStep][col+(allowableDigits[i]-1)*hStep] == value).OnlyEnforceIf(varBitmap[i]+[bit.Not()])
			self.model.AddBoolAnd([bit]).OnlyEnforceIf(self.sCell[row+(allowableDigits[i]-1)*vStep][col+(allowableDigits[i]-1)*hStep].Not())
			
	def setRenbanLine(self,inlist):
		inlist = self._procCellList(inlist)
		# First the easy part: ensure all of the digits are different. The unassigned S-Cells will not get in the way, and we want to ensure the assigned ones are different from the regular cell values. So this is safe regardless of which are the S-cells
		self.model.AddAllDifferent([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))] + [self.sCellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))])
		
		# Old way was dumb. We don't need to know where the S-cells are, just how *many* there are
		numSCells = self.model.NewIntVar(0,len(inlist),'renbanNumSCells')
		self.model.Add(numSCells == sum(self.sCellInt[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))))
		
		for i in range(len(inlist)):
			for j in range(len(inlist)):
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]]-self.cellValues[inlist[j][0]][inlist[j][1]] < len(inlist) + numSCells)
				self.model.Add(self.sCellValues[inlist[i][0]][inlist[i][1]]-self.cellValues[inlist[j][0]][inlist[j][1]] < len(inlist) + numSCells).OnlyEnforceIf(self.sCell[inlist[i][0]][inlist[i][1]])
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]]-self.sCellValues[inlist[j][0]][inlist[j][1]] < len(inlist) + numSCells).OnlyEnforceIf(self.sCell[inlist[j][0]][inlist[j][1]])
				self.model.Add(self.sCellValues[inlist[i][0]][inlist[i][1]]-self.sCellValues[inlist[j][0]][inlist[j][1]] < len(inlist) + numSCells).OnlyEnforceIf([self.sCell[inlist[i][0]][inlist[i][1]],self.sCell[inlist[j][0]][inlist[j][1]]])
						
	def setArrow(self,inlist,sSum=False):
		inlist = self._procCellList(inlist)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] + self.sCellSums[inlist[0][0]][inlist[0][1]] == sum([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))] + [self.sCellSums[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))]))
		if sSum is False:
			self.model.AddBoolAnd([self.sCell[inlist[0][0]][inlist[0][1]].Not()])
			
	def setDoubleArrow(self,inlist,sSum=False):
		inlist = self._procCellList(inlist)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] + self.sCellSums[inlist[0][0]][inlist[0][1]] + self.cellValues[inlist[-1][0]][inlist[-1][1]] + self.sCellSums[inlist[-1][0]][inlist[-1][1]] == sum([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist)-1)] + [self.sCellSums[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist)-1)]))
		if sSum is False:
			self.model.AddBoolAnd([self.sCell[inlist[0][0]][inlist[0][1]].Not()])
			self.model.AddBoolAnd([self.sCell[inlist[-1][0]][inlist[-1][1]].Not()])
			
	def setThermo(self,inlist):
		inlist = self._procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.sCellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(self.sCell[inlist[j+1][0]][inlist[j+1][1]])
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(self.sCell[inlist[j][0]][inlist[j][1]])
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] < self.sCellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf([self.sCell[inlist[j][0]][inlist[j][1]],self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
			
	def setSlowThermo(self,inlist):
		inlist = self._procCellList(inlist)
		for j in range(len(inlist)-1):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] <= self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] <= self.sCellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(self.sCell[inlist[j+1][0]][inlist[j+1][1]])
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] <= self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(self.sCell[inlist[j][0]][inlist[j][1]])
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] <= self.sCellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf([self.sCell[inlist[j][0]][inlist[j][1]],self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
			
	def setBetweenLine(self,inlist):
		inlist = self._procCellList(inlist)
		
		# First note that if an endpoint of a between line is an S-cell, then the other endpoint (one or both values) must be strictly greater or strictly less than both values in the original endpoint. Otherwise, the between cannot be valid for both values of the original endpoint. So as with normal between lines, we create a Boolean variable c to distinguish between the cases where the first endpoint has the greater values, or the second endpoind does.
		
		c = self.model.NewBoolVar('BetweenRow{:d}Col{:d}ToRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1],inlist[-1][0],inlist[-1][1]))
		self.allVars.append(c)
		
		# Now tie the endpoint values to ensure c True = first element largest, c False = last element largest. There are actually two cases for each, depending on whether the endpoints are S-cells.
		
		# Case 1: First endpoint is largest. Since the S-cell value is always bigger than the base value, we don't care whether or not the first cell is an S-cell...as long as the base value of the first endpoint is larger than both the S-value and base value of the last, we'll be in this case. If the last endpoint is an S-cell, we have to be bigger than the S-value. Otherwise, we just need to be bigger than the base value.
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf([c,self.sCell[inlist[-1][0]][inlist[-1][1]].Not()])
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.sCellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf([c,self.sCell[inlist[-1][0]][inlist[-1][1]]])
		
		# Case 2: Last endpoint is largest. Basically everything is symmetric, but now we care that the first endpoint is an sCell of not
		self.model.Add(self.cellValues[inlist[-1][0]][inlist[-1][1]] > self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf([c.Not(),self.sCell[inlist[0][0]][inlist[0][1]].Not()])
		self.model.Add(self.cellValues[inlist[-1][0]][inlist[-1][1]] > self.sCellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf([c.Not(),self.sCell[inlist[0][0]][inlist[0][1]]])
		
		# Now, to check the between condition, we need to be:
		# 1. less than the smaller of the bigger cell, which is always the base value
		# 2. bigger than the larger of the smallest cell, which is the S-value if it exists, otherwise the base
		# We'll just create variables to determine these, and that way our per-cell comparisons are easy
		minEndpoint = self.model.NewIntVar(self.minDigit,self.maxDigit,'minEndpointBetweenRow{:d}Col{:d}ToRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1],inlist[-1][0],inlist[-1][1]))
		maxEndpoint = self.model.NewIntVar(self.minDigit,self.maxDigit,'maxEndpointBetweenRow{:d}Col{:d}ToRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1],inlist[-1][0],inlist[-1][1]))
		
		self.model.Add(maxEndpoint == self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf(c)
		self.model.Add(maxEndpoint == self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c.Not())
		
		self.model.Add(minEndpoint == self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf([c,self.sCell[inlist[-1][0]][inlist[-1][1]].Not()])
		self.model.Add(minEndpoint == self.sCellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf([c,self.sCell[inlist[-1][0]][inlist[-1][1]]])
		self.model.Add(minEndpoint == self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf([c.Not(),self.sCell[inlist[0][0]][inlist[0][1]].Not()])
		self.model.Add(minEndpoint == self.sCellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf([c.Not(),self.sCell[inlist[0][0]][inlist[0][1]]])
		
		# Now the per cell comparisons are easy
		for j in range(1,len(inlist)-1):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < maxEndpoint)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > minEndpoint)
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] < maxEndpoint).OnlyEnforceIf(self.sCell[inlist[j][0]][inlist[j][1]])
			self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] > minEndpoint).OnlyEnforceIf(self.sCell[inlist[j][0]][inlist[j][1]])
			
	def setVault(self,inlist):
		# Digits in a vault cannot appear in any cell outside the vault but orthogonally adjacent ot a cell in it.
		inlist = self._procCellList(inlist)
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
		if 'Parity' not in self._propertyInitialized:
			self.__setParity()
		inlist = self._procCellList(inlist)
		for j in range(len(inlist)):
			self.model.Add(self.cellParity[inlist[j][0]][inlist[j][1]] == self.sCellParity[inlist[j][0]][inlist[j][1]])
		
		for j in range(len(inlist)-1):
			self.model.Add(self.cellParity[inlist[j][0]][inlist[j][1]] != self.cellParity[inlist[j+1][0]][inlist[j+1][1]])

	def setRegionSumLine(self,inlist):
		inlist = self._procCellList(inlist)
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
		inlist = self._procCellList(inlist)
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
			
	def setMinWhispersLine(self,inlist,value,sSum=False):
		# Sets a whispers line where the minimum difference between two adjacent cells on the line is value. For an S-cell, the comparison must be valid for both digits
		inlist = self._procCellList(inlist)
		for j in range(len(inlist)-1):
			if sSum is False:
				bit1 = self.model.NewBoolVar('MaxWhisperBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= value).OnlyEnforceIf(bit1)
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= -1*value).OnlyEnforceIf(bit1.Not())
				
				bit2 = self.model.NewBoolVar('MaxWhisperSCellFirstOnlyBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
				self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= value).OnlyEnforceIf([bit2,self.sCell[inlist[j][0]][inlist[j][1]]])
				self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= -1*value).OnlyEnforceIf([bit2.Not(),self.sCell[inlist[j][0]][inlist[j][1]]])
				self.model.AddBoolAnd(bit2).OnlyEnforceIf(self.sCell[inlist[j][0]][inlist[j][1]].Not())
				
				bit3 = self.model.NewBoolVar('MaxWhisperSCellSecondOnlyBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.sCellValues[inlist[j+1][0]][inlist[j+1][1]] >= value).OnlyEnforceIf([bit3,self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.sCellValues[inlist[j+1][0]][inlist[j+1][1]] <= -1*value).OnlyEnforceIf([bit3.Not(),self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
				self.model.AddBoolAnd(bit3).OnlyEnforceIf(self.sCell[inlist[j+1][0]][inlist[j+1][1]].Not())
				
				bit4 = self.model.NewBoolVar('MaxWhisperSCellBothBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
				self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] - self.sCellValues[inlist[j+1][0]][inlist[j+1][1]] >= value).OnlyEnforceIf([bit4,self.sCell[inlist[j][0]][inlist[j][1]],self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
				self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] - self.sCellValues[inlist[j+1][0]][inlist[j+1][1]] <= -1*value).OnlyEnforceIf([bit4.Not(),self.sCell[inlist[j][0]][inlist[j][1]],self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
				self.model.AddBoolAnd(bit4).OnlyEnforceIf(self.sCell[inlist[j][0]][inlist[j][1]].Not())
				self.model.AddBoolAnd(bit4).OnlyEnforceIf(self.sCell[inlist[j+1][0]][inlist[j+1][1]].Not())
			else:
				bit1 = self.model.NewBoolVar('MaxWhisperBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + self.sCellSums[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] - self.sCellSums[inlist[j+1][0]][inlist[j+1][1]] >= value).OnlyEnforceIf(bit1)
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + self.sCellSums[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] - self.sCellSums[inlist[j+1][0]][inlist[j+1][1]] <= -1*value).OnlyEnforceIf(bit1.Not())
				
	def setMaxWhispersLine(self,inlist,value,sSum=False):
		# Sets a whispers line where the maximum difference between two adjacent cells on the line is value For an S-cell, the comparison is made with both values
		inlist = self._procCellList(inlist)
		for j in range(len(inlist)-1):
			if sSum is False:
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= value)
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= -1*value)
				self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= value).OnlyEnforceIf([self.sCell[inlist[j][0]][inlist[j][1]]])
				self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= -1*value).OnlyEnforceIf([self.sCell[inlist[j][0]][inlist[j][1]]])
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.sCellValues[inlist[j+1][0]][inlist[j+1][1]] <= value).OnlyEnforceIf([self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.sCellValues[inlist[j+1][0]][inlist[j+1][1]] >= -1*value).OnlyEnforceIf([self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
				self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] - self.sCellValues[inlist[j+1][0]][inlist[j+1][1]] <= value).OnlyEnforceIf([self.sCell[inlist[j][0]][inlist[j][1]],self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
				self.model.Add(self.sCellValues[inlist[j][0]][inlist[j][1]] - self.sCellValues[inlist[j+1][0]][inlist[j+1][1]] >= -1*value).OnlyEnforceIf([self.sCell[inlist[j][0]][inlist[j][1]],self.sCell[inlist[j+1][0]][inlist[j+1][1]]])
			else:
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + self.sCellSums[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] - self.sCellSums[inlist[j+1][0]][inlist[j+1][1]] <= value)
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + self.sCellSums[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] - self.sCellSums[inlist[j+1][0]][inlist[j+1][1]] >= -1*value)
				
	def setCountingCircles(self,inlist):
		inlist = self._procCellList(inlist)
		for d in self.digits:
			if d > 0:
				circleDigit = []
				for x in inlist:
					dx = self.model.NewBoolVar('countingCircle')
					dxInt = self.model.NewIntVar(0,1,'countingCircle')
					circleDigit.append(dxInt)
					self.model.Add(dxInt == 1).OnlyEnforceIf(dx)
					self.model.Add(dxInt == 0).OnlyEnforceIf(dx.Not())
					
					dxSwitch = self.model.NewBoolVar('countingCircleSCell')
					self.model.Add(self.cellValues[x[0]][x[1]] == d).OnlyEnforceIf([dx,dxSwitch])
					self.model.Add(self.sCellValues[x[0]][x[1]] == d).OnlyEnforceIf([dx,dxSwitch.Not()])
					self.model.Add(self.cellValues[x[0]][x[1]] != d).OnlyEnforceIf(dx.Not())
					self.model.Add(self.sCellValues[x[0]][x[1]] != d).OnlyEnforceIf(dx.Not())
					self.model.AddBoolAnd(dxSwitch).OnlyEnforceIf(dx.Not())
				
				dAppears = self.model.NewBoolVar('countingCircleValueAppears')
				self.model.Add(sum(circleDigit) == d).OnlyEnforceIf(dAppears)
				self.model.Add(sum(circleDigit) == 0).OnlyEnforceIf(dAppears.Not())
			else:
				for x in inlist:
					self.model.Add(self.cellValues[x[0]][x[1]] != d)
					self.model.Add(self.sCellValues[x[0]][x[1]] != d)
					
class superpositionSudoku(schroedingerCellSudoku):
	'''This class is a version of Schrödinger cell sudoku, but the constraints take a harder line on the double-digit cells to 
	   look more like classical superposition. Whenever an S-cell is used on a constraint, there must be an assignment of Schrödinger cells that makes the constraint work, for both possible values. So for example, if an S-cell is on a Renban line with 3, 4, and 5, the Schrödinger cell must be 2/6, since either assignment independently could satisfy the constraint. It could not be 1/2, for assigning it to be 1 would leave the set of digits discontiguous. Constraints that order, such as between lines or thermos, can be inherited intact, but summing constraints need to be revised.'''
	   
	def __setSuperpositionArrow(self,inlist,singleDouble):
		# Single/double determines if this is a single or double arrow
		inlist = self._procCellList(inlist)
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
		varBitmap = self._varBitmap('sDAS',len(sCandidates))
		
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
		
	def setKnightMare(self):
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				ij = [self.cellValues[i][j],self.sCellValues[i][j]]
				self.model.Add(ij[0] + ij[1] != 5)
				self.model.Add(ij[0] + ij[1] != 15)
				kCells = [self.cellValues[i+k][j+m] for k in [1,2] for m in [-2,-1,1,2] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth] + [self.sCellValues[i+k][j+m] for k in [1,2] for m in [-2,-1,1,2] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth]
				for m in ij:
					for k in kCells:
						self.model.Add(m + k != 5)
						self.model.Add(m + k != 15)

	def setRenbanLine(self,inlist):
		inlist = self._procCellList(inlist)
		# First the easy part: ensure all of the digits are different. The unassigned S-Cells will not get in the way, and we want to ensure the assigned ones are different from the regular cell values. So this is safe regardless of which are the S-cells
		self.model.AddAllDifferent([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))] + [self.sCellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))])
		
		# Now the consecutive condition. To do this, we need to know exactly which are the S-cells
		sCandidates = self.sSubsets(inlist)
		varBitmap = self._varBitmap('RenbanLine',len(sCandidates))
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