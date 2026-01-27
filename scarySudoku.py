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

class scarySudoku(sudoku):
	"""A class used to implement scary puzzles."""	
	
	def __init__(self,boardSizeRoot,irregular=None,digitSet=None,diff=3,noDiag=False,allDifferent=False,antiKing=False):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot
		self.diff = diff

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

		# Define regions
		self.regions = []
		if irregular is None:
			self._sudoku__setBoxes()
			for i in range(len(self.regions)):
				self.model.Add(sum(self.scaryInt[x[0]][x[1]] for x in self.regions[i]) == 1)
				
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
		inlist = self._procCellList(inlist)
		self.regions.append(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in self.regions[-1]])
		self.model.Add(sum(self.scaryInt[x[0]][x[1]] for x in inlist) == 1)	# Ensure one scary cell per region

	def printCurrentSolution(self,value_source=None):
		if value_source is None:
			value_source = self.solver
		dW = max([len(str(x)) for x in self.digits])
		colorama.init()
		for i in range(self.boardWidth):
			for j in range(self.boardWidth):
				if value_source.Value(self.scaryInt[i][j]) == 1: # This one is doubled!
					print(Fore.RED + '{:d}'.format(value_source.Value(self.cellValues[i][j])).rjust(dW) + Fore.RESET,end = " ")
				else:
					print('{:d}'.format(value_source.Value(self.cellValues[i][j])).rjust(dW),end = " ")
			print()
		print()