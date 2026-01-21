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
		
class soheiSudoku(sudoku):
	"""A class used to implement Sohei Sudoku puzzles."""

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
		
		overlap = self.boardWidth-self.boardSizeRoot
		for i in range(self.boardSizeRoot):
			for j in range(self.boardSizeRoot):
				self.model.Add(self.p1.getCellVar(overlap+i,j) == self.p2.getCellVar(i,overlap+j))
				self.model.Add(self.p1.getCellVar(overlap+i,overlap+j) == self.p3.getCellVar(i,j))
				self.model.Add(self.p2.getCellVar(overlap+i,overlap+j) == self.p4.getCellVar(i,j))
				self.model.Add(self.p3.getCellVar(overlap+i,j) == self.p4.getCellVar(i,overlap+j))
		
	def setSoheiConstraint(self,puzz,constraint,args):
		# Unified interface to apply Samurai constraints to sub-puzzles
		getattr(getattr(self,'p'+str(puzz)),'set'+constraint)(args)
	
	def findSolution(self):
		self.p1.applyNegativeConstraints()
		self.p2.applyNegativeConstraints()
		self.p3.applyNegativeConstraints()
		self.p4.applyNegativeConstraints()

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
		overlap = self.boardWidth-self.boardSizeRoot
		# p1
		for i in range(overlap):
			# Space before p1
			print(' '*((1+dW)*overlap),end = '')
			# p1
			for j in range(self.boardWidth):
				print('{:d}'.format(self.solver.Value(self.p1.getCellVar(i,j))).rjust(dW),end = " ")
			print()

		#p2/p1/p3 rows
		for i in range(self.boardSizeRoot):
			#p2 cells
			for j in range(overlap):
				print('{:d}'.format(self.solver.Value(self.p2.getCellVar(i,j))).rjust(dW),end = " ")
			#p1/p2 overlap
			for j in range(self.boardSizeRoot):
				print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p2.getCellVar(i,overlap+j))).rjust(dW)+Fore.RESET,end = " ")
			#p1 box 8
			for j in range(self.boardSizeRoot):
				print('{:d}'.format(self.solver.Value(self.p1.getCellVar(overlap+i,self.boardSizeRoot+j))).rjust(dW),end = " ")
			#p1/p3 overlap
			for j in range(self.boardSizeRoot):
				print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p3.getCellVar(i,j))).rjust(dW)+Fore.RESET,end = " ")
			#p3 cells
			for j in range(overlap):
				print('{:d}'.format(self.solver.Value(self.p3.getCellVar(i,self.boardSizeRoot+j))).rjust(dW),end = " ")
			print()
		
		#Middle row
		for i in range(self.boardSizeRoot):
			#p2 cells
			for j in range(self.boardWidth):
				print('{:d}'.format(self.solver.Value(self.p2.getCellVar(self.boardSizeRoot+i,j))).rjust(dW),end = " ")
			#hole
			print(' '*((1+dW)*self.boardSizeRoot),end = '')
			#p3 cells
			for j in range(self.boardWidth):
				print('{:d}'.format(self.solver.Value(self.p3.getCellVar(self.boardSizeRoot+i,j))).rjust(dW),end = " ")
			print()
				
		#p2/p4/p3 rows
		for i in range(self.boardSizeRoot):
			#p2 cells
			for j in range(overlap):
				print('{:d}'.format(self.solver.Value(self.p2.getCellVar(overlap+i,j))).rjust(dW),end = " ")
			#p2/p4 overlap
			for j in range(self.boardSizeRoot):
				print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p2.getCellVar(overlap+i,overlap+j))).rjust(dW)+Fore.RESET,end = " ")
			#p4 box 2
			for j in range(self.boardSizeRoot):
				print('{:d}'.format(self.solver.Value(self.p4.getCellVar(i,self.boardSizeRoot+j))).rjust(dW),end = " ")
			#p3/p4 overlap
			for j in range(self.boardSizeRoot):
				print(Fore.CYAN+'{:d}'.format(self.solver.Value(self.p4.getCellVar(i,overlap+j))).rjust(dW)+Fore.RESET,end = " ")
			#p3 cells
			for j in range(overlap):
				print('{:d}'.format(self.solver.Value(self.p3.getCellVar(overlap+i,self.boardSizeRoot+j))).rjust(dW),end = " ")
			print()
		
		for i in range(overlap):
			# Space before p4
			print(' '*((1+dW)*overlap),end = '')
			# p4
			for j in range(self.boardWidth):
				print('{:d}'.format(self.solver.Value(self.p4.getCellVar(self.boardSizeRoot+i,j))).rjust(dW),end = " ")
			print()

