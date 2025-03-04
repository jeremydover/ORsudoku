import math
import re

def _varBitmap(self,string,num):
	# Utility function to create a list of Boolean variable propositions that encode num possibilities exactly.
	# string is used to label the variables
	# Implements model constraints to ensure "extra"
	
	if num == 1:
		# We just create a single variable that is always true
		bits = [self.model.NewBoolVar(string+'BM0')]
		self.model.AddBoolAnd(bits[0]).OnlyEnforceIf(bits[0].Not())
		var = [[bits[0]]]
	else:
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
		
		if (num > 2):
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
	
def _procCell(self,cell):
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
		
def _procCellList(self,inlist):
	# Utility function to process a list from one of several input formats into the tuple format
	# required by our functions
	return list(map(lambda x: self._procCell(x),inlist))
	
def getOrthogonalNeighbors(self,i,j):
	#return [(i+k,j+m) for k in [-1,0,1] for m in [-1,0,1] if i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth and abs(k) != abs(m)]
	return list({(i+k,j+m) for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)})
	
def _selectCellsMatchDigitSet(self,myVars,L,values):
	if type(values) is int:
		values = [values]
	for i in range(len(myVars)):
		for j in self.digits:
			if j in values:
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] != j).OnlyEnforceIf(myVars[i].Not())
			else:
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] != j).OnlyEnforceIf(myVars[i])

def _selectCellsOnLine(self,L,selectCriteria,initiatorCells=[]):
	
	# Migrated from a version which worked on row/column, should not be too hard :-)
	# I'm going to create selection Booleans to evaluate each cell against the selectCriteria criteria. 
	# Notice how I'm clever enough to avoid defining selectSummands as long as I can. #genius
	selectionCells = [self.model.NewBoolVar('SelectionCondition{:d}'.format(i)) for i in range(len(L))]
	self.allVars = self.allVars + selectionCells
	
	# OK, document as I go! selectCriteria is an array of criteria, all of which must be true for a cell to be
	# selected. Each array element is itself a tuple of at least two items: property, value.
	# More than one value may be given, and depend on the property how they are interpreted
	# 
	# Property: 'Location'
	#   For this property, we are picking cells based on their position within the clued row/column.
	#   Values[0]: A comparator: use the class variables GE, EQ or LE, or NE if you really think that's useful
	#   Values[1]: location to stop
	#   So for example, ('Location',p.GE,4) would include all cells in the two boxes not adjacent to the clue. Yes, this is just a cage. I get it.
	#
	# Property: 'LocationSkip'
	#   Hah, it's not just cages.
	#   For this property, we can pick every other, every third, etc. cell
	#   Values[0]: Skip number, 2 skips every other, etc.
	#   Values[1]: Start number, cell in (0...skip-1} to start at
	#
	# Property: 'Magnitude'
	#   For this property, we select digits based on whether they're big or small.
	#   Values[0]: A comparator. Again, NE and EQ don't seem particularly useful, but I'll put em in anyway
	#   Values[1]: Value for comparison
	#
	# Property: 'Parity'
	#   For this property, we will pick cells based on parity.
	#   Value: Use 0 for even, 1 for odd. Or you can use the Even/Odd class variables.
	#
	# Property: 'Entropy'
	#  For this property, we pick cells based on Entropy class: low: 1,2,3, middle: 4,5,6, high: 7,8,9
	#  Values[0]: Use any comparator class variable: NE, EQ, LE, GE
	#  Values[1]: Values for comparison: again, use class variables Low, Middle, High
	#
	# Property: 'Modular'
	#  For this property, we pick cells based on Modulus class: 1: 1,4,7, 2: 2,5,8, 3: 3,6,9
	#  Values[0]: Use any comparator class variable: NE, EQ, LE, GE. Mathematically, LE and GE don't really make much sense, but they work.
	#  Values[1]: Values for comparison: again, use class variables Low, Middle, High
	#
	# Property: 'Primality'
	# For this property, we pick cells based on whether their digit is prime or not. Which brings up the 1 problem.
	# For purposes here, "not prime" is 0: 4,6,8,9; "maybe kinda" is 1: 1; "prime" is 2: 2,3,5,7. Like modular, evern though the LE and GE 
	# comparisons don't really make sense, you can use them.
	#
	# Property: 'MatchParity'
	# For this property, we pick cells if they match the parity of the cell specified in value
	# Value: cell whose parity to match
	#
	# Property: 'MatchEntropy'
	# For this property, we pick cells if they match the entropy of the cell specified in value
	# Value: cell whose parity to match
	#
	# Property: 'MatchModular'
	# For this property, we pick cells if they match the modularity of the cell specified in value
	# Value: cell whose parity to match
	#
	# Property: 'ParityChange', 'EntropyChange', 'ModularChange', 'PrimalityChange'
	# For this property, slect the values either before or after a change in the specified property
	# Value: 'before' or 'after'

	criteriaBools = []
	criterionNumber = 0
	for criterion in selectCriteria:
		criterionBools = [self.model.NewBoolVar('Criterion{:d}{:d}'.format(criterionNumber,i)) for i in range(len(L))]
		self.allVars = self.allVars + criterionBools
		
		match criterion[0]:
			case 'All':
				self.model.AddBoolAnd(criterionBools)
			
			case 'Location':
				thisCriterion = 0
				theseCriteria = []
				for n in range(1,len(criterion),2):
					thisCriterionBools = [self.model.NewBoolVar('Criterion{:d}{:d}'.format(criterionNumber,i)) for i in range(len(L))]
					
					match criterion[n]:
						case self.LE:
							self.model.AddBoolAnd([thisCriterionBools[j] for j in range(criterion[n+1])])
							self.model.AddBoolAnd([thisCriterionBools[j].Not() for j in range(criterion[n+1],len(L))])
						case self.EQ:
							self.model.AddBoolAnd([thisCriterionBools[criterion[n+1]-1]])
							self.model.AddBoolAnd([thisCriterionBools[j].Not() for j in range(len(L)) if j != criterion[n+1]-1])
						case self.GE:
							self.model.AddBoolAnd([thisCriterionBools[j].Not() for j in range(criterion[n+1]-1)])
							self.model.AddBoolAnd([thisCriterionBools[j] for j in range(criterion[n+1]-1,len(L))])
						case self.NE:
							self.model.AddBoolAnd([thisCriterionBools[criterion[n+1]-1].Not()])
							self.model.AddBoolAnd([thisCriterionBools[j] for j in range(len(L)) if j != criterion[n+1]-1])
						case 'Indexed':
							for i in range(len(L)):
								self.model.Add(self.cellValues[L[criterion[n+1]-1][0]][L[criterion[n+1]-1][1]] == i+1).OnlyEnforceIf(thisCriterionBools[i])
								self.model.Add(self.cellValues[L[criterion[n+1]-1][0]][L[criterion[n+1]-1][1]] != i+1).OnlyEnforceIf(thisCriterionBools[i].Not())
			
					theseCriteria.insert(thisCriterion,thisCriterionBools)
					thisCriterion = thisCriterion + 1
				for i in range(len(L)):
					self.model.AddBoolOr([theseCriteria[j][i] for j in range(len(theseCriteria))]).OnlyEnforceIf(criterionBools[i])
					self.model.AddBoolAnd([theseCriteria[j][i].Not() for j in range(len(theseCriteria))]).OnlyEnforceIf(criterionBools[i].Not())
					
			case 'LocationSkip':
				self.model.AddBoolAnd([criterionBools[j] for j in range(len(L)) if (j % criterion[1]) == criterion[2]])
				self.model.AddBoolAnd([criterionBools[j].Not() for j in range(len(L)) if (j % criterion[1]) != criterion[2]])
				
			case 'Magnitude':
				for i in range(len(L)):
					match criterion[1]:
						case self.LE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] <= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] > criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.EQ:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] == criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] != criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.GE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] >= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] < criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.NE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] != criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] == criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
			
			case 'Parity' | 'Entropy' | 'Modular' | 'Primality':
				if criterion[0] not in self._propertyInitialized:
					getattr(self,'_set'+criterion[0])()
				myCells = getattr(self,'cell'+criterion[0])
				for i in range(len(L)):
					match criterion[1]:
						case self.LE:
							self.model.Add(myCells[L[i][0]][L[i][1]] <= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(myCells[L[i][0]][L[i][1]] > criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.EQ:
							self.model.Add(myCells[L[i][0]][L[i][1]] == criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(myCells[L[i][0]][L[i][1]] != criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.GE:
							self.model.Add(myCells[L[i][0]][L[i][1]] >= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(myCells[L[i][0]][L[i][1]] < criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.NE:
							self.model.Add(myCells[L[i][0]][L[i][1]] != criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(myCells[L[i][0]][L[i][1]] == criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
							
			case 'Uniparity':
				self._initializeParity()
				c = self.model.NewBoolVar('selectionCriteriaUnipartyPickEven')
				d = self.model.NewBoolVar('selectionCriteriaUnipartyPickOdd')
				for i in range(len(L)):
					self.model.Add(self.cellParity[L[i][0]][L[i][1]] == 0).OnlyEnforceIf([criterionBools[i],c])
					self.model.Add(self.cellParity[L[i][0]][L[i][1]] == 1).OnlyEnforceIf([criterionBools[i].Not(),c])
					self.model.Add(self.cellParity[L[i][0]][L[i][1]] == 1).OnlyEnforceIf([criterionBools[i],d])
					self.model.Add(self.cellParity[L[i][0]][L[i][1]] == 0).OnlyEnforceIf([criterionBools[i].Not(),d])
				self.model.AddBoolXOr([c,d])
							
			case 'MatchParity' | 'MatchEntropy' | 'MatchModular' | 'MatchPrimality':
				if criterion[0][5:] not in self._propertyInitialized:
					getattr(self,'_set'+criterion[0][5:])()
				mCell = criterion[1] - 1
				myCells = getattr(self,'cell'+criterion[0][5:])
				for i in range(len(L)):
					self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[mCell][0]][L[mCell][1]]).OnlyEnforceIf(criterionBools[i])
					self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[mCell][0]][L[mCell][1]]).OnlyEnforceIf(criterionBools[i].Not())
							
			case 'ParityChange' | 'EntropyChange' | 'ModularChange' | 'PrimalityChange':
				if criterion[0][0:-6] not in self._propertyInitialized:
					getattr(self,'_set'+criterion[0][0:-6])()
				if criterion[1] == 'before':
					self.model.AddBoolAnd(criterionBools[-1].Not())  # last cell cannot be picked
				else:
					self.model.AddBoolAnd(criterionBools[0].Not())  # first cell cannot be picked
				myCells = getattr(self,'cell'+criterion[0][0:-6])
				for i in range(1,len(L)):
					if criterion[1] == 'before':
						self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf(criterionBools[i-1])
						self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf(criterionBools[i-1].Not())
					else:
						self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf(criterionBools[i])
						self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf(criterionBools[i].Not())
					
			case 'DigitSet':
				self._selectCellsMatchDigitSet(criterionBools,L,criterion[1])
							
			case 'BeforeDigits':
				matchDigit = [self.model.NewBoolVar('BeforeDigitsMatch') for i in range(len(L))]
				self._selectCellsMatchDigitSet(matchDigit,L,criterion[1])
				self.model.AddBoolAnd(criterionBools[-1].Not()).OnlyEnforceIf(criterionBools[-1])
				for i in range(1,len(L)):
					self.model.AddBoolAnd(criterionBools[i-1]).OnlyEnforceIf(matchDigit[i])
					self.model.AddBoolAnd(criterionBools[i-1].Not()).OnlyEnforceIf(matchDigit[i].Not())

			case 'AfterDigits':
				matchDigit = [self.model.NewBoolVar('AfterDigitsMatch') for i in range(len(L))]
				self._selectCellsMatchDigitSet(matchDigit,L,criterion[1])
				self.model.AddBoolAnd(criterionBools[0].Not()).OnlyEnforceIf(criterionBools[0])
				for i in range(len(L)-1):
					self.model.AddBoolAnd(criterionBools[i+1]).OnlyEnforceIf(matchDigit[i])
					self.model.AddBoolAnd(criterionBools[i+1].Not()).OnlyEnforceIf(matchDigit[i].Not())
					
			case 'NextToDigits':
				matchDigit = [self.model.NewBoolVar('AfterDigitsMatch') for i in range(len(L))]
				self._selectCellsMatchDigitSet(matchDigit,L,criterion[1])
				self.model.AddBoolAnd(criterionBools[0]).OnlyEnforceIf(matchDigit[1])
				self.model.AddBoolAnd(criterionBools[0].Not()).OnlyEnforceIf(matchDigit[1].Not())
				self.model.AddBoolAnd(criterionBools[-1]).OnlyEnforceIf(matchDigit[-2])
				self.model.AddBoolAnd(criterionBools[-1].Not()).OnlyEnforceIf(matchDigit[-2].Not())
				for i in range(1,len(L)-1):
					self.model.AddBoolOr([matchDigit[i-1],matchDigit[i+1]]).OnlyEnforceIf(criterionBools[i])
					self.model.AddBoolAnd([matchDigit[i-1].Not(),matchDigit[i+1].Not()]).OnlyEnforceIf(criterionBools[i].Not())
						
			case 'DigitInstance':
				instanceCount = [self.model.NewIntVar(0,len(L),'SelectionCriterionInstanceCount') for i in range(len(L))]
				self.model.Add(instanceCount[0] == 1)
				for i in range(1,len(L)):
					isFirst = self.model.NewBoolVar('SelectionCriterionIsFirst')
					for j in range(i):
						self.model.Add(self.cellValues[L[j][0]][L[j][1]] != self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf(isFirst)
					self.model.Add(instanceCount[i] == 1).OnlyEnforceIf(isFirst)
					
					lastMatch = [self.model.NewBoolVar('SelectionCriterionLastMatch') for j in range(i)]
					self.model.AddBoolOr(lastMatch).OnlyEnforceIf(isFirst.Not())
					self.model.AddBoolAnd([x.Not() for x in lastMatch]).OnlyEnforceIf(isFirst)
					
					for j in range(i):
						self.model.Add(self.cellValues[L[j][0]][L[j][1]] == self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf(lastMatch[j])
						for k in range(j+1,i):
							self.model.Add(self.cellValues[L[k][0]][L[k][1]] != self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf(lastMatch[j])
						self.model.Add(instanceCount[i] == instanceCount[j] + 1).OnlyEnforceIf(lastMatch[j])
					
				for i in range(len(L)):
					match criterion[1]:
						case self.LE:
							self.model.Add(instanceCount[i] <= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(instanceCount[i] > criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.EQ:
							self.model.Add(instanceCount[i] == criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(instanceCount[i] != criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.GE:
							self.model.Add(instanceCount[i] >= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(instanceCount[i] < criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.NE:
							self.model.Add(instanceCount[i] != criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(instanceCount[i] == criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
			case 'NoRepeats':
				matchVars = []
				for i in range(len(L)):
					myMatchVars = [self.model.NewBoolVar('SelectionNoRepeatsMatch{:d}{:d}'.format(i,j)) for j in range(i)]
					matchVars.insert(i,myMatchVars)
					for j in range(i):
						self.model.Add(self.cellValues[L[i][0]][L[i][1]] == self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf(myMatchVars[j])
						self.model.Add(self.cellValues[L[i][0]][L[i][1]] != self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf(myMatchVars[j].Not())
				for i in range(len(L)):
					self.model.AddBoolAnd([x.Not() for x in matchVars[i]] + [matchVars[j][i].Not() for j in range(i+1,len(L))]).OnlyEnforceIf(criterionBools[i])
					self.model.AddBoolOr(matchVars[i] + [matchVars[j][i] for j in range(i+1,len(L))]).OnlyEnforceIf(criterionBools[i].Not())
			case 'ConsecutiveNeighbor'|'ConsecutiveBefore'|'ConsecutiveAfter'|'ConsecutiveNone':
				consecPair = [self.model.NewBoolVar('ConsecPair') for j in range(len(L)-1)]
				maxPair = [self.model.NewIntVar(self.minDigit,self.maxDigit,'ConsecPairMax') for j in range(len(L)-1)]
				minPair = [self.model.NewIntVar(self.minDigit,self.maxDigit,'ConsecPairMin') for j in range(len(L)-1)]
				for i in range(len(L)-1):
					self.model.AddMinEquality(minPair[i],[self.cellValues[L[i][0]][L[i][1]],self.cellValues[L[i+1][0]][L[i+1][1]]])
					self.model.AddMaxEquality(maxPair[i],[self.cellValues[L[i][0]][L[i][1]],self.cellValues[L[i+1][0]][L[i+1][1]]])
					self.model.Add(maxPair[i] - minPair[i] == 1).OnlyEnforceIf(consecPair[i])
					self.model.Add(maxPair[i] - minPair[i] != 1).OnlyEnforceIf(consecPair[i].Not())
				
				if criterion[0] == 'ConsecutiveNeighbor':
					self.model.AddBoolAnd(consecPair[0]).OnlyEnforceIf(criterionBools[0])
					self.model.AddBoolAnd(consecPair[0].Not()).OnlyEnforceIf(criterionBools[0].Not())
					self.model.AddBoolAnd(consecPair[-1]).OnlyEnforceIf(criterionBools[-1])
					self.model.AddBoolAnd(consecPair[-1].Not()).OnlyEnforceIf(criterionBools[-1].Not())
					for i in range(1,len(L)-1):
						self.model.AddBoolOr([consecPair[i-1],consecPair[i]]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolAnd([consecPair[i-1].Not(),consecPair[i].Not()]).OnlyEnforceIf(criterionBools[i].Not())
				elif criterion[0] == 'ConsecutiveBefore':
					self.model.AddBoolAnd(criterionBools[0].Not())
					for i in range(1,len(L)):
						self.model.AddBoolAnd(consecPair[i-1]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolAnd(consecPair[i-1].Not()).OnlyEnforceIf(criterionBools[i].Not())
				elif criterion[0] == 'ConsecutiveAfter':
					self.model.AddBoolAnd(criterionBools[-1].Not())
					for i in range(len(L)-1):
						self.model.AddBoolAnd(consecPair[i]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolAnd(consecPair[i].Not()).OnlyEnforceIf(criterionBools[i].Not())
				elif criterion[0] == 'ConsecutiveNone':
					self.model.AddBoolAnd(consecPair[0].Not()).OnlyEnforceIf(criterionBools[0])
					self.model.AddBoolAnd(consecPair[0]).OnlyEnforceIf(criterionBools[0].Not())
					self.model.AddBoolAnd(consecPair[-1].Not()).OnlyEnforceIf(criterionBools[-1])
					self.model.AddBoolAnd(consecPair[-1]).OnlyEnforceIf(criterionBools[-1].Not())
					for i in range(1,len(L)-1):
						self.model.AddBoolAnd([consecPair[i-1].Not(),consecPair[i].Not()]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolOr([consecPair[i-1],consecPair[i]]).OnlyEnforceIf(criterionBools[i].Not())
			case 'ParityNeighbor'|'ParityBefore'|'ParityAfter'|'ParityNone'|'ParityAll'|'ParityBoth'|'ParityNeither'|'EntropyNeighbor'|'EntropyBefore'|'EntropyAfter'|'EntropyNone'|'EntropyAll'|'EntropyBoth'|'EntropyNeither'|'ModularNeighbor'|'ModularBefore'|'ModularAfter'|'ModularNone'|'ModularAll'|'ModularBoth'|'ModularNeither'|'PrimalityNeighbor'|'PrimalityBefore'|'PrimalityAfter'|'PrimalityNone'|'PrimalityAll'|'PrimalityBoth'|'PrimalityNeither':
				x = re.search("(Parity|Entropy|Modular|Primality)(.*)",criterion[0])
				mode = x.group(1)
				where = x.group(2)
				if mode not in self._propertyInitialized:
					getattr(self,'_set'+mode)()
				myCells = getattr(self,'cell'+mode)
				matchForward = [self.model.NewBoolVar('HasNeighborForward') for j in range(len(L))]
				matchBackward = [self.model.NewBoolVar('HasNeighborBackward') for j in range(len(L))]
				for i in range(len(L)):
					if len(criterion) > 1:
						testValue = criterion[1]
					else:
						testValue = myCells[L[i][0]][L[i][1]]
					if i == 0:
						self.model.AddBoolAnd(matchBackward[i].Not())
					else:
						self.model.Add(myCells[L[i-1][0]][L[i-1][1]] == testValue).OnlyEnforceIf(matchBackward[i])
						self.model.Add(myCells[L[i-1][0]][L[i-1][1]] != testValue).OnlyEnforceIf(matchBackward[i].Not())
					if i == len(L)-1:
						self.model.AddBoolAnd(matchForward[i].Not())
					else:
						self.model.Add(myCells[L[i+1][0]][L[i+1][1]] == testValue).OnlyEnforceIf(matchForward[i])
						self.model.Add(myCells[L[i+1][0]][L[i+1][1]] != testValue).OnlyEnforceIf(matchForward[i].Not())
						
				if where == 'Neighbor':
					for i in range(len(L)):
						self.model.AddBoolOr([matchForward[i],matchBackward[i]]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolAnd([matchForward[i].Not(),matchBackward[i].Not()]).OnlyEnforceIf(criterionBools[i].Not())
				elif where == 'Before':
					for i in range(len(L)):
						self.model.AddBoolAnd(matchBackward[i]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolAnd(matchBackward[i].Not()).OnlyEnforceIf(criterionBools[i].Not())
				elif where == 'After':
					for i in range(len(L)):
						self.model.AddBoolAnd(matchForward[i]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolAnd(matchForward[i].Not()).OnlyEnforceIf(criterionBools[i].Not())
				elif where == 'None':
					for i in range(len(L)):
						self.model.AddBoolAnd([matchBackward[i].Not(),matchForward[i].Not()]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolOr([matchBackward[i],matchForward[i]]).OnlyEnforceIf(criterionBools[i].Not())
				elif where == 'All':
					self.model.AddBoolAnd(matchForward[0]).OnlyEnforceIf(criterionBools[0])
					self.model.AddBoolAnd(matchForward[0].Not()).OnlyEnforceIf(criterionBools[0].Not())
					self.model.AddBoolAnd(matchBackward[-1]).OnlyEnforceIf(criterionBools[-1])
					self.model.AddBoolAnd(matchBackward[-1].Not()).OnlyEnforceIf(criterionBools[-1].Not())
					for i in range(1,len(L)-1):
						self.model.AddBoolAnd([matchBackward[i],matchForward[i]]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolOr([matchBackward[i].Not(),matchForward[i].Not()]).OnlyEnforceIf(criterionBools[i].Not())
				elif where == 'Both':
					self.model.AddBoolAnd([criterionBools[0].Not(),criterionBools[-1].Not()])
					for i in range(1,len(L)-1):
						self.model.AddBoolAnd([matchBackward[i],matchForward[i]]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolOr([matchBackward[i].Not(),matchForward[i].Not()]).OnlyEnforceIf(criterionBools[i].Not())
				elif where == 'Neither':
					self.model.AddBoolAnd([criterionBools[0].Not(),criterionBools[-1].Not()])
					for i in range(1,len(L)-1):
						self.model.AddBoolAnd([matchBackward[i].Not(),matchForward[i].Not()]).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolOr([matchBackward[i],matchForward[i]]).OnlyEnforceIf(criterionBools[i].Not())
			case 'ParityRun'|'EntropyRun'|'ModularRun'|'PrimalityRun':
				if criterion[0][0:-3] not in self._propertyInitialized:
					getattr(self,'_set'+criterion[0][0:-3])()
				myCells = getattr(self,'cell'+criterion[0][0:-3])
				
				# First split the line up into contiguous runs with the same property
				runNumber = [self.model.NewIntVar(1,len(L),'PropertyRunSelectionRunNumber') for i in range(len(L))]
				propertySwitch = [self.model.NewBoolVar('PropertyRunSwitch') for i in range(len(L))]
				self.model.Add(runNumber[0] == 1)
				self.model.AddBoolAnd(propertySwitch[0].Not())
				for i in range(1,len(L)):
					self.model.Add(myCells[L[i-1][0]][L[i-1][1]] == myCells[L[i][0]][L[i][1]]).OnlyEnforceIf(propertySwitch[i].Not())
					self.model.Add(myCells[L[i-1][0]][L[i-1][1]] != myCells[L[i][0]][L[i][1]]).OnlyEnforceIf(propertySwitch[i])
					self.model.Add(runNumber[i] == runNumber[i-1]).OnlyEnforceIf(propertySwitch[i].Not())
					self.model.Add(runNumber[i] == runNumber[i-1]+1).OnlyEnforceIf(propertySwitch[i])
				
				filteredRunNumber = [self.model.NewIntVar(0,len(L),'PropertyRunSelectionFilteredNumber') for i in range(len(L))]
				filteredRunCount = [self.model.NewIntVar(0,len(L),'PropertyRunSelectionFilteredCount') for i in range(len(L))]
				
				match criterion[1][0]:
					case 'Any':
						for i in range(len(L)):
							self.model.Add(filteredRunNumber[i] == runNumber[i])
					case _:
						propertyMatch = [self.model.NewBoolVar('PropertyRunMatch') for i in range(len(L))]
						if criterion[1][0] == 'Property':
							comparisonValue = criterion[1][2]
						else:
							comparisonValue = myCells[L[criterion[1][2]-1][0]][L[criterion[1][2]-1][1]]
						for i in range(len(L)):
							match criterion[1][1]:
								case self.EQ:
									self.model.Add(myCells[L[i][0]][L[i][1]] == comparisonValue).OnlyEnforceIf(propertyMatch[i])
									self.model.Add(myCells[L[i][0]][L[i][1]] != comparisonValue).OnlyEnforceIf(propertyMatch[i].Not())
								case self.LE:
									self.model.Add(myCells[L[i][0]][L[i][1]] <= comparisonValue).OnlyEnforceIf(propertyMatch[i])
									self.model.Add(myCells[L[i][0]][L[i][1]] > comparisonValue).OnlyEnforceIf(propertyMatch[i].Not())
								case self.GE:
									self.model.Add(myCells[L[i][0]][L[i][1]] >= comparisonValue).OnlyEnforceIf(propertyMatch[i])
									self.model.Add(myCells[L[i][0]][L[i][1]] < comparisonValue).OnlyEnforceIf(propertyMatch[i].Not())
								case self.NE:
									self.model.Add(myCells[L[i][0]][L[i][1]] != comparisonValue).OnlyEnforceIf(propertyMatch[i])
									self.model.Add(myCells[L[i][0]][L[i][1]] == comparisonValue).OnlyEnforceIf(propertyMatch[i].Not())
							if i == 0:
								self.model.Add(filteredRunNumber[0] == 1).OnlyEnforceIf(propertyMatch[0])
								self.model.Add(filteredRunNumber[0] == 0).OnlyEnforceIf(propertyMatch[0].Not())
								self.model.Add(filteredRunCount[0] == 1).OnlyEnforceIf(propertyMatch[0])
								self.model.Add(filteredRunCount[0] == 0).OnlyEnforceIf(propertyMatch[0].Not())
							else:
								# propertySwitch determines if the property switch is here; if not, keep these steady
								self.model.Add(filteredRunNumber[i] == filteredRunNumber[i-1]).OnlyEnforceIf(propertySwitch[i].Not())
								self.model.Add(filteredRunCount[i] == filteredRunCount[i-1]).OnlyEnforceIf(propertySwitch[i].Not())
								
								# Now if there is a switch and the new cell is a property match, create a new filtered group number
								self.model.Add(filteredRunNumber[i] == filteredRunCount[i-1]+1).OnlyEnforceIf([propertySwitch[i],propertyMatch[i]])
								self.model.Add(filteredRunCount[i] == filteredRunCount[i-1]+1).OnlyEnforceIf([propertySwitch[i],propertyMatch[i]])
							
								# If there is a switch, but the new cell is not a match, we don't increment the countm, and we make the run number 0
								self.model.Add(filteredRunNumber[i] == 0).OnlyEnforceIf([propertySwitch[i],propertyMatch[i].Not()])
								self.model.Add(filteredRunCount[i] == filteredRunCount[i-1]).OnlyEnforceIf([propertySwitch[i],propertyMatch[i].Not()])
				if type(criterion[2]) is int:
					for i in range(len(L)):
						self.model.Add(filteredRunNumber[i] == criterion[2]).OnlyEnforceIf(criterionBools[i])
						self.model.Add(filteredRunNumber[i] != criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
				elif criterion[2] == 'Last':
					for i in range(len(L)):
						self.model.Add(filteredRunNumber[i] == filteredRunCount[-1]).OnlyEnforceIf(criterionBools[i])
						self.model.Add(filteredRunNumber[i] != filteredRunCount[-1]).OnlyEnforceIf(criterionBools[i].Not())
				else:
					for i in range(len(L)):
						myBools = [self.model.NewBoolVar('PropertyRunSelectionMultipleRanges') for j in range(len(criterion[2]))]
						for j in range(len(criterion[2])):
							if type(criterion[2][j]) is int:
								self.model.Add(filteredRunNumber[i] == criterion[2][j]).OnlyEnforceIf(myBools[j])
								self.model.Add(filteredRunNumber[i] != criterion[2][j]).OnlyEnforceIf(myBools[j].Not())
							else:
								self.model.Add(filteredRunNumber[i] == filteredRunCount[-1]).OnlyEnforceIf(myBools[j])
								self.model.Add(filteredRunNumber[i] != filteredRunCount[-1]).OnlyEnforceIf(myBools[j].Not())
						self.model.AddBoolOr(myBools).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolAnd([x.Not() for x in myBools]).OnlyEnforceIf(criterionBools[i].Not())
			case 'AscendingRun'|'DescendingRun':
				# First split the line up into contiguous runs
				runNumber = [self.model.NewIntVar(1,len(L),'UpDownRunSelectionRunNumber') for i in range(len(L))]
				runSwitch = [self.model.NewBoolVar('UpDownRunSwitch') for i in range(len(L))]
				self.model.Add(runNumber[0] == 1)
				self.model.AddBoolAnd(runSwitch[0].Not())
				for i in range(1,len(L)):
					if criterion[0] == 'AscendingRun':
						self.model.Add(self.cellValues[L[i-1][0]][L[i-1][1]] < self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf(runSwitch[i].Not())
						self.model.Add(self.cellValues[L[i-1][0]][L[i-1][1]] >= self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf(runSwitch[i])	
					else:
						self.model.Add(self.cellValues[L[i-1][0]][L[i-1][1]] > self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf(runSwitch[i].Not())
						self.model.Add(self.cellValues[L[i-1][0]][L[i-1][1]] <= self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf(runSwitch[i])	
					self.model.Add(runNumber[i] == runNumber[i-1]).OnlyEnforceIf(runSwitch[i].Not())
					self.model.Add(runNumber[i] == runNumber[i-1]+1).OnlyEnforceIf(runSwitch[i])
				if type(criterion[1]) is int:
					for i in range(len(L)):
						self.model.Add(runNumber[i] == criterion[1]).OnlyEnforceIf(criterionBools[i])
						self.model.Add(runNumber[i] != criterion[1]).OnlyEnforceIf(criterionBools[i].Not())
				elif criterion[1] == 'Last':
					for i in range(len(L)):
						self.model.Add(runNumber[i] == runNumber[-1]).OnlyEnforceIf(criterionBools[i])
						self.model.Add(runNumber[i] != runNumber[-1]).OnlyEnforceIf(criterionBools[i].Not())
				else:
					for i in range(len(L)):
						myBools = [self.model.NewBoolVar('UpDownRunSelectionMultipleRanges') for j in range(len(criterion[1]))]
						for j in range(len(criterion[1])):
							if type(criterion[1][j]) is int:
								self.model.Add(runNumber[i] == criterion[1][j]).OnlyEnforceIf(myBools[j])
								self.model.Add(runNumber[i] != criterion[1][j]).OnlyEnforceIf(myBools[j].Not())
							else:
								self.model.Add(runNumber[i] == runNumber[-1]).OnlyEnforceIf(myBools[j])
								self.model.Add(runNumber[i] != runNumber[-1]).OnlyEnforceIf(myBools[j].Not())
						self.model.AddBoolOr(myBools).OnlyEnforceIf(criterionBools[i])
						self.model.AddBoolAnd([x.Not() for x in myBools]).OnlyEnforceIf(criterionBools[i].Not())
			case 'Skyscrapers':
				# Select the cells which are the maximum of all cells seens thus far
				self.model.AddBoolAnd(criterionBools[0])
				for i in range(1,len(L)):
					maxVar = self.model.NewIntVar(0,max(self.digits),'SelectionSkyscraper{:d}'.format(i))
					self.model.AddMaxEquality(maxVar,[self.cellValues[L[j][0]][L[j][1]] for j in range(i+1)])
					self.model.Add(self.cellValues[L[i][0]][L[i][1]] == maxVar).OnlyEnforceIf(criterionBools[i])
					self.model.Add(self.cellValues[L[i][0]][L[i][1]] < maxVar).OnlyEnforceIf(criterionBools[i].Not())
		criteriaBools.insert(criterionNumber,criterionBools)
		criterionNumber = criterionNumber + 1
	
	# Ensure selectionCells[i] is True if and only if each of the underlying criteria is
	for i in range(len(L)):
		self.model.AddBoolAnd([criteriaBools[j][i] for j in range(len(criteriaBools))]).OnlyEnforceIf(selectionCells[i])
		self.model.AddBoolOr([criteriaBools[j][i].Not() for j in range(len(criteriaBools))]).OnlyEnforceIf(selectionCells[i].Not())
		
	return selectionCells

def _selectCellsInRowCol(self,row,col,rc,selectCriteria):
	
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	L = [(row+i*vStep,col+i*hStep) for i in range(self.boardWidth)]
	selectionCells = self._selectCellsOnLine(L,selectCriteria)
	return selectionCells

	
def _terminateCellsOnLine(self,L,selectTerminator):
	
	# Well, I'll be danged. That actually went surprisingly well. Which means the terminator is going to be a bear, because I initially thought it'd be straightforward. The good news is we don't have to worry about multiple criteria...just one is going to apply. As before I'll document here as I code. As before, a select terminator is going to be a tuple, with the first element the terminator name.
	
	# Terminator: 'Fixed'
	# We're terminating at a fixed index in the row/column, e.g. the first six cells.
	# Value: index at which to terminate sum
	# 
	# Terminator: 'SumReached'
	# Terminate when a particular sum is reached or exceeded, value is the sum that is reached
	# Value: target sum
	#
	# Terminator: 'DigitReached'
	# Terminate when a fixed digit is reached
	# Value: target digit
	#
	# Terminator: 'DigitSetReached'
	# Terminate when some numbered instance of a digit set is reached
	# Values[0]: list of target digits
	# Values[1]: nth instance of target
	#
	# Terminator: 'ParityChangeReached'
	# Terminate when some numbered instance of a change in parity occurs
	# Value: nth instance of target
	#
	# Terminator: 'EntropyChangeReached'
	# Terminate when some numbered instance of a change in entropy occurs
	# Value: nth instance of target
	#
	# Terminator: 'ModularChangeReached'
	# Terminate when some numbered instance of a change in modular occurs
	# Value: nth instance of target	
	
	terminatorCells = [self.model.NewBoolVar('HangingSumTermination{:d}'.format(i)) for i in range(len(L))]
	self.allVars = self.allVars + terminatorCells
	terminatorBools = []
	terminatorNumber = 0
	for terminator in selectTerminator:
		termBools = [self.model.NewBoolVar('TermCriterion{:d}{:d}'.format(terminatorNumber,i)) for i in range(len(L))]
		self.allVars = self.allVars + termBools
		match terminator[0]:
			case 'Last':
				self.model.AddBoolAnd([termBools[j].Not() for j in range(len(L)-1)])
				self.model.AddBoolAnd(termBools[-1])
			case 'Fixed':
				self.model.AddBoolAnd(termBools[terminator[1]-1])
				self.model.AddBoolAnd([termBools[j].Not() for j in range(len(L)) if j != terminator[1]-1])
			case 'SumReached':
				self.model.Add(self.cellValues[L[0][0]][L[0][1]] >= terminator[1]).OnlyEnforceIf(termBools[0])
				self.model.Add(self.cellValues[L[0][0]][L[0][1]] < terminator[1]).OnlyEnforceIf(termBools[0].Not())
				for i in range(1,len(L)):
					self.model.Add(sum(self.cellValues[L[j][0]][L[j][1]] for j in range(i)) < terminator[1]).OnlyEnforceIf(termBools[i])
					self.model.Add(sum(self.cellValues[L[j][0]][L[j][1]] for j in range(i+1)) >= terminator[1]).OnlyEnforceIf(termBools[i])
					c = self.model.NewBoolVar('switch')
					self.model.Add(sum(self.cellValues[L[j][0]][L[j][1]] for j in range(i)) >= terminator[1]).OnlyEnforceIf([c,termBools[i].Not()])
					self.model.Add(sum(self.cellValues[L[j][0]][L[j][1]] for j in range(i+1)) < terminator[1]).OnlyEnforceIf([c.Not(),termBools[i].Not()])
					self.model.AddBoolAnd(c).OnlyEnforceIf(termBools[i])
			case 'DigitReached':
				for i in range(len(L)):
					self.model.Add(self.cellValues[L[i][0]][L[i][1]] == terminator[1]).OnlyEnforceIf(termBools[i])
					self.model.Add(self.cellValues[L[i][0]][L[i][1]] != terminator[1]).OnlyEnforceIf(termBools[i].Not())
			case 'DigitSetReached':
				instanceCount = [self.model.NewIntVar(0,len(L),'digitInstanceCount') for j in range(len(L))]
				isInstance = [self.model.NewBoolVar('digitInstanceTest') for j in range(len(L))]
				self.allVars = self.allVars + instanceCount + isInstance
				for i in range(len(L)):
					digitVars = [self.model.NewBoolVar('digitPicker') for j in range(len(terminator[1]))]
					self.allVars = self.allVars + digitVars
					for j in range(len(terminator[1])):
						self.model.Add(self.cellValues[L[i][0]][L[i][1]] == terminator[1][j]).OnlyEnforceIf(digitVars[j])
						self.model.Add(self.cellValues[L[i][0]][L[i][1]] != terminator[1][j]).OnlyEnforceIf(digitVars[j].Not())
						self.model.AddBoolAnd(isInstance[i]).OnlyEnforceIf(digitVars[j])
					self.model.AddBoolAnd(isInstance[i].Not()).OnlyEnforceIf([digitVars[j].Not() for j in range(len(terminator[1]))])
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf(isInstance[0])
				self.model.Add(instanceCount[0] == 0).OnlyEnforceIf(isInstance[0].Not())
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i] == instanceCount[i-1]+1).OnlyEnforceIf(isInstance[i])
					self.model.Add(instanceCount[i] == instanceCount[i-1]).OnlyEnforceIf(isInstance[i].Not())
				self.model.Add(instanceCount[0] == terminator[2]).OnlyEnforceIf(termBools[0])
				self.model.Add(instanceCount[0] < terminator[2]).OnlyEnforceIf(termBools[0].Not())
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i-1] < terminator[2]).OnlyEnforceIf(termBools[i])
					self.model.Add(instanceCount[i] == terminator[2]).OnlyEnforceIf(termBools[i])
					c = self.model.NewBoolVar('switch')
					self.allVars = self.allVars + [c]
					self.model.Add(instanceCount[i-1] >= terminator[2]).OnlyEnforceIf([c,termBools[i].Not()])
					self.model.Add(instanceCount[i] < terminator[2]).OnlyEnforceIf([c.Not(),termBools[i].Not()])
					self.model.AddBoolAnd(c).OnlyEnforceIf(termBools[i])
			case 'ParityChangeReached' | 'EntropyChangeReached' | 'ModularChangeReached' | 'PrimalityChangeReached' | 'ParityRepeatReached' | 'EntropyRepeatReached' | 'ModularRepeatReached' | 'PrimalityRepeatReached':
				if terminator[0][0:-13] not in self._propertyInitialized:
					getattr(self,'_set'+terminator[0][0:-13])()
				myTransition = terminator[0][-13:-7] # 'Change' or 'Repeat'
				instanceCount = [self.model.NewIntVar(0,len(L),terminator[0][0:-13]+'ChangeInstanceCount') for j in range(len(L))]
				isInstance = [self.model.NewBoolVar(terminator[0][0:-13]+'ChangeInstanceTest') for j in range(len(L))]
				self.allVars = self.allVars + instanceCount + isInstance
				self.model.AddBoolAnd(isInstance[0].Not())  # first cell cannot be a change
				myCells = getattr(self,'cell'+terminator[0][0:-13])
				for i in range(1,len(L)):
					if myTransition == 'Change':
						self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf(isInstance[i])
						self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf(isInstance[i].Not())
					elif myTransition == 'Repeat':
						self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf(isInstance[i])
						self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf(isInstance[i].Not())
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf(isInstance[0])
				self.model.Add(instanceCount[0] == 0).OnlyEnforceIf(isInstance[0].Not())
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i] == instanceCount[i-1]+1).OnlyEnforceIf(isInstance[i])
					self.model.Add(instanceCount[i] == instanceCount[i-1]).OnlyEnforceIf(isInstance[i].Not())
				self.model.Add(instanceCount[0] == terminator[1]).OnlyEnforceIf(termBools[0])
				self.model.Add(instanceCount[0] < terminator[1]).OnlyEnforceIf(termBools[0].Not())
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i-1] < terminator[1]).OnlyEnforceIf(termBools[i])
					self.model.Add(instanceCount[i] == terminator[1]).OnlyEnforceIf(termBools[i])
					c = self.model.NewBoolVar('switch')
					self.allVars = self.allVars + [c]
					self.model.Add(instanceCount[i-1] >= terminator[1]).OnlyEnforceIf([c,termBools[i].Not()])
					self.model.Add(instanceCount[i] < terminator[1]).OnlyEnforceIf([c.Not(),termBools[i].Not()])
					self.model.AddBoolAnd(c).OnlyEnforceIf(termBools[i])
			case 'Indexed':
				if type(terminator[1]) is int:
					depthIndices = [terminator[1]-1]
				else:
					depthIndices = [x-1 for x in terminator[1]]
				depthVars = [self.model.NewBoolVar('TerminationSelectionCellRow') for j in range(len(depthIndices))]
				self.allVars = self.allVars + depthVars
				self.model.AddBoolOr(depthVars)

				for i in range(len(L)):
					for j in range(len(depthVars)):
						self.model.Add(self.cellValues[L[depthIndices[j]][0]][L[depthIndices[j]][1]] == i+1).OnlyEnforceIf([termBools[i], depthVars[j]])
						self.model.Add(self.cellValues[L[depthIndices[j]][0]][L[depthIndices[j]][1]] != i+1).OnlyEnforceIf([termBools[i], depthVars[j].Not()])
						
				if len(terminator) > 2:
					if terminator[2]== 'Smallest':
						for j in range(len(depthIndices)):
							for k in range(len(depthIndices)):
								if k != j:
									self.model.Add(self.cellValues[L[depthIndices[j]][0]][L[depthIndices[j]][1]] < self.cellValues[L[depthIndices[k]][0]][L[depthIndices[k]][1]]).OnlyEnforceIf(depthVars[j])
					elif terminator[2] == 'Largest':
						for j in range(len(depthIndices)):
							for k in range(len(depthIndices)):
								if k != j:
									self.model.Add(self.cellValues[L[depthIndices[j]][0]][L[depthIndices[j]][1]] > self.cellValues[L[depthIndices[k]][0]][L[depthIndices[k]][1]]).OnlyEnforceIf(depthVars[j])
			case 'RepeatReached':
				isRepeat = [self.model.NewBoolVar('TerminationRepeatReachedTest') for j in range(len(L))]
				repeatCount = [self.model.NewIntVar(0,len(L),'TerminationRepeatReachedCount') for j in range(len(L))]
				self.model.AddBoolAnd(isRepeat[0].Not())
				self.model.Add(repeatCount[0] == 0)
				self.model.AddBoolAnd(termBools[0].Not())

				if terminator[1] == 'Last':
					myTarget = self.model.NewIntVar(0,len(L),'TerminationRepeatReachedMaxCount')
					self.model.AddMaxEquality(myTarget,repeatCount)
				else:
					myTarget = terminator[1]
				
				for j in range(1,len(L)):
					isEqual = [self.model.NewBoolVar('TerminationRepeatReachedEqualityChecker') for k in range(j)]
					for k in range(j):
						self.model.Add(self.cellValues[L[k][0]][L[k][1]] == self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf(isEqual[k])
						self.model.Add(self.cellValues[L[k][0]][L[k][1]] != self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf(isEqual[k].Not())
					self.model.AddBoolOr(isEqual).OnlyEnforceIf(isRepeat[j])
					self.model.AddBoolAnd([x.Not() for x in isEqual]).OnlyEnforceIf(isRepeat[j].Not())
					self.model.Add(repeatCount[j] == repeatCount[j-1]+1).OnlyEnforceIf(isRepeat[j])
					self.model.Add(repeatCount[j] == repeatCount[j-1]).OnlyEnforceIf(isRepeat[j].Not())
				
					self.model.Add(repeatCount[j] == myTarget).OnlyEnforceIf(termBools[j])
					self.model.AddBoolAnd(isRepeat[j]).OnlyEnforceIf(termBools[j])
					self.model.Add(repeatCount[j] != myTarget).OnlyEnforceIf([termBools[j].Not(),isRepeat[j]])
			case 'RelatedDigit':
				base = terminator[1]-1
				comparator = terminator[2]
				scale = terminator[3]
				shift = terminator[4]
				instance = terminator[5]
				
				instanceCount = [self.model.NewIntVar(0,len(L),'RelatedDigitInstanceCount') for j in range(len(L))]
				isInstance = [self.model.NewBoolVar('RelatedDigitInstanceTest') for j in range(len(L))]
				
				for i in range(len(L)):
					match comparator:
						case self.LE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] <= scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf(isInstance[i])
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] > scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf(isInstance[i].Not())
						case self.EQ:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] == scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf(isInstance[i])
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] != scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf(isInstance[i].Not())
						case self.GE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] >= scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf(isInstance[i])
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] < scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf(isInstance[i].Not())
						case self.NE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] != scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf(isInstance[i])
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] == scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf(isInstance[i].Not())
							
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf(isInstance[0])
				self.model.Add(instanceCount[0] == 0).OnlyEnforceIf(isInstance[0].Not())
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i] == instanceCount[i-1] + 1).OnlyEnforceIf(isInstance[i])
					self.model.Add(instanceCount[i] == instanceCount[i-1]).OnlyEnforceIf(isInstance[i].Not())
					
				if instance == 1:
					self.model.AddBoolAnd(termBools[0]).OnlyEnforceIf(isInstance[0])
					self.model.AddBoolAnd(termBools[0].Not()).OnlyEnforceIf(isInstance[0].Not())
				else:
					self.model.AddBoolAnd(termBools[0].Not())
				
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i] == instance).OnlyEnforceIf(termBools[i])
					self.model.AddBoolAnd(isInstance[i]).OnlyEnforceIf(termBools[i])
					self.model.Add(instanceCount[i] != instance).OnlyEnforceIf([termBools[i].Not(),isInstance[i]])
			case 'ModelVariable':
				for i in range(len(L)):
					self.model.Add(terminator[1] == i+1).OnlyEnforceIf(termBools[i])
					self.model.Add(terminator[1] != i+1).OnlyEnforceIf(termBools[i].Not())
									
		terminatorBools.insert(terminatorNumber,termBools)
		terminatorNumber = terminatorNumber + 1
	
	# For each terminator cell, need only one of the criteria below it to be true, so it could terminate here.
	for i in range(len(L)):
		self.model.AddBoolOr([terminatorBools[j][i] for j in range(len(terminatorBools))]).OnlyEnforceIf(terminatorCells[i])
		self.model.AddBoolAnd([terminatorBools[j][i].Not() for j in range(len(terminatorBools))]).OnlyEnforceIf(terminatorCells[i].Not())
		
	return terminatorCells
	
def _terminateCellsInRowCol(self,row,col,rc,selectTerminator):
	
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	L = [(row+i*vStep,col+i*hStep) for i in range(self.boardWidth)]
	terminatorCells = self._terminateCellsOnLine(L,selectTerminator)
	return terminatorCells
	
def _evaluateHangingClues(self,partial,terminatorCells,value,terminateOn,includeTerminator,comparator=None,forceTermination=True):
	# This does the final configuration of a hanging clue, just extracting the ugly stuff away from the individual functions
	
	if forceTermination == True:
		# One of the existing cells must terminate per the specified conditions
		self.model.AddBoolOr(terminatorCells)
	elif type(forceTermination) is list:
		# Only force termination if the associated list of Bools is true
		self.model.AddBoolOr(terminatorCells).OnlyEnforceIf(forceTermination)
	else:
		# Otherwise we create a new final terminator as a default. If any other terminators are true, we want
		# this to be false, but otherwise it becomes true.
		newFinalTerminator = self.model.NewBoolVar('AlternateTerminator')
		self.allVars.append(newFinalTerminator)
		self.model.AddBoolAnd(newFinalTerminator).OnlyEnforceIf([x.Not() for x in terminatorCells])
		for x in terminatorCells:
			self.model.AddBoolAnd(newFinalTerminator.Not()).OnlyEnforceIf(x)
		
		if includeTerminator:
			# If we're including the terminator in the count or sum, we need to *replace* the current
			# final terminator in terminator cells, since its value no longer accurately determines
			# whether or not we can actually terminate there
			terminatorCells[-1] = newFinalTerminator
		else:
			# We are not including the terminator cell in the count or sum, but there is no
			# terminator. So we should include all of the cells in the sum/count. This means we need
			# to *append* the newFinalTerminator, allowing the possibility that the last cell of the line
			# could be added, if it's not a *real* terminator.
			terminatorCells.append(newFinalTerminator)
		
	if terminateOn == 'First':
		if includeTerminator:
			self.model.Add(partial[0] == value).OnlyEnforceIf(terminatorCells[0])
		else:
			if type(value) is int and value == 0:
				pass
			else:
				self.model.AddBoolAnd(terminatorCells[0].Not()).OnlyEnforceIf(terminatorCells[0])
		# Note: we are changing the loop limits to range over terminatorCells, since if includeTerminator is 
		# False and forceTermination is False, terminatorCells may be one longer than partial. However, in
		# this case, there is no risk of over-running partial, since we'll be in the "else" clause below,
		# where the indices are one less that the 
		for i in range(1,len(terminatorCells)):
			if includeTerminator:
				match comparator:
					case self.LE:
						self.model.Add(partial[i] <= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
					case self.GE:
						self.model.Add(partial[i] >= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
					case self.NE:
						self.model.Add(partial[i] != value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
					case _:
						self.model.Add(partial[i] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
			else:
				match comparator:
					case self.LE:
						self.model.Add(partial[i-1] <= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
					case self.GE:
						self.model.Add(partial[i-1] >= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
					case self.NE:
						self.model.Add(partial[i-1] != value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
					case _:
						self.model.Add(partial[i-1] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
	elif terminateOn == 'Last':
		for i in range(len(terminatorCells)):
			if includeTerminator:
				match comparator:
					case self.LE:
						self.model.Add(partial[i] <= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))])
					case self.GE:
						self.model.Add(partial[i] >= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))])
					case self.NE:
						self.model.Add(partial[i] != value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))])
					case _:
						self.model.Add(partial[i] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))])
			else:
				match comparator:
					case self.LE:
						self.model.Add(partial[i-1] <= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))])
					case self.GE:
						self.model.Add(partial[i-1] >= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))])
					case self.NE:
						self.model.Add(partial[i-1] != value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))])
					case _:
						self.model.Add(partial[i-1] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))])
				
	else:
		# OK, what the heck is going on here? I want to allow for the possibility that any place that provides a possible 
		# termination point could be chosen, so terminateOn is 'Any'. Hence the varBitmap to pick. However. I want to ensure the solution is unique, so
		# I want to make sure to pick the *first* location which meets the condition. I actually don't care which, just need to
		# be canonical. The for j loop below ensures that if there is an earlier terminator that *could* be chosen, this
		# one cannot be.
		varBitmap = self._varBitmap('terminationPicker',len(terminatorCells))
		self.allVars = self.allVars + varBitmap[0]
		for i in range(len(terminatorCells)):
			if includeTerminator:
				match comparator:
					case self.LE:
						self.model.Add(partial[i] <= value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]])
					case self.GE:
						self.model.Add(partial[i] >= value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]])
					case self.NE:
						self.model.Add(partial[i] != value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]])
					case _:
						self.model.Add(partial[i] == value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]])
			else:
				match comparator:
					case self.LE:
						self.model.Add(partial[i-1] <= value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]])
					case self.GE:
						self.model.Add(partial[i-1] >= value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]])
					case self.NE:
						self.model.Add(partial[i-1] != value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]])
					case _:
						self.model.Add(partial[i-1] == value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]])
						
			self.model.AddBoolAnd(terminatorCells[i]).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i].Not()])
			  # ensures this varBitmap cannot be chosen if terminatorCells is not set
			for j in range(i):
				c = self.model.NewBoolVar('solutionPickerSwitch')
				self.allVars = self.allVars + [c]
				match comparator:
					case self.LE:
						self.model.Add(partial[j] > value).OnlyEnforceIf(varBitmap[i] + [c])
					case self.GE:
						self.model.Add(partial[j] < value).OnlyEnforceIf(varBitmap[i] + [c])
					case self.NE:
						self.model.Add(partial[j] == value).OnlyEnforceIf(varBitmap[i] + [c])
					case _:
						self.model.Add(partial[j] != value).OnlyEnforceIf(varBitmap[i] + [c])
				self.model.AddBoolAnd(terminatorCells[j].Not()).OnlyEnforceIf(varBitmap[i] + [c.Not()])
				self.model.AddBoolAnd(c.Not()).OnlyEnforceIf(varBitmap[i] + [terminatorCells[j].Not()])
				for k in range(len(terminatorCells)):
					if k != i:
						self.model.AddBoolAnd(c).OnlyEnforceIf(varBitmap[k])