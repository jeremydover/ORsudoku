import math

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
	return [(i+k,j+m) for k in [-1,0,1] for m in [-1,0,1] if i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth and abs(k) != abs(m)]
	
def _selectCellsInRowCol(self,row,col,rc,selectCriteria):
	
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	# Now I'm going to create selection Booleans to evaluate each cell against the selectCriteria criteria. 
	# Notice how I'm clever enough to avoid defining selectSummands as long as I can. #genius
	selectionCells = [self.model.NewBoolVar('SelectionCondition{:d}'.format(i)) for i in range(self.boardWidth)]
	
	# OK, document as I go! selectCriteria is an array of criteria, all of which must be true for a cell to be
	# selected. Each array element is itself a tuple of at least two items: property, value.
	# More than one value may be given, and depend on the property how they are interpreted
	# 
	# Property: 'Index'
	#   For this property, we are picking cells based on their position within the clued row/column.
	#   Values[0]: A comparator: use the class variables GE, EQ or LE, or NE if you really think that's useful
	#   Values[1]: index to stop
	#   So for example, ('Index',p.GE,4) would include all cells in the two boxes not adjacent to the clue. Yes, this is just a cage. I get it.
	#
	# Property: 'IndexSkip'
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

	criteriaBools = []
	criterionNumber = 0
	for criterion in selectCriteria:
		criterionBools = [self.model.NewBoolVar('Criterion{:d}{:d}'.format(criterionNumber,i)) for i in range(self.boardWidth)]
		self.allVars = self.allVars + criterionBools
		match criterion[0]:
			case 'Location':
				match criterion[1]:
					case self.LE:
						self.model.AddBoolAnd([criterionBools[j] for j in range(criterion[2])])
						self.model.AddBoolAnd([criterionBools[j].Not() for j in range(criterion[2],self.boardWidth)])
					case self.EQ:
						self.model.AddBoolAnd([criterionBools[criterion[2]]])
						self.model.AddBoolAnd([criterionBools[j].Not() for j in range(self.boardWidth) if j != criterion[2]])
					case self.GE:
						self.model.AddBoolAnd([criterionBools[j].Not() for j in range(criterion[2]-1)])
						self.model.AddBoolAnd([criterionBools[j] for j in range(criterion[2]-1,self.boardWidth)])
					case self.NE:
						self.model.AddBoolAnd([criterionBools[criterion[2]].Not()])
						self.model.AddBoolAnd([criterionBools[j] for j in range(self.boardWidth) if j != criterion[2]])
			
			case 'LocationSkip':
				self.model.AddBoolAnd([criterionBools[j] for j in range(self.boardWidth) if (j % criterion[1]) == criterion[2]])
				self.model.AddBoolAnd([criterionBools[j].Not() for j in range(self.boardWidth) if (j % criterion[1]) != criterion[2]])
				
			case 'Magnitude':
				for i in range(self.boardWidth):
					match criterion[1]:
						case self.LE:
							self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] <= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] > criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.EQ:
							self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] != criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.GE:
							self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] >= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] < criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.NE:
							self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] != criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
			
			case 'Parity':
				if 'Parity' not in self._propertyInitialized:
					self._setParity()
				if len(criterion) == 2:
					target = criterion[1]
				else:
					target = criterion[2]
				for i in range(self.boardWidth):
					self.model.Add(self.cellParity[row+i*vStep][col+i*hStep] == target).OnlyEnforceIf(criterionBools[i])
					self.model.Add(self.cellParity[row+i*vStep][col+i*hStep] != target).OnlyEnforceIf(criterionBools[i].Not())

			case 'MatchParity':
				if 'Parity' not in self._propertyInitialized:
					self._setParity()
				mCell = criterion[1] - 1
				for i in range(self.boardWidth):
					self.model.Add(self.cellParity[row+i*vStep][col+i*hStep] == self.cellParity[row+mCell*vStep][col+mCell*hStep]).OnlyEnforceIf(criterionBools[i])
					self.model.Add(self.cellParity[row+i*vStep][col+i*hStep] != self.cellParity[row+mCell*vStep][col+mCell*hStep]).OnlyEnforceIf(criterionBools[i].Not())
			
			case 'Entropy':
				if 'Entropy' not in self._propertyInitialized:
					self._setEntropy()
				for i in range(self.boardWidth):
					match criterion[1]:
						case self.LE:
							self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] <= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] > criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.EQ:
							self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] == criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] != criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.GE:
							self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] >= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] < criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.NE:
							self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] != criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] == criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
			
			case 'MatchEntropy':
				if 'Entropy' not in self._propertyInitialized:
					self._setEntropy()
				mCell = criterion[1] - 1
				for i in range(self.boardWidth):
					self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] == self.cellEntropy[row+mCell*vStep][col+mCell*hStep]).OnlyEnforceIf(criterionBools[i])
					self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] != self.cellEntropy[row+mCell*vStep][col+mCell*hStep]).OnlyEnforceIf(criterionBools[i].Not())

			case 'Modular':
				if 'Modular' not in self._propertyInitialized:
					self._setModular()
				for i in range(self.boardWidth):
					match criterion[1]:
						case self.LE:
							self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] <= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] > criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.EQ:
							self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] == criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] != criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.GE:
							self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] >= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] < criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.NE:
							self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] != criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] == criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
							
			case 'MatchModular':
				if 'Modular' not in self._propertyInitialized:
					self._setModular()
				mCell = criterion[1] - 1
				for i in range(self.boardWidth):
					self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] == self.cellModular[row+mCell*vStep][col+mCell*hStep]).OnlyEnforceIf(criterionBools[i])
					self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] != self.cellModular[row+mCell*vStep][col+mCell*hStep]).OnlyEnforceIf(criterionBools[i].Not())
			
			case 'Primality':
				if 'Primality' not in self._propertyInitialized:
					self._setPrimality()
				for i in range(self.boardWidth):
					match criterion[1]:
						case self.LE:
							self.model.Add(self.cellPrimality[row+i*vStep][col+i*hStep] <= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellPrimality[row+i*vStep][col+i*hStep] > criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.EQ:
							self.model.Add(self.cellPrimality[row+i*vStep][col+i*hStep] == criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellPrimality[row+i*vStep][col+i*hStep] != criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.GE:
							self.model.Add(self.cellPrimality[row+i*vStep][col+i*hStep] >= criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellPrimality[row+i*vStep][col+i*hStep] < criterion[2]).OnlyEnforceIf(criterionBools[i].Not())
						case self.NE:
							self.model.Add(self.cellPrimality[row+i*vStep][col+i*hStep] != criterion[2]).OnlyEnforceIf(criterionBools[i])
							self.model.Add(self.cellPrimality[row+i*vStep][col+i*hStep] == criterion[2]).OnlyEnforceIf(criterionBools[i].Not())	
							
			case 'DigitSet':
				for i in range(self.boardWidth):
					for j in self.digits:
						if j in criterion[1]:
							self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] != j).OnlyEnforceIf(criterionBools[i].Not())
						else:
							self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] != j).OnlyEnforceIf(criterionBools[i])
							
			case 'BeforeDigit':
				self.model.Add(self.cellValues[row][col] != criterion[1]).OnlyEnforceIf(criterionBools[0])
				self.model.Add(self.cellValues[row][col] == criterion[1]).OnlyEnforceIf(criterionBools[0].Not())
				for i in range(1,self.boardWidth):
					self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] != criterion[1]).OnlyEnforceIf(criterionBools[i])
					self.model.AddBoolAnd(criterionBools[i-1]).OnlyEnforceIf(criterionBools[i])
					for j in range(i+1,self.boardWidth):
						self.model.Add(self.cellValues[row+j*vStep][col+j*hStep] != criterion[1]).OnlyEnforceIf(criterionBools[i].Not())

			case 'AfterDigit':
				self.model.Add(self.cellValues[row+(self.boardWidth-1)*vStep][col+(self.boardWidth-1)*hStep] != criterion[1]).OnlyEnforceIf(criterionBools[-1])
				self.model.Add(self.cellValues[row+(self.boardWidth-1)*vStep][col+(self.boardWidth-1)*hStep] == criterion[1]).OnlyEnforceIf(criterionBools[-1].Not())
				for i in range(self.boardWidth-1):
					self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] != criterion[1]).OnlyEnforceIf(criterionBools[i])
					self.model.AddBoolAnd(criterionBools[i+1]).OnlyEnforceIf(criterionBools[i])
					for j in range(i):
						self.model.Add(self.cellValues[row+j*vStep][col+j*hStep] != criterion[1]).OnlyEnforceIf(criterionBools[i].Not())
										
		criteriaBools.insert(criterionNumber,criterionBools)
		criterionNumber = criterionNumber + 1
	
	# Ensure selectionCells[i] is True if and only if each of the underlying criteria is
	for i in range(self.boardWidth):
		self.model.AddBoolAnd([criteriaBools[j][i] for j in range(len(criteriaBools))]).OnlyEnforceIf(selectionCells[i])
		self.model.AddBoolOr([criteriaBools[j][i].Not() for j in range(len(criteriaBools))]).OnlyEnforceIf(selectionCells[i].Not())
		
	return selectionCells
	
def _terminateCellsInRowCol(self,row,col,rc,selectTerminator):
	
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
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
	
	terminatorCells = [self.model.NewBoolVar('HangingSumTermination{:d}'.format(i)) for i in range(self.boardWidth)]
	self.allVars = self.allVars + terminatorCells
	terminatorBools = []
	terminatorNumber = 0
	for terminator in selectTerminator:
		termBools = [self.model.NewBoolVar('TermCriterion{:d}{:d}'.format(terminatorNumber,i)) for i in range(self.boardWidth)]
		self.allVars = self.allVars + termBools
		match terminator[0]:
			case 'Fixed':
				self.model.AddBoolAnd(termBools[terminator[1]-1])
				self.model.AddBoolAnd([termBools[j].Not() for j in range(self.boardWidth) if j != terminator[1]-1])
			case 'SumReached':
				self.model.Add(partialSum[0] >= terminator[1]).OnlyEnforceIf(termBools[0])
				self.model.Add(partialSum[0] < terminator[1]).OnlyEnforceIf(termBools[0].Not())
				for i in range(1,self.boardWidth):
					self.model.Add(partialSum[i-1] < terminator[1]).OnlyEnforceIf(termBools[i])
					self.model.Add(partialSum[i] >= terminator[1]).OnlyEnforceIf(termBools[i])
					c = self.model.NewBoolVar('switch')
					self.model.Add(partialSum[i-1] >= terminator[1]).OnlyEnforceIf([c,termBools[i].Not()])
					self.model.Add(partialSum[i] < terminator[1]).OnlyEnforceIf([c.Not(),termBools[i].Not()])
					self.model.AddBoolAnd(c).OnlyEnforceIf(termBools[i])
			case 'DigitReached':
				for i in range(self.boardWidth):
					self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == terminator[1]).OnlyEnforceIf(termBools[i])
					self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] != terminator[1]).OnlyEnforceIf(termBools[i].Not())
			case 'DigitSetReached':
				instanceCount = [self.model.NewIntVar(0,self.boardWidth,'digitInstanceCount') for j in range(self.boardWidth)]
				isInstance = [self.model.NewBoolVar('digitInstanceTest') for j in range(self.boardWidth)]
				self.allVars = self.allVars + instanceCount + isInstance
				for i in range(self.boardWidth):
					digitVars = [self.model.NewBoolVar('digitPicker') for j in range(len(terminator[1]))]
					self.allVars = self.allVars + digitVars
					for j in range(len(terminator[1])):
						self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == terminator[1][j]).OnlyEnforceIf(digitVars[j])
						self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] != terminator[1][j]).OnlyEnforceIf(digitVars[j].Not())
						self.model.AddBoolAnd(isInstance[i]).OnlyEnforceIf(digitVars[j])
					self.model.AddBoolAnd(isInstance[i].Not()).OnlyEnforceIf([digitVars[j].Not() for j in range(len(terminator[1]))])
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf(isInstance[0])
				self.model.Add(instanceCount[0] == 0).OnlyEnforceIf(isInstance[0].Not())
				for i in range(1,self.boardWidth):
					self.model.Add(instanceCount[i] == instanceCount[i-1]+1).OnlyEnforceIf(isInstance[i])
					self.model.Add(instanceCount[i] == instanceCount[i-1]).OnlyEnforceIf(isInstance[i].Not())
				self.model.Add(instanceCount[0] == terminator[2]).OnlyEnforceIf(termBools[0])
				self.model.Add(instanceCount[0] < terminator[2]).OnlyEnforceIf(termBools[0].Not())
				for i in range(1,self.boardWidth):
					self.model.Add(instanceCount[i-1] < terminator[2]).OnlyEnforceIf(termBools[i])
					self.model.Add(instanceCount[i] == terminator[2]).OnlyEnforceIf(termBools[i])
					c = self.model.NewBoolVar('switch')
					self.allVars = self.allVars + [c]
					self.model.Add(instanceCount[i-1] >= terminator[2]).OnlyEnforceIf([c,termBools[i].Not()])
					self.model.Add(instanceCount[i] < terminator[2]).OnlyEnforceIf([c.Not(),termBools[i].Not()])
					self.model.AddBoolAnd(c).OnlyEnforceIf(termBools[i])
			case 'ParityChangeReached':
				if 'Parity' not in self._propertyInitialized:
					self._setParity()
				instanceCount = [self.model.NewIntVar(0,self.boardWidth,'parityChangeInstanceCount') for j in range(self.boardWidth)]
				isInstance = [self.model.NewBoolVar('parityChangeInstanceTest') for j in range(self.boardWidth)]
				self.allVars = self.allVars + instanceCount + isInstance
				self.model.AddBoolAnd(isInstance[0].Not())  # first cell cannot be a change
				for i in range(1,self.boardWidth):
					self.model.Add(self.cellParity[row+i*vStep][col+i*hStep] != self.cellParity[row+(i-1)*vStep][col+(i-1)*hStep]).OnlyEnforceIf(isInstance[i])
					self.model.Add(self.cellParity[row+i*vStep][col+i*hStep] == self.cellParity[row+(i-1)*vStep][col+(i-1)*hStep]).OnlyEnforceIf(isInstance[i].Not())
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf(isInstance[0])
				self.model.Add(instanceCount[0] == 0).OnlyEnforceIf(isInstance[0].Not())
				for i in range(1,self.boardWidth):
					self.model.Add(instanceCount[i] == instanceCount[i-1]+1).OnlyEnforceIf(isInstance[i])
					self.model.Add(instanceCount[i] == instanceCount[i-1]).OnlyEnforceIf(isInstance[i].Not())
				self.model.Add(instanceCount[0] == terminator[1]).OnlyEnforceIf(termBools[0])
				self.model.Add(instanceCount[0] < terminator[1]).OnlyEnforceIf(termBools[0].Not())
				for i in range(1,self.boardWidth):
					self.model.Add(instanceCount[i-1] < terminator[1]).OnlyEnforceIf(termBools[i])
					self.model.Add(instanceCount[i] == terminator[1]).OnlyEnforceIf(termBools[i])
					c = self.model.NewBoolVar('switch')
					self.allVars = self.allVars + [c]
					self.model.Add(instanceCount[i-1] >= terminator[1]).OnlyEnforceIf([c,termBools[i].Not()])
					self.model.Add(instanceCount[i] < terminator[1]).OnlyEnforceIf([c.Not(),termBools[i].Not()])
					self.model.AddBoolAnd(c).OnlyEnforceIf(termBools[i])
			case 'EntropyChangeReached':
				if 'Entropy' not in self._propertyInitialized:
					self._setEntropy()
				instanceCount = [self.model.NewIntVar(0,self.boardWidth,'entropyChangeInstanceCount') for j in range(self.boardWidth)]
				isInstance = [self.model.NewBoolVar('entropyChangeInstanceTest') for j in range(self.boardWidth)]
				self.allVars = self.allVars + instanceCount + isInstance
				self.model.AddBoolAnd(isInstance[0].Not())  # first cell cannot be a change
				for i in range(1,self.boardWidth):
					self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] != self.cellEntropy[row+(i-1)*vStep][col+(i-1)*hStep]).OnlyEnforceIf(isInstance[i])
					self.model.Add(self.cellEntropy[row+i*vStep][col+i*hStep] == self.cellEntropy[row+(i-1)*vStep][col+(i-1)*hStep]).OnlyEnforceIf(isInstance[i].Not())
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf(isInstance[0])
				self.model.Add(instanceCount[0] == 0).OnlyEnforceIf(isInstance[0].Not())
				for i in range(1,self.boardWidth):
					self.model.Add(instanceCount[i] == instanceCount[i-1]+1).OnlyEnforceIf(isInstance[i])
					self.model.Add(instanceCount[i] == instanceCount[i-1]).OnlyEnforceIf(isInstance[i].Not())
				self.model.Add(instanceCount[0] == terminator[1]).OnlyEnforceIf(termBools[0])
				self.model.Add(instanceCount[0] < terminator[1]).OnlyEnforceIf(termBools[0].Not())
				for i in range(1,self.boardWidth):
					self.model.Add(instanceCount[i-1] < terminator[1]).OnlyEnforceIf(termBools[i])
					self.model.Add(instanceCount[i] == terminator[1]).OnlyEnforceIf(termBools[i])
					c = self.model.NewBoolVar('switch')
					self.allVars = self.allVars + [c]
					self.model.Add(instanceCount[i-1] >= terminator[1]).OnlyEnforceIf([c,termBools[i].Not()])
					self.model.Add(instanceCount[i] < terminator[1]).OnlyEnforceIf([c.Not(),termBools[i].Not()])
					self.model.AddBoolAnd(c).OnlyEnforceIf(termBools[i])
			case 'ModularChangeReached':
				if 'Modular' not in self._propertyInitialized:
					self._setModular()
				instanceCount = [self.model.NewIntVar(0,self.boardWidth,'modularChangeInstanceCount') for j in range(self.boardWidth)]
				isInstance = [self.model.NewBoolVar('modularChangeInstanceTest') for j in range(self.boardWidth)]
				self.allVars = self.allVars + instanceCount + isInstance
				self.model.AddBoolAnd(isInstance[0].Not())  # first cell cannot be a change
				for i in range(1,self.boardWidth):
					self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] != self.cellModular[row+(i-1)*vStep][col+(i-1)*hStep]).OnlyEnforceIf(isInstance[i])
					self.model.Add(self.cellModular[row+i*vStep][col+i*hStep] == self.cellModular[row+(i-1)*vStep][col+(i-1)*hStep]).OnlyEnforceIf(isInstance[i].Not())
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf(isInstance[0])
				self.model.Add(instanceCount[0] == 0).OnlyEnforceIf(isInstance[0].Not())
				for i in range(1,self.boardWidth):
					self.model.Add(instanceCount[i] == instanceCount[i-1]+1).OnlyEnforceIf(isInstance[i])
					self.model.Add(instanceCount[i] == instanceCount[i-1]).OnlyEnforceIf(isInstance[i].Not())
				
				self.model.Add(instanceCount[0] == terminator[1]).OnlyEnforceIf(termBools[0])
				self.model.Add(instanceCount[0] < terminator[1]).OnlyEnforceIf(termBools[0].Not())
				for i in range(1,self.boardWidth):
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
				self.model.AddBoolOr(depthVars)
				self.model.AddBoolOr(termBools)

				for i in range(self.boardWidth):
					for j in range(len(depthVars)):
						self.model.Add(self.cellValues[row+depthIndices[j]*vStep][col+depthIndices[j]*hStep] == i+1).OnlyEnforceIf([termBools[i], depthVars[j]])
						self.model.Add(self.cellValues[row+depthIndices[j]*vStep][col+depthIndices[j]*hStep] != i+1).OnlyEnforceIf([termBools[i], depthVars[j].Not()])
						
				if len(terminator) > 2:
					if terminator[2]== 'Smallest':
						for j in range(len(depthIndices)):
							for k in range(len(depthIndices)):
								if k != j:
									self.model.Add(self.cellValues[row+depthIndices[j]*vStep][col+depthIndices[j]*hStep] < self.cellValues[row+depthIndices[k]*vStep][col+depthIndices[k]*hStep]).OnlyEnforceIf(depthVars[j])
					elif terminator[2] == 'Largest':
						for j in range(len(depthIndices)):
							for k in range(len(depthIndices)):
								if k != j:
									self.model.Add(self.cellValues[row+depthIndices[j]*vStep][col+depthIndices[j]*hStep] > self.cellValues[row+depthIndices[k]*vStep][col+depthIndices[k]*hStep]).OnlyEnforceIf(depthVars[j])
					
		terminatorBools.insert(terminatorNumber,termBools)
		terminatorNumber = terminatorNumber + 1
	
	# For each terminator cell, need only one of the criteria below it to be true, so it could terminate here.
	for i in range(self.boardWidth):
		self.model.AddBoolOr([terminatorBools[j][i] for j in range(len(terminatorBools))]).OnlyEnforceIf(terminatorCells[i])
		self.model.AddBoolAnd([terminatorBools[j][i].Not() for j in range(len(terminatorBools))]).OnlyEnforceIf(terminatorCells[i].Not())
		
	# Ensure some terminator cell is picked
	self.model.AddBoolOr(terminatorCells)
	
	return terminatorCells
	
def _evaluateHangingClues(self,partial,terminatorCells,value,terminateOnFirst,includeTerminator):
	# This does the final configuration of a hanging clue, just extracting the ugly stuff away from the individual functions
	if terminateOnFirst:
		if includeTerminator:
			self.model.Add(partial[0] == value).OnlyEnforceIf(terminatorCells[0])
		else:
			if value == 0:
				pass
			else:
				self.model.AddBoolAnd(terminatorCells[0].Not()).OnlyEnforceIf(terminatorCells[0])
		for i in range(1,self.boardWidth):
			if includeTerminator:
				self.model.Add(partial[i] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
			else:
				self.model.Add(partial[i-1] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
	else:
		# OK, what the heck is going on here? I want to allow for the possibility that any place that provides a possible 
		# termination point could be chosen. Hence the varBitmap to pick. However. I want to ensure the solution is unique, so
		# I want to make sure to pick the *first* location which meets the condition. I actually don't care which, just need to
		# be canonical. The for j loop below ensures that if there is an earlier terminator that *could* be chosen, this
		# one cannot be.
		varBitmap = self._varBitmap('terminationPicker',self.boardWidth)
		self.allVars = self.allVars + varBitmap[0]
		for i in range(self.boardWidth):
			self.model.Add(partial[i] == value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]])
			self.model.AddBoolAnd(terminatorCells[i]).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i].Not()])
			  # ensures this varBitmap cannot be chosen if terminatorCells is not set
			for j in range(i):
				c = self.model.NewBoolVar('solutionPickerSwitch')
				self.allVars = self.allVars + [c]
				self.model.Add(partial[j] != value).OnlyEnforceIf(varBitmap[i] + [c])
				self.model.AddBoolAnd(terminatorCells[j].Not()).OnlyEnforceIf(varBitmap[i] + [c.Not()])
				self.model.AddBoolAnd(c.Not()).OnlyEnforceIf(varBitmap[i] + [terminatorCells[j].Not()])
				for k in range(self.boardWidth):
					if k != i:
						self.model.AddBoolAnd(c).OnlyEnforceIf(varBitmap[k])