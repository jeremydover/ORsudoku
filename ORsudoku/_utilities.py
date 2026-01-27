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
	
def getRegion(self,row,col):
	return [i for i in range(len(self.regions)) if (row,col) in self.regions[i]][0]
	
def _initializeDigitTracking(self):
		if 'DigitTracking' not in self._propertyInitialized:
			self._setDigitTracking()

def _setDigitTracking(self):
	if 'DigitTracking' not in self._propertyInitialized:
		self._propertyInitialized.append('DigitTracking')
	self.cellDigitBools = [[None for _ in range(self.boardWidth)] for _ in range(self.boardWidth)]
	self.cellDigitInts = [[None for _ in range(self.boardWidth)] for _ in range(self.boardWidth)]
	self.digitList = sorted(self.digits)
	
def _initializeDigitTrackingCell(self,row,col):
	if self.cellDigitBools[row][col] is None:
		self.cellDigitBools[row][col] = [self.model.NewBoolVar('DigitTrackingBoolRow{:d}Col{:d}Digit{:d}'.format(row,col,self.digitList[i])) for i in range(len(self.digitList))]
		self.cellDigitInts[row][col] = [self.model.NewIntVar(0,1,'DigitTrackingIntRow{:d}Col{:d}Digit{:d}'.format(row,col,self.digitList[i])) for i in range(len(self.digitList))]
		for i in range(len(self.digitList)):
			self.model.Add(self.cellValues[row][col] == self.digitList[i]).OnlyEnforceIf(self.cellDigitBools[row][col][i])
			self.model.Add(self.cellValues[row][col] != self.digitList[i]).OnlyEnforceIf(self.cellDigitBools[row][col][i].Not())
			self.model.Add(self.cellDigitInts[row][col][i] == 1).OnlyEnforceIf(self.cellDigitBools[row][col][i])
			self.model.Add(self.cellDigitInts[row][col][i] == 0).OnlyEnforceIf(self.cellDigitBools[row][col][i].Not())

def _initializeParity(self):
	if 'Parity' not in self._propertyInitialized:
		self._setParity()

def _setParity(self):
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
		
	if 'VariableExteriorClues' in self._constraintInitialized:
		maxDiff = self.maxDigit*self.boardWidth - min(0,self.minDigit*self.boardWidth)
		for i in range(self.boardWidth):
			# Right column
			div = self.model.NewIntVar(0,2*maxDiff,'ParityDiv')
			mod = self.model.NewIntVar(0,1,'parityValue{:d}{:d}'.format(i,self.boardWidth))
			self.model.Add(2*div <= self.cellValues[i][self.boardWidth])
			self.model.Add(2*div+2 > self.cellValues[i][self.boardWidth])
			self.model.Add(mod == self.cellValues[i][self.boardWidth]-2*div)
			self.cellParity[i].append(mod)
			# Left column
			div = self.model.NewIntVar(0,2*maxDiff,'ParityDiv')
			mod = self.model.NewIntVar(0,1,'parityValue{:d}{:d}'.format(i,-1))
			self.model.Add(2*div <= self.cellValues[i][-1])
			self.model.Add(2*div+2 > self.cellValues[i][-1])
			self.model.Add(mod == self.cellValues[i][-1]-2*div)
			self.cellParity[i].append(mod)
		
		# Bottom row
		divs = [self.model.NewIntVar(0,2*maxDiff,'ParityDiv') for j in range(self.boardWidth+2)]
		mods = [self.model.NewIntVar(0,1,'parityValue{:d}{:d}'.format(i,self.boardWidth)) for j in range(self.boardWidth+2)]
		for j in range(self.boardWidth+2):
			self.model.Add(2*divs[j] <= self.cellValues[self.boardWidth][j])
			self.model.Add(2*divs[j]+2 > self.cellValues[self.boardWidth][j])
			self.model.Add(mods[j] == self.cellValues[self.boardWidth][j]-2*divs[j])
		self.cellParity.append(mods)
		# Top row
		divs = [self.model.NewIntVar(0,2*maxDiff,'ParityDiv') for j in range(self.boardWidth+2)]
		mods = [self.model.NewIntVar(0,1,'parityValue{:d}{:d}'.format(i,self.boardWidth)) for j in range(self.boardWidth+2)]
		for j in range(self.boardWidth+2):
			self.model.Add(2*divs[j] <= self.cellValues[-1][j])
			self.model.Add(2*divs[j]+2 > self.cellValues[-1][j])
			self.model.Add(mods[j] == self.cellValues[-1][j]-2*divs[j])
		self.cellParity.append(mods)
	
	self._propertyInitialized.append('Parity')
	
def _initializeEntropy(self):
	if 'Entropy' not in self._propertyInitialized:
		self._setEntropy()

def _setEntropy(self):
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
		
	if 'VariableExteriorClues' in self._constraintInitialized:
		for i in range(self.boardWidth):
			# Right column
			c = self.model.NewIntVar(min(0,self.minDigit*self.boardWidth) // 3 - 1,self.maxDigit*self.boardWidth // 3,'entropyValue{:d}{:d}'.format(i,self.boardWidth))
			self.model.Add(3*c+1 <= self.cellValues[i][self.boardWidth])
			self.model.Add(3*c+4 > self.cellValues[i][self.boardWidth])
			self.cellEntropy[i].append(c)
			# Left column
			c = self.model.NewIntVar(min(0,self.minDigit*self.boardWidth) // 3 - 1,self.maxDigit*self.boardWidth // 3,'entropyValue{:d}{:d}'.format(i,-1))
			self.model.Add(3*c+1 <= self.cellValues[i][-1])
			self.model.Add(3*c+4 > self.cellValues[i][-1])
			self.cellEntropy[i].append(c)
		
		# Bottom row
		cs = [self.model.NewIntVar(min(0,self.minDigit*self.boardWidth) // 3 - 1,self.maxDigit*self.boardWidth // 3,'entropyValue{:d}{:d}'.format(self.boardWidth,j)) for j in range(self.boardWidth+2)]
		for j in range(self.boardWidth+2):
			self.model.Add(3*cs[j]+1 <= self.cellValues[self.boardWidth][j])
			self.model.Add(3*cs[j]+4 > self.cellValues[self.boardWidth][j])
		self.cellEntropy.append(cs)
		## Top row
		cs = [self.model.NewIntVar(min(0,self.minDigit*self.boardWidth) // 3 - 1,self.maxDigit*self.boardWidth // 3,'entropyValue{:d}{:d}'.format(self.boardWidth,-1)) for j in range(self.boardWidth+2)]
		for j in range(self.boardWidth+2):
			self.model.Add(3*cs[j]+1 <= self.cellValues[-1][j])
			self.model.Add(3*cs[j]+4 > self.cellValues[-1][j])
		self.cellEntropy.append(cs)
	
	self._propertyInitialized.append('Entropy')

def _initializeModular(self):
	if 'Modular' not in self._propertyInitialized:
		self._setModular()

def _setModular(self):
	# Set up variables to track modular constraints
	if 'Entropy' not in self._propertyInitialized:
		self._setEntropy()
	
	self.cellModular = []
	
	for i in range(self.boardWidth):
		t = []
		for j in range(self.boardWidth):
			c = self.model.NewIntVar(1,3,'modularValue{:d}{:d}'.format(i,j))
			t.append(c)
			self.model.Add(c == self.cellValues[i][j] - 3*self.cellEntropy[i][j])
		self.cellModular.insert(i,t)

	if 'VariableExteriorClues' in self._constraintInitialized:
		for i in range(self.boardWidth):
			# Right column
			c = self.model.NewIntVar(1,3,'modularValue{:d}{:d}'.format(i,self.boardWidth))
			self.model.Add(c == self.cellValues[i][self.boardWidth] - 3*self.cellEntropy[i][self.boardWidth])
			self.cellModular[i].append(c)
			# Left column
			c = self.model.NewIntVar(1,3,'modularValue{:d}{:d}'.format(i,-1))
			self.model.Add(c == self.cellValues[i][-1] - 3*self.cellEntropy[i][-1])
			self.cellModular[i].append(c)
		
		# Bottom row
		cs = [self.model.NewIntVar(1,3,'modularValue{:d}{:d}'.format(self.boardWidth,j)) for j in range(self.boardWidth+2)]
		for j in range(self.boardWidth+2):
			self.model.Add(cs[j] == self.cellValues[self.boardWidth][j] - 3*self.cellEntropy[self.boardWidth][j])
		self.cellModular.append(cs)
		## Top row
		cs = [self.model.NewIntVar(1,3,'modularValue{:d}{:d}'.format(-1,j)) for j in range(self.boardWidth+2)]
		for j in range(self.boardWidth+2):
			self.model.Add(cs[j] == self.cellValues[-1][j] - 3*self.cellEntropy[-1][j])
		self.cellModular.append(cs)
		
	self._propertyInitialized.append('Modular')
	
def _setFullRank(self):
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
				sumRow = i if j == self.Row else (self.boardWidth-1 if k == 0 else 0)
				sumCol = i if j == self.Col else (self.boardWidth-1 if k == 0 else 0)
				hStep = 0 if j == self.Col else (-1 if k == 0 else 1) 
				vStep = 0 if j == self.Row else (-1 if k == 0 else 1)
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
			
	self._propertyInitialized.append('FullRank')
	
def _initializePrimality(self):
	if 'Primality' not in self._propertyInitialized:
		self._setPrimality()

def configurePrimality(self,whatIsOne='Neither'):
	match whatIsOne:
		case 'Prime':
			one = 0
		case 'NotPrime':
			one = 2
		case 'Neither':
			one = 1
	self._setPrimality(one)

def _setPrimality(self,whatIsOne=1):
	if self.boardWidth != 9 or self.minDigit < 0 or self.maxDigit > 9:
		print("Primality constraints only supported for digits {0..9} on 9x9 boards or smaller.")
		sys.exit()

	# Set up variables to track primality constraints
	self.cellPrimality = []
	for i in range(self.boardWidth):
		t = []
		for j in range(self.boardWidth):
			varBitmap = self._varBitmap('PrimalityRow{:d}Col{:d}'.format(i,j),self.boardWidth)
			c = self.model.NewIntVar(0,2,'primalityValue{:d}{:d}'.format(i,j))
			self.model.Add(self.cellValues[i][j] == 1).OnlyEnforceIf(varBitmap[0])
			self.model.Add(c == whatIsOne).OnlyEnforceIf(varBitmap[0])
			self.model.Add(self.cellValues[i][j] == 2).OnlyEnforceIf(varBitmap[1])
			self.model.Add(c == 0).OnlyEnforceIf(varBitmap[1])
			self.model.Add(self.cellValues[i][j] == 3).OnlyEnforceIf(varBitmap[2])
			self.model.Add(c == 0).OnlyEnforceIf(varBitmap[2])
			self.model.Add(self.cellValues[i][j] == 4).OnlyEnforceIf(varBitmap[3])
			self.model.Add(c == 2).OnlyEnforceIf(varBitmap[3])
			self.model.Add(self.cellValues[i][j] == 5).OnlyEnforceIf(varBitmap[4])
			self.model.Add(c == 0).OnlyEnforceIf(varBitmap[4])
			self.model.Add(self.cellValues[i][j] == 6).OnlyEnforceIf(varBitmap[5])
			self.model.Add(c == 2).OnlyEnforceIf(varBitmap[5])
			self.model.Add(self.cellValues[i][j] == 7).OnlyEnforceIf(varBitmap[6])
			self.model.Add(c == 0).OnlyEnforceIf(varBitmap[6])
			self.model.Add(self.cellValues[i][j] == 8).OnlyEnforceIf(varBitmap[7])
			self.model.Add(c == 2).OnlyEnforceIf(varBitmap[7])
			self.model.Add(self.cellValues[i][j] == 9).OnlyEnforceIf(varBitmap[8])
			self.model.Add(c == 2).OnlyEnforceIf(varBitmap[8])
			t.append(c)
		self.cellPrimality.insert(i,t)
	self._propertyInitialized.append('Primality')

def _initializeDigitSize(self):
	if 'DigitSize' not in self._propertyInitialized:
		self._setDigitSize()

def configureDigitSize(self,whatIsFive='Neither'):
	match whatIsFive:
		case 'Big':
			five = 2
		case 'Small':
			five = 0
		case 'Neither':
			five = 1
	self._setDigitSize(five)

def _setDigitSize(self,whatIsFive=1):
	if self.boardWidth != 9 or self.minDigit < 0 or self.maxDigit > 9:
		print("DigitSize constraints only supported for digits {0..9} on 9x9 boards or smaller.")
		sys.exit()

	# Set up variables to track magnitude constraints
	self.cellDigitSize = []
	for i in range(self.boardWidth):
		t = []
		for j in range(self.boardWidth):
			c = self.model.NewIntVar(0,2,'MagnitudeValue{:d}{:d}'.format(i,j))
			if whatIsFive == 0:
				varBitmap = self._varBitmap('MagnitudeRow{:d}Col{:d}'.format(i,j),2)
				self.model.Add(self.cellValues[i][j] <= 5).OnlyEnforceIf(varBitmap[0])
				self.model.Add(c == 0).OnlyEnforceIf(varBitmap[0])
				self.model.Add(self.cellValues[i][j] > 5).OnlyEnforceIf(varBitmap[1])
				self.model.Add(c == 2).OnlyEnforceIf(varBitmap[1])
			elif whatIsFive == 2:	
				varBitmap = self._varBitmap('MagnitudeRow{:d}Col{:d}'.format(i,j),2)
				self.model.Add(self.cellValues[i][j] < 5).OnlyEnforceIf(varBitmap[0])
				self.model.Add(c == 0).OnlyEnforceIf(varBitmap[0])
				self.model.Add(self.cellValues[i][j] >= 5).OnlyEnforceIf(varBitmap[1])
				self.model.Add(c == 2).OnlyEnforceIf(varBitmap[1])
			else:
				varBitmap = self._varBitmap('MagnitudeRow{:d}Col{:d}'.format(i,j),2)
				self.model.Add(self.cellValues[i][j] < 5).OnlyEnforceIf(varBitmap[0])
				self.model.Add(c == 0).OnlyEnforceIf(varBitmap[0])
				self.model.Add(self.cellValues[i][j] == 5).OnlyEnforceIf(varBitmap[1])
				self.model.Add(c == 1).OnlyEnforceIf(varBitmap[1])
				self.model.Add(self.cellValues[i][j] > 5).OnlyEnforceIf(varBitmap[2])
				self.model.Add(c == 2).OnlyEnforceIf(varBitmap[2])
			t.append(c)
		self.cellDigitSize.insert(i,t)
	self._propertyInitialized.append('DigitSize')
	
def getCellVar(self,i,j):
	# Returns the model variable associated with a cell value. Useful when tying several puzzles together, e.g. Samurai
	return self.cellValues[i][j]
	
def assertNoRoping(self,rc):
	if rc == self.Row:
		rows = [[(3*j,i) for i in range(3)] for j in range(3)]
	else:
		rows = [[(i,3*j) for i in range(3)] for j in range(3)]

	minVars = [self.model.NewIntVar(self.minDigit,self.maxDigit,'roping') for j in range(3)]
	for i in range(3):
		self.model.AddMinEquality(minVars[i],[self.cellValues[x[0]][x[1]] for x in rows[i]])
	maxVars = [self.model.NewIntVar(self.minDigit,self.maxDigit,'roping') for j in range(3)]
	for i in range(3):
		self.model.AddMaxEquality(maxVars[i],[self.cellValues[x[0]][x[1]] for x in rows[i]])
	sumVars = [self.model.NewIntVar(3*self.minDigit,3*self.maxDigit,'roping') for j in range(3)]
	for i in range(3):
		self.model.Add(sumVars[i] == sum([self.cellValues[x[0]][x[1]] for x in rows[i]]))
	
	hStep = 0 if rc == self.Col else 1
	vStep = 0 if rc == self.Row else 1
	
	for i in range(3):
		for j in range(1,3):
			myMinVar = self.model.NewIntVar(self.minDigit,self.maxDigit,'roping')
			myMaxVar = self.model.NewIntVar(self.minDigit,self.maxDigit,'roping')
			mySumVar = self.model.NewIntVar(3*self.minDigit,3*self.maxDigit,'roping')
			myTestRow = [(x[0]+j*hStep+3*vStep,x[1]+j*vStep+3*hStep) for x in rows[i]]

			self.model.AddMinEquality(myMinVar,[self.cellValues[x[0]][x[1]] for x in myTestRow])
			self.model.AddMaxEquality(myMaxVar,[self.cellValues[x[0]][x[1]] for x in myTestRow])
			self.model.Add(mySumVar == sum([self.cellValues[x[0]][x[1]] for x in myTestRow]))
			
			compVars = [self.model.NewBoolVar('roping') for k in range(3)]
			self.model.Add(minVars[i] == myMinVar).OnlyEnforceIf(compVars[0].Not())
			self.model.Add(minVars[i] != myMinVar).OnlyEnforceIf(compVars[0])
			self.model.Add(maxVars[i] == myMaxVar).OnlyEnforceIf(compVars[1].Not())
			self.model.Add(maxVars[i] != myMaxVar).OnlyEnforceIf(compVars[1])
			self.model.Add(sumVars[i] == mySumVar).OnlyEnforceIf(compVars[2].Not())
			self.model.Add(sumVars[i] != mySumVar).OnlyEnforceIf(compVars[2])
			self.model.AddBoolOr(compVars)

def _selectCellsMatchDigitSet(self,myVars,L,values,OEI=[]):
	if type(values) is int:
		values = [values]
	for i in range(len(myVars)):
		for j in self.digits:
			if j in values:
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] != j).OnlyEnforceIf([myVars[i].Not()] + OEI)
			else:
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] != j).OnlyEnforceIf([myVars[i]] + OEI)

def _selectCellsOnLine(self,L,selectCriteria,OEI=[]):
	
	# Migrated from a version which worked on row/column, should not be too hard :-)
	# I'm going to create selection Booleans to evaluate each cell against the selectCriteria criteria. 
	# Notice how I'm clever enough to avoid defining selectSummands as long as I can. #genius
	selectionCells = [self.model.NewBoolVar('SelectionCondition{:d}'.format(i)) for i in range(len(L))]
	self.allVars = self.allVars + selectionCells
	for x in OEI:
		self.model.AddBoolAnd(selectionCells).OnlyEnforceIf(x.Not())
	
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
		for x in OEI:
			self.model.AddBoolAnd(criterionBools).OnlyEnforceIf(x.Not())
		
		match criterion[0]:
			case 'All':
				self.model.AddBoolAnd(criterionBools).OnlyEnforceIf(OEI)
			
			case 'Location':
				thisCriterion = 0
				theseCriteria = []
				for n in range(1,len(criterion),2):
					thisCriterionBools = [self.model.NewBoolVar('Criterion{:d}{:d}'.format(criterionNumber,i)) for i in range(len(L))]
					for x in OEI:
						self.model.AddBoolAnd(thisCriterionBools).OnlyEnforceIf(x.Not())
					match criterion[n]:
						case self.LE:
							self.model.AddBoolAnd([thisCriterionBools[j] for j in range(criterion[n+1])]).OnlyEnforceIf(OEI)
							self.model.AddBoolAnd([thisCriterionBools[j].Not() for j in range(criterion[n+1],len(L))]).OnlyEnforceIf(OEI)
						case self.EQ:
							self.model.AddBoolAnd([thisCriterionBools[criterion[n+1]-1]]).OnlyEnforceIf(OEI)
							self.model.AddBoolAnd([thisCriterionBools[j].Not() for j in range(len(L)) if j != criterion[n+1]-1]).OnlyEnforceIf(OEI)
						case self.GE:
							self.model.AddBoolAnd([thisCriterionBools[j].Not() for j in range(criterion[n+1]-1)]).OnlyEnforceIf(OEI)
							self.model.AddBoolAnd([thisCriterionBools[j] for j in range(criterion[n+1]-1,len(L))]).OnlyEnforceIf(OEI)
						case self.NE:
							self.model.AddBoolAnd([thisCriterionBools[criterion[n+1]-1].Not()]).OnlyEnforceIf(OEI)
							self.model.AddBoolAnd([thisCriterionBools[j] for j in range(len(L)) if j != criterion[n+1]-1]).OnlyEnforceIf(OEI)
						case 'Indexed':
							for i in range(len(L)):
								self.model.Add(self.cellValues[L[criterion[n+1]-1][0]][L[criterion[n+1]-1][1]] == i+1).OnlyEnforceIf([thisCriterionBools[i]] + OEI)
								self.model.Add(self.cellValues[L[criterion[n+1]-1][0]][L[criterion[n+1]-1][1]] != i+1).OnlyEnforceIf([thisCriterionBools[i].Not()] + OEI)
						case 'Distance':
							for i in range(len(L)):
								self.model.Add(self.cellValues[L[criterion[n+1]-1][0]][L[criterion[n+1]-1][1]] == i-criterion[n+1]+1).OnlyEnforceIf([thisCriterionBools[i]] + OEI)
								self.model.Add(self.cellValues[L[criterion[n+1]-1][0]][L[criterion[n+1]-1][1]] != i-criterion[n+1]+1).OnlyEnforceIf([thisCriterionBools[i].Not()] + OEI)
			
					theseCriteria.insert(thisCriterion,thisCriterionBools)
					thisCriterion = thisCriterion + 1
				for i in range(len(L)):
					self.model.AddBoolOr([theseCriteria[j][i] for j in range(len(theseCriteria))]).OnlyEnforceIf([criterionBools[i]] + OEI)
					self.model.AddBoolAnd([theseCriteria[j][i].Not() for j in range(len(theseCriteria))]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
					
			case 'LocationSkip':
				self.model.AddBoolAnd([criterionBools[j] for j in range(len(L)) if (j % criterion[1]) == criterion[2]]).OnlyEnforceIf(OEI)
				self.model.AddBoolAnd([criterionBools[j].Not() for j in range(len(L)) if (j % criterion[1]) != criterion[2]]).OnlyEnforceIf(OEI)
				
			case 'Magnitude':
				for i in range(len(L)):
					match criterion[1]:
						case self.LE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] <= criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] > criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.EQ:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] == criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] != criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.GE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] >= criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] < criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.NE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] != criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] == criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
			
			case 'Parity' | 'Entropy' | 'Modular' | 'Primality' | 'DigitSize':
				if criterion[0] not in self._propertyInitialized:
					getattr(self,'_set'+criterion[0])()
				myCells = getattr(self,'cell'+criterion[0])
				for i in range(len(L)):
					match criterion[1]:
						case self.LE:
							self.model.Add(myCells[L[i][0]][L[i][1]] <= criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(myCells[L[i][0]][L[i][1]] > criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.EQ:
							self.model.Add(myCells[L[i][0]][L[i][1]] == criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(myCells[L[i][0]][L[i][1]] != criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.GE:
							self.model.Add(myCells[L[i][0]][L[i][1]] >= criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(myCells[L[i][0]][L[i][1]] < criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.NE:
							self.model.Add(myCells[L[i][0]][L[i][1]] != criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(myCells[L[i][0]][L[i][1]] == criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
							
			case 'Uniparity':
				self._initializeParity()
				c = self.model.NewBoolVar('selectionCriteriaUnipartyPickEven')
				d = self.model.NewBoolVar('selectionCriteriaUnipartyPickOdd')
				self.model.AddBoolAnd(OEI).OnlyEnforceIf(c)
				self.model.AddBoolAnd(OEI).OnlyEnforceIf(d.Not())
				for i in range(len(L)):
					self.model.Add(self.cellParity[L[i][0]][L[i][1]] == 0).OnlyEnforceIf([criterionBools[i],c] + OEI)
					self.model.Add(self.cellParity[L[i][0]][L[i][1]] == 1).OnlyEnforceIf([criterionBools[i].Not(),c] + OEI)
					self.model.Add(self.cellParity[L[i][0]][L[i][1]] == 1).OnlyEnforceIf([criterionBools[i],d] + OEI)
					self.model.Add(self.cellParity[L[i][0]][L[i][1]] == 0).OnlyEnforceIf([criterionBools[i].Not(),d] + OEI)
				self.model.AddBoolXOr([c,d])
							
			case 'MatchParity' | 'MatchEntropy' | 'MatchModular' | 'MatchPrimality' | 'MatchDigitSize':
				if criterion[0][5:] not in self._propertyInitialized:
					getattr(self,'_set'+criterion[0][5:])()
				mCell = criterion[1] - 1
				myCells = getattr(self,'cell'+criterion[0][5:])
				for i in range(len(L)):
					self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[mCell][0]][L[mCell][1]]).OnlyEnforceIf([criterionBools[i]] + OEI)
					self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[mCell][0]][L[mCell][1]]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
							
			case 'DoNotMatchParity' | 'DoNotMatchEntropy' | 'DoNotMatchModular' | 'DoNotMatchPrimality' | 'DoNotMatchDigitSize':
				if criterion[0][10:] not in self._propertyInitialized:
					getattr(self,'_set'+criterion[0][10:])()
				mCell = criterion[1] - 1
				myCells = getattr(self,'cell'+criterion[0][10:])
				for i in range(len(L)):
					self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[mCell][0]][L[mCell][1]]).OnlyEnforceIf([criterionBools[i]] + OEI)
					self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[mCell][0]][L[mCell][1]]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
					
			case 'ParityChange' | 'EntropyChange' | 'ModularChange' | 'PrimalityChange' | 'DigitSizeChange':
				if criterion[0][0:-6] not in self._propertyInitialized:
					getattr(self,'_set'+criterion[0][0:-6])()
				if criterion[1] == 'before':
					self.model.AddBoolAnd(criterionBools[-1].Not()).OnlyEnforceIf(OEI)  # last cell cannot be picked
				else:
					self.model.AddBoolAnd(criterionBools[0].Not()).OnlyEnforceIf(OEI)  # first cell cannot be picked
				myCells = getattr(self,'cell'+criterion[0][0:-6])
				for i in range(1,len(L)):
					if criterion[1] == 'before':
						self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf([criterionBools[i-1]] + OEI)
						self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf([criterionBools[i-1].Not()] + OEI)
					else:
						self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
					
			case 'DigitSet':
				self._selectCellsMatchDigitSet(criterionBools,L,criterion[1],OEI)
							
			case 'BeforeDigits':
				matchDigit = [self.model.NewBoolVar('BeforeDigitsMatch') for i in range(len(L))]
				for x in OEI:
					self.model.AddBoolAnd(matchDigit).OnlyEnforceIf(x.Not())
				self._selectCellsMatchDigitSet(matchDigit,L,criterion[1],OEI)
				self.model.AddBoolAnd(criterionBools[-1].Not()).OnlyEnforceIf([criterionBools[-1]] + OEI)
				for i in range(1,len(L)):
					self.model.AddBoolAnd(criterionBools[i-1]).OnlyEnforceIf([matchDigit[i]] + OEI)
					self.model.AddBoolAnd(criterionBools[i-1].Not()).OnlyEnforceIf([matchDigit[i].Not()] + OEI)

			case 'AfterDigits':
				matchDigit = [self.model.NewBoolVar('AfterDigitsMatch') for i in range(len(L))]
				for x in OEI:
					self.model.AddBoolAnd(matchDigit).OnlyEnforceIf(x.Not())
				self._selectCellsMatchDigitSet(matchDigit,L,criterion[1],OEI)
				self.model.AddBoolAnd(criterionBools[0].Not()).OnlyEnforceIf([criterionBools[0]] + OEI)
				for i in range(len(L)-1):
					self.model.AddBoolAnd(criterionBools[i+1]).OnlyEnforceIf([matchDigit[i]] + OEI)
					self.model.AddBoolAnd(criterionBools[i+1].Not()).OnlyEnforceIf([matchDigit[i].Not()] + OEI)
					
			case 'NextToDigits':
				matchDigit = [self.model.NewBoolVar('AfterDigitsMatch') for i in range(len(L))]
				for x in OEI:
					self.model.AddBoolAnd(matchDigit).OnlyEnforceIf(x.Not())
				self._selectCellsMatchDigitSet(matchDigit,L,criterion[1],OEI)
				self.model.AddBoolAnd(criterionBools[0]).OnlyEnforceIf([matchDigit[1]] + OEI)
				self.model.AddBoolAnd(criterionBools[0].Not()).OnlyEnforceIf([matchDigit[1].Not()] + OEI)
				self.model.AddBoolAnd(criterionBools[-1]).OnlyEnforceIf([matchDigit[-2]] + OEI)
				self.model.AddBoolAnd(criterionBools[-1].Not()).OnlyEnforceIf([matchDigit[-2].Not()] + OEI)
				for i in range(1,len(L)-1):
					self.model.AddBoolOr([matchDigit[i-1],matchDigit[i+1]]).OnlyEnforceIf([criterionBools[i]] + OEI)
					self.model.AddBoolAnd([matchDigit[i-1].Not(),matchDigit[i+1].Not()]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						
			case 'DigitInstance':
				instanceCount = [self.model.NewIntVar(0,len(L),'SelectionCriterionInstanceCount') for i in range(len(L))]
				for x in OEI:
					for j in range(len(L)):
						self.model.Add(instanceCount[j] == 0).OnlyEnforceIf(x.Not())
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf(OEI)
				for i in range(1,len(L)):
					isFirst = self.model.NewBoolVar('SelectionCriterionIsFirst')
					for x in OEI:
						self.model.AddBoolAnd(isFirst).OnlyEnforceIf(x.Not())
					for j in range(i):
						self.model.Add(self.cellValues[L[j][0]][L[j][1]] != self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf([isFirst] + OEI)
					self.model.Add(instanceCount[i] == 1).OnlyEnforceIf([isFirst] + OEI)
					
					lastMatch = [self.model.NewBoolVar('SelectionCriterionLastMatch') for j in range(i)]
					for x in OEI:
						self.model.AddBoolAnd(lastMatch).OnlyEnforceIf(x.Not())
					self.model.AddBoolOr(lastMatch).OnlyEnforceIf([isFirst.Not()] + OEI)
					self.model.AddBoolAnd([x.Not() for x in lastMatch]).OnlyEnforceIf([isFirst] + OEI)
					
					for j in range(i):
						self.model.Add(self.cellValues[L[j][0]][L[j][1]] == self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf([lastMatch[j]] + OEI)
						for k in range(j+1,i):
							self.model.Add(self.cellValues[L[k][0]][L[k][1]] != self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf([lastMatch[j]] + OEI)
						self.model.Add(instanceCount[i] == instanceCount[j] + 1).OnlyEnforceIf([lastMatch[j]] + OEI)
					
				for i in range(len(L)):
					match criterion[1]:
						case self.LE:
							self.model.Add(instanceCount[i] <= criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(instanceCount[i] > criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.EQ:
							self.model.Add(instanceCount[i] == criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(instanceCount[i] != criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.GE:
							self.model.Add(instanceCount[i] >= criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(instanceCount[i] < criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.NE:
							self.model.Add(instanceCount[i] != criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(instanceCount[i] == criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)

			case 'NoRepeats':
				matchVars = []
				for i in range(len(L)):
					myMatchVars = [self.model.NewBoolVar('SelectionNoRepeatsMatch{:d}{:d}'.format(i,j)) for j in range(i)]
					matchVars.insert(i,myMatchVars)
					for x in OEI:
						self.model.AddBoolAnd(myMatchVars).OnlyEnforceIf(x.Not())
					for j in range(i):
						self.model.Add(self.cellValues[L[i][0]][L[i][1]] == self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([myMatchVars[j]] + OEI)
						self.model.Add(self.cellValues[L[i][0]][L[i][1]] != self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([myMatchVars[j].Not()] + OEI)
				for i in range(len(L)):
					self.model.AddBoolAnd([x.Not() for x in matchVars[i]] + [matchVars[j][i].Not() for j in range(i+1,len(L))]).OnlyEnforceIf([criterionBools[i]] + OEI)
					self.model.AddBoolOr(matchVars[i] + [matchVars[j][i] for j in range(i+1,len(L))]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)

			case 'ConsecutiveNeighbor'|'ConsecutiveBefore'|'ConsecutiveAfter'|'ConsecutiveNone':
				consecPair = [self.model.NewBoolVar('ConsecPair') for j in range(len(L)-1)]
				maxPair = [self.model.NewIntVar(self.minDigit,self.maxDigit,'ConsecPairMax') for j in range(len(L)-1)]
				minPair = [self.model.NewIntVar(self.minDigit,self.maxDigit,'ConsecPairMin') for j in range(len(L)-1)]
				for x in OEI:
					self.model.AddBoolAnd(consecPair).OnlyEnforceIf(x.Not())
				for i in range(len(L)-1):
					self.model.AddMinEquality(minPair[i],[self.cellValues[L[i][0]][L[i][1]],self.cellValues[L[i+1][0]][L[i+1][1]]])
					self.model.AddMaxEquality(maxPair[i],[self.cellValues[L[i][0]][L[i][1]],self.cellValues[L[i+1][0]][L[i+1][1]]])
					self.model.Add(maxPair[i] - minPair[i] == 1).OnlyEnforceIf([consecPair[i]] + OEI)
					self.model.Add(maxPair[i] - minPair[i] != 1).OnlyEnforceIf([consecPair[i].Not()] + OEI)
				
				if criterion[0] == 'ConsecutiveNeighbor':
					self.model.AddBoolAnd(consecPair[0]).OnlyEnforceIf([criterionBools[0]] + OEI)
					self.model.AddBoolAnd(consecPair[0].Not()).OnlyEnforceIf([criterionBools[0].Not()] + OEI)
					self.model.AddBoolAnd(consecPair[-1]).OnlyEnforceIf([criterionBools[-1]] + OEI)
					self.model.AddBoolAnd(consecPair[-1].Not()).OnlyEnforceIf([criterionBools[-1].Not()] + OEI)
					for i in range(1,len(L)-1):
						self.model.AddBoolOr([consecPair[i-1],consecPair[i]]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolAnd([consecPair[i-1].Not(),consecPair[i].Not()]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif criterion[0] == 'ConsecutiveBefore':
					self.model.AddBoolAnd(criterionBools[0].Not()).OnlyEnforceIf(OEI)
					for i in range(1,len(L)):
						self.model.AddBoolAnd(consecPair[i-1]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolAnd(consecPair[i-1].Not()).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif criterion[0] == 'ConsecutiveAfter':
					self.model.AddBoolAnd(criterionBools[-1].Not()).OnlyEnforceIf(OEI)
					for i in range(len(L)-1):
						self.model.AddBoolAnd(consecPair[i]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolAnd(consecPair[i].Not()).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif criterion[0] == 'ConsecutiveNone':
					self.model.AddBoolAnd(consecPair[0].Not()).OnlyEnforceIf([criterionBools[0]] + OEI)
					self.model.AddBoolAnd(consecPair[0]).OnlyEnforceIf([criterionBools[0].Not()] + OEI)
					self.model.AddBoolAnd(consecPair[-1].Not()).OnlyEnforceIf([criterionBools[-1]] + OEI)
					self.model.AddBoolAnd(consecPair[-1]).OnlyEnforceIf([criterionBools[-1].Not()] + OEI)
					for i in range(1,len(L)-1):
						self.model.AddBoolAnd([consecPair[i-1].Not(),consecPair[i].Not()]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolOr([consecPair[i-1],consecPair[i]]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)

			case 'ParityNeighbor'|'ParityBefore'|'ParityAfter'|'ParityNone'|'ParityAll'|'ParityBoth'|'ParityNeither'|'EntropyNeighbor'|'EntropyBefore'|'EntropyAfter'|'EntropyNone'|'EntropyAll'|'EntropyBoth'|'EntropyNeither'|'ModularNeighbor'|'ModularBefore'|'ModularAfter'|'ModularNone'|'ModularAll'|'ModularBoth'|'ModularNeither'|'PrimalityNeighbor'|'PrimalityBefore'|'PrimalityAfter'|'PrimalityNone'|'PrimalityAll'|'PrimalityBoth'|'PrimalityNeither'|'DigitSizeNeighbor'|'DigitSizeBefore'|'DigitSizeAfter'|'DigitSizeNone'|'DigitSizeAll'|'DigitSizeBoth'|'DigitSizeNeither':
				x = re.search("(Parity|Entropy|Modular|Primality|DigitSize)(.*)",criterion[0])
				mode = x.group(1)
				where = x.group(2)
				if mode not in self._propertyInitialized:
					getattr(self,'_set'+mode)()
				myCells = getattr(self,'cell'+mode)
				matchForward = [self.model.NewBoolVar('HasNeighborForward') for j in range(len(L))]
				matchBackward = [self.model.NewBoolVar('HasNeighborBackward') for j in range(len(L))]
				for x in OEI:
					self.model.AddBoolAnd(matchForward).OnlyEnforceIf(x.Not())
					self.model.AddBoolAnd(matchBackward).OnlyEnforceIf(x.Not())
				
				# The value we're matching may be fixed for the whole line, or may depend on the cell we're looking at
				# To avoid making a hash of things, we'll do the "whole line" stuff first, and leave the value as none
				# if it's supposed to match the current cell.
				if len(criterion) > 2:
					if criterion[1] == 'Fixed':
						myTestValue = myCells[L[criterion[2]-1][0]][L[criterion[2]-1][1]]
					elif criterion[1] == 'Indexed':
						myTestValue = self.model.NewIntVar(-1,4,'PropertyMatchIndexedValue')
						for i in range(len(L)):
							if i+1 in self.digits:
								c = self.model.NewBoolVar('PropertyMatchIndexPicker{:d}'.format(i))
								self.allVars.append(c)
								self.model.Add(self.cellValues[L[criterion[2]-1][0]][L[criterion[2]-1][1]] == i+1).OnlyEnforceIf([c] + OEI)
								self.model.Add(self.cellValues[L[criterion[2]-1][0]][L[criterion[2]-1][1]] != i+1).OnlyEnforceIf([c.Not()] + OEI)
								self.model.Add(myTestValue == myCells[L[i][0]][L[i][1]]).OnlyEnforceIf([c] + OEI)
				elif len(criterion) > 1:
					myTestValue = criterion[1]
				else:
					myTestValue = None
				
				for i in range(len(L)):
					if myTestValue is None:
						testValue = myCells[L[i][0]][L[i][1]]
					else:
						testValue = myTestValue

					if i == 0:
						self.model.AddBoolAnd(matchBackward[i].Not()).OnlyEnforceIf(OEI)
					else:
						self.model.Add(myCells[L[i-1][0]][L[i-1][1]] == testValue).OnlyEnforceIf([matchBackward[i]] + OEI)
						self.model.Add(myCells[L[i-1][0]][L[i-1][1]] != testValue).OnlyEnforceIf([matchBackward[i].Not()] + OEI)
					if i == len(L)-1:
						self.model.AddBoolAnd(matchForward[i].Not()).OnlyEnforceIf(OEI)
					else:
						self.model.Add(myCells[L[i+1][0]][L[i+1][1]] == testValue).OnlyEnforceIf([matchForward[i]] + OEI)
						self.model.Add(myCells[L[i+1][0]][L[i+1][1]] != testValue).OnlyEnforceIf([matchForward[i].Not()] + OEI)
						
				if where == 'Neighbor':
					for i in range(len(L)):
						self.model.AddBoolOr([matchForward[i],matchBackward[i]]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolAnd([matchForward[i].Not(),matchBackward[i].Not()]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif where == 'Before':
					for i in range(len(L)):
						self.model.AddBoolAnd(matchBackward[i]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolAnd(matchBackward[i].Not()).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif where == 'After':
					for i in range(len(L)):
						self.model.AddBoolAnd(matchForward[i]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolAnd(matchForward[i].Not()).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif where == 'None':
					for i in range(len(L)):
						self.model.AddBoolAnd([matchBackward[i].Not(),matchForward[i].Not()]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolOr([matchBackward[i],matchForward[i]]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif where == 'All':
					self.model.AddBoolAnd(matchForward[0]).OnlyEnforceIf([criterionBools[0]] + OEI)
					self.model.AddBoolAnd(matchForward[0].Not()).OnlyEnforceIf([criterionBools[0].Not()] + OEI)
					self.model.AddBoolAnd(matchBackward[-1]).OnlyEnforceIf([criterionBools[-1]] + OEI)
					self.model.AddBoolAnd(matchBackward[-1].Not()).OnlyEnforceIf([criterionBools[-1].Not()] + OEI)
					for i in range(1,len(L)-1):
						self.model.AddBoolAnd([matchBackward[i],matchForward[i]]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolOr([matchBackward[i].Not(),matchForward[i].Not()]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif where == 'Both':
					self.model.AddBoolAnd([criterionBools[0].Not(),criterionBools[-1].Not()]).OnlyEnforceIf(OEI)
					for i in range(1,len(L)-1):
						self.model.AddBoolAnd([matchBackward[i],matchForward[i]]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolOr([matchBackward[i].Not(),matchForward[i].Not()]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif where == 'Neither':
					self.model.AddBoolAnd([criterionBools[0].Not(),criterionBools[-1].Not()]).OnlyEnforceIf(OEI)
					for i in range(1,len(L)-1):
						self.model.AddBoolAnd([matchBackward[i].Not(),matchForward[i].Not()]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolOr([matchBackward[i],matchForward[i]]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)

			case 'ParityRun'|'EntropyRun'|'ModularRun'|'PrimalityRun'|'DigitSizeRun':
				# First split the line up into contiguous runs
				runNumber = self._partitionProperty(L,criterion[0],OEI)
				
				filteredRunNumber = [self.model.NewIntVar(0,len(L),'PropertyRunSelectionFilteredNumber') for i in range(len(L))]
				filteredRunCount = [self.model.NewIntVar(0,len(L),'PropertyRunSelectionFilteredCount') for i in range(len(L))]
				
				for x in OEI:
					for i in range(len(L)):
						self.model.Add(filteredRunNumber[i] == 0).OnlyEnforceIf(x.Not())
						self.model.Add(filteredRunCount[i] == 0).OnlyEnforceIf(x.Not())
				
				match criterion[1][0]:
					case 'Any':
						for i in range(len(L)):
							self.model.Add(filteredRunNumber[i] == runNumber[i]).OnlyEnforceIf(OEI)
					case _:
						propertyMatch = [self.model.NewBoolVar('PropertyRunMatch') for i in range(len(L))]
						for x in OEI:
							self.model.AddBoolAnd(propertyMatch).OnlyEnforceIf(x.Not())
						if criterion[1][0] == 'Property':
							comparisonValue = criterion[1][2]
						else:
							comparisonValue = myCells[L[criterion[1][2]-1][0]][L[criterion[1][2]-1][1]]
						for i in range(len(L)):
							match criterion[1][1]:
								case self.EQ:
									self.model.Add(myCells[L[i][0]][L[i][1]] == comparisonValue).OnlyEnforceIf([propertyMatch[i]] + OEI)
									self.model.Add(myCells[L[i][0]][L[i][1]] != comparisonValue).OnlyEnforceIf([propertyMatch[i].Not()] + OEI)
								case self.LE:
									self.model.Add(myCells[L[i][0]][L[i][1]] <= comparisonValue).OnlyEnforceIf([propertyMatch[i]] + OEI)
									self.model.Add(myCells[L[i][0]][L[i][1]] > comparisonValue).OnlyEnforceIf([propertyMatch[i].Not()] + OEI)
								case self.GE:
									self.model.Add(myCells[L[i][0]][L[i][1]] >= comparisonValue).OnlyEnforceIf([propertyMatch[i]] + OEI)
									self.model.Add(myCells[L[i][0]][L[i][1]] < comparisonValue).OnlyEnforceIf([propertyMatch[i].Not()] + OEI)
								case self.NE:
									self.model.Add(myCells[L[i][0]][L[i][1]] != comparisonValue).OnlyEnforceIf([propertyMatch[i]] + OEI)
									self.model.Add(myCells[L[i][0]][L[i][1]] == comparisonValue).OnlyEnforceIf([propertyMatch[i].Not()] + OEI)
							if i == 0:
								self.model.Add(filteredRunNumber[0] == 1).OnlyEnforceIf([propertyMatch[0]] + OEI)
								self.model.Add(filteredRunNumber[0] == 0).OnlyEnforceIf([propertyMatch[0].Not()] + OEI)
								self.model.Add(filteredRunCount[0] == 1).OnlyEnforceIf([propertyMatch[0]] + OEI)
								self.model.Add(filteredRunCount[0] == 0).OnlyEnforceIf([propertyMatch[0].Not()] + OEI)
							else:
								# propertySwitch determines if the property switch is here; if not, keep these steady
								self.model.Add(filteredRunNumber[i] == filteredRunNumber[i-1]).OnlyEnforceIf([propertySwitch[i].Not()] + OEI)
								self.model.Add(filteredRunCount[i] == filteredRunCount[i-1]).OnlyEnforceIf([propertySwitch[i].Not()] + OEI)
								
								# Now if there is a switch and the new cell is a property match, create a new filtered group number
								self.model.Add(filteredRunNumber[i] == filteredRunCount[i-1]+1).OnlyEnforceIf([propertySwitch[i],propertyMatch[i]] + OEI)
								self.model.Add(filteredRunCount[i] == filteredRunCount[i-1]+1).OnlyEnforceIf([propertySwitch[i],propertyMatch[i]] + OEI)
							
								# If there is a switch, but the new cell is not a match, we don't increment the countm, and we make the run number 0
								self.model.Add(filteredRunNumber[i] == 0).OnlyEnforceIf([propertySwitch[i],propertyMatch[i].Not()] + OEI)
								self.model.Add(filteredRunCount[i] == filteredRunCount[i-1]).OnlyEnforceIf([propertySwitch[i],propertyMatch[i].Not()] + OEI)
				if type(criterion[2]) is int:
					for i in range(len(L)):
						self.model.Add(filteredRunNumber[i] == criterion[2]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.Add(filteredRunNumber[i] != criterion[2]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif criterion[2] == 'Last':
					for i in range(len(L)):
						self.model.Add(filteredRunNumber[i] == filteredRunCount[-1]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.Add(filteredRunNumber[i] != filteredRunCount[-1]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				else:
					for i in range(len(L)):
						myBools = [self.model.NewBoolVar('PropertyRunSelectionMultipleRanges') for j in range(len(criterion[2]))]
						for x in OEI:
							self.model.AddBoolAnd(myBools).OnlyEnforceIf(x.Not())
						for j in range(len(criterion[2])):
							if type(criterion[2][j]) is int:
								self.model.Add(filteredRunNumber[i] == criterion[2][j]).OnlyEnforceIf([myBools[j]] + OEI)
								self.model.Add(filteredRunNumber[i] != criterion[2][j]).OnlyEnforceIf([myBools[j].Not()] + OEI)
							else:
								self.model.Add(filteredRunNumber[i] == filteredRunCount[-1]).OnlyEnforceIf([myBools[j]] + OEI)
								self.model.Add(filteredRunNumber[i] != filteredRunCount[-1]).OnlyEnforceIf([myBools[j].Not()] + OEI)
						self.model.AddBoolOr(myBools).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolAnd([x.Not() for x in myBools]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)

			case 'AscendingRun'|'DescendingRun':
				# First split the line up into contiguous runs
				runNumber = self._partitionMonotone(L,criterion[0],OEI)
				if type(criterion[1]) is int:
					for i in range(len(L)):
						self.model.Add(runNumber[i] == criterion[1]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.Add(runNumber[i] != criterion[1]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				elif criterion[1] == 'Last':
					for i in range(len(L)):
						self.model.Add(runNumber[i] == runNumber[-1]).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.Add(runNumber[i] != runNumber[-1]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
				else:
					for i in range(len(L)):
						myBools = [self.model.NewBoolVar('UpDownRunSelectionMultipleRanges') for j in range(len(criterion[1]))]
						for x in OEI:
							self.model.AddBoolAnd(myBools).OnlyEnforceIf(x.Not())
						for j in range(len(criterion[1])):
							if type(criterion[1][j]) is int:
								self.model.Add(runNumber[i] == criterion[1][j]).OnlyEnforceIf([myBools[j]] + OEI)
								self.model.Add(runNumber[i] != criterion[1][j]).OnlyEnforceIf([myBools[j].Not()] + OEI)
							else:
								self.model.Add(runNumber[i] == runNumber[-1]).OnlyEnforceIf([myBools[j]] + OEI)
								self.model.Add(runNumber[i] != runNumber[-1]).OnlyEnforceIf([myBools[j].Not()] + OEI)
						self.model.AddBoolOr(myBools).OnlyEnforceIf([criterionBools[i]] + OEI)
						self.model.AddBoolAnd([x.Not() for x in myBools]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)

			case 'Skyscrapers':
				# Select the cells which are the maximum of all cells seens thus far
				self.model.AddBoolAnd(criterionBools[0]).OnlyEnforceIf(OEI)
				for i in range(1,len(L)):
					maxVar = self.model.NewIntVar(0,max(self.digits),'SelectionSkyscraper{:d}'.format(i))
					self.model.AddMaxEquality(maxVar,[self.cellValues[L[j][0]][L[j][1]] for j in range(i+1)])
					self.model.Add(self.cellValues[L[i][0]][L[i][1]] == maxVar).OnlyEnforceIf([criterionBools[i]] + OEI)
					self.model.Add(self.cellValues[L[i][0]][L[i][1]] < maxVar).OnlyEnforceIf([criterionBools[i].Not()] + OEI)

			case 'RelatedDigit':
				base = criterion[1]-1
				comparator = criterion[2]
				scale = criterion[3]
				shift = criterion[4]
				
				for i in range(len(L)):
					match comparator:
						case self.LE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] <= scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] > scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.EQ:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] == scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] != scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.GE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] >= scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] < scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.NE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] != scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] == scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([criterionBools[i].Not()] + OEI)

			case 'MajorityParity'|'MajorityEntropy'|'MajorityModularity'|'MajorityPrimality'|'MajorityDigitSize'|'MinorityParity'|'MinorityEntropy'|'MinorityModularity'|'MinorityPrimality'|'MinorityDigitSize':
				if criterion[0][8:] not in self._propertyInitialized:
					getattr(self,'_set'+criterion[0][8:])()
				myCells = getattr(self,'cell'+criterion[0][8:])
				
				countSame = [self.model.NewIntVar(0,len(L),'MajorityPropertyMatchCount') for i in range(len(L))]
				for x in OEI:
					for i in range(len(L)):
						self.model.Add(countSame[i] == 0).OnlyEnforceIf(x.Not())
				
				for i in range(len(L)):
					isSame = [self.model.NewBoolVar('MajorityPropertyComparisonBool') for j in range(len(L))]
					isSameInt = [self.model.NewIntVar(0,1,'MajorityPropertyComparisonInt') for j in range(len(L))]
					for x in OEI:
						self.model.AddBoolAnd(isSame).OnlyEnforceIf(x.Not())
						for j in range(len(L)):
							self.model.Add(isSameInt[j] == 0).OnlyEnforceIf(x.Not())
					for j in range(len(L)):
						self.model.Add(isSameInt[j] == 1).OnlyEnforceIf([isSame[j]] + OEI)
						self.model.Add(isSameInt[j] == 0).OnlyEnforceIf([isSame[j].Not()] + OEI)
						self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[j][0]][L[j][1]]).OnlyEnforceIf([isSame[j]] + OEI)
						self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[j][0]][L[j][1]]).OnlyEnforceIf([isSame[j].Not()] + OEI)
					self.model.Add(countSame[i] == sum(isSameInt)).OnlyEnforceIf(OEI)
				
				extremum = self.model.NewIntVar(0,len(L),'MajorityPropertyExtremumCount')
				if criterion[0][:8] == 'Majority':
					self.model.AddMaxEquality(extremum,countSame)
				else:
					self.model.AddMinEquality(extremum,countSame)
					
				for i in range(len(L)):
					self.model.Add(countSame[i] == extremum).OnlyEnforceIf([criterionBools[i]] + OEI)
					self.model.Add(countSame[i] != extremum).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
			
			case 'ContiguousSum':
				for i in range(len(L)):
					if len(criterion) == 2:
						jRange = range(i,len(L))
					else:
						match criterion[2]:
							case self.LE:
								jRange = range(i,min(i+criterion[3],len(L)))
							case self.EQ:
								jRange = range(i+criterion[3]-1,min(i+criterion[3],len(L)))
							case self.GE:
								jRange = range(i+criterion[3]-1,len(L))
							case self.NE:
								jRange = list(range(i,i+criterion[3]-2)) + list(range(i+criterion[3],len(L)))
					
					mySumVars = []
					
					for j in jRange:
						c = self.model.NewBoolVar('ContiguousSumSelector{:d}-{:d}'.format(i,j))
						mySumVars.append(c)
						self.allVars.append(c)
						self.model.Add(sum(self.cellValues[L[k][0]][L[k][1]] for k in range(i,j+1)) == criterion[1]).OnlyEnforceIf([c] + OEI)
						self.model.Add(sum(self.cellValues[L[k][0]][L[k][1]] for k in range(i,j+1)) != criterion[1]).OnlyEnforceIf([c.Not()] + OEI)
					self.model.AddBoolOr(mySumVars).OnlyEnforceIf([criterionBools[i]] + OEI)
					self.model.AddBoolAnd([x.Not() for x in mySumVars]).OnlyEnforceIf([criterionBools[i].Not()] + OEI)

					for x in OEI:
						self.model.AddBoolAnd(mySumVars).OnlyEnforceIf(x.Not())
						
			case 'Increase'|'Decrease':
				if criterion[1] == 'before':
					self.model.AddBoolAnd(criterionBools[-1].Not()).OnlyEnforceIf(OEI)  # last cell cannot be picked
				else:
					self.model.AddBoolAnd(criterionBools[0].Not()).OnlyEnforceIf(OEI)  # first cell cannot be picked
				for i in range(1,len(L)):
					if criterion[0] == 'Increase':
						myComp = self.cellValues[L[i][0]][L[i][1]] - self.cellValues[L[i-1][0]][L[i-1][1]]
					else:
						myComp = self.cellValues[L[i-1][0]][L[i-1][1]] - self.cellValues[L[i][0]][L[i][1]]
						
					if criterion[1] == 'before':
						myBool = criterionBools[i-1]
					else:
						myBool = criterionBools[i]
						
					self.model.Add(myComp > 0).OnlyEnforceIf([myBool] + OEI)
					self.model.Add(myComp <= 0).OnlyEnforceIf([myBool.Not()] + OEI)
					
			case 'Difference':
				comparator = criterion[2]
				value = criterion[3]
				for i in range(len(L)):
					if type(criterion[1]) is int:
						target = self.cellValues[L[criterion[1]-1][0]][L[criterion[1]-1][1]]
					else:
						if i == 0:
							self.model.AddBoolAnd(criterionBools[0].Not()).OnlyEnforceIf(OEI)
							continue
						else:
							target = self.cellValues[L[i-1][0]][L[i-1][1]]
							
					switch = self.model.NewBoolVar('ConditionDifference')
					for x in OEI:
						self.model.AddBoolAnd(switch).OnlyEnforceIf(x.Not())
						
					match comparator:
						case self.LE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] - target <= value).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(target - self.cellValues[L[i][0]][L[i][1]] <= value).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.AddBoolAnd(switch).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] - target > value).OnlyEnforceIf([criterionBools[i].Not(),switch] + OEI)
							self.model.Add(target - self.cellValues[L[i][0]][L[i][1]] > value).OnlyEnforceIf([criterionBools[i].Not(),switch.Not()] + OEI)
						case self.EQ:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] - target == value).OnlyEnforceIf([criterionBools[i],switch] + OEI)
							self.model.Add(target - self.cellValues[L[i][0]][L[i][1]] == value).OnlyEnforceIf([criterionBools[i],switch.Not()] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] - target != value).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
							self.model.Add(target - self.cellValues[L[i][0]][L[i][1]] != value).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
							self.model.AddBoolAnd(switch).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.GE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] - target >= value).OnlyEnforceIf([criterionBools[i],switch] + OEI)
							self.model.Add(target - self.cellValues[L[i][0]][L[i][1]] >= value).OnlyEnforceIf([criterionBools[i],switch.Not()] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] - target < value).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
							self.model.Add(target - self.cellValues[L[i][0]][L[i][1]] < value).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
							self.model.AddBoolAnd(switch).OnlyEnforceIf([criterionBools[i].Not()] + OEI)
						case self.NE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] - target != value).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(target - self.cellValues[L[i][0]][L[i][1]] != value).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.AddBoolAnd(switch).OnlyEnforceIf([criterionBools[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] - target == value).OnlyEnforceIf([criterionBools[i].Not(),switch] + OEI)
							self.model.Add(target - self.cellValues[L[i][0]][L[i][1]] == value).OnlyEnforceIf([criterionBools[i].Not(),switch.Not()] + OEI)
											
		criteriaBools.insert(criterionNumber,criterionBools)
		criterionNumber = criterionNumber + 1
	
	# Ensure selectionCells[i] is True if and only if each of the underlying criteria is
	for i in range(len(L)):
		self.model.AddBoolAnd([criteriaBools[j][i] for j in range(len(criteriaBools))]).OnlyEnforceIf([selectionCells[i]] + OEI)
		self.model.AddBoolOr([criteriaBools[j][i].Not() for j in range(len(criteriaBools))]).OnlyEnforceIf([selectionCells[i].Not()] + OEI)
		
	return selectionCells

def _partitionRegion(self,L,OEI):
	runNumber = [self.model.NewIntVar(1,len(L),'RegionRunSelectionRunNumber') for i in range(len(L))]
	for x in OEI:
		for i in range(len(L)):
			self.model.Add(runNumber[i] == 1).OnlyEnforceIf(x.Not())
	myRegion = [self.getRegion(L[i][0],L[i][1]) for i in range(len(L))]
	self.model.Add(runNumber[0] == 1).OnlyEnforceIf(OEI)
	maxRegion = 1
	for i in range(1,len(L)):
		if myRegion[i] == myRegion[i-1]:
			self.model.Add(runNumber[i] == runNumber[i-1]).OnlyEnforceIf(OEI)
		else:
			self.model.Add(runNumber[i] == runNumber[i-1]+1).OnlyEnforceIf(OEI)
	return runNumber

def _partitionProperty(self,L,mode,OEI):
	if mode[0:-3] not in self._propertyInitialized:
		getattr(self,'_set'+mode[0:-3])()
	myCells = getattr(self,'cell'+mode[0:-3])
	runNumber = [self.model.NewIntVar(1,len(L),'PropertyRunSelectionRunNumber') for i in range(len(L))]
	propertySwitch = [self.model.NewBoolVar('PropertyRunSwitch') for i in range(len(L))]
	for x in OEI:
		self.model.AddBoolAnd(propertySwitch).OnlyEnforceIf(x.Not())
		for i in range(len(L)):
			self.model.Add(runNumber[i] == 1).OnlyEnforceIf(x.Not())
	self.model.Add(runNumber[0] == 1).OnlyEnforceIf(OEI)
	self.model.AddBoolAnd(propertySwitch[0].Not()).OnlyEnforceIf(OEI)
	for i in range(1,len(L)):
		self.model.Add(myCells[L[i-1][0]][L[i-1][1]] == myCells[L[i][0]][L[i][1]]).OnlyEnforceIf([propertySwitch[i].Not()] + OEI)
		self.model.Add(myCells[L[i-1][0]][L[i-1][1]] != myCells[L[i][0]][L[i][1]]).OnlyEnforceIf([propertySwitch[i]] + OEI)
		self.model.Add(runNumber[i] == runNumber[i-1]).OnlyEnforceIf([propertySwitch[i].Not()] + OEI)
		self.model.Add(runNumber[i] == runNumber[i-1]+1).OnlyEnforceIf([propertySwitch[i]] + OEI)
	return runNumber

def _partitionMonotone(self,L,mode,OEI):
	# This code takes a line and splits it up into monotone runs of increasing or decreasing digits
	runNumber = [self.model.NewIntVar(1,len(L),'UpDownRunSelectionRunNumber') for i in range(len(L))]
	runSwitch = [self.model.NewBoolVar('UpDownRunSwitch') for i in range(len(L))]
	for x in OEI:
		self.model.AddBoolAnd(runSwitch).OnlyEnforceIf(x.Not())
		for i in range(len(L)):
			self.model.Add(runNumber[i] == 1).OnlyEnforceIf(x.Not())
	self.model.Add(runNumber[0] == 1).OnlyEnforceIf(OEI)
	self.model.AddBoolAnd(runSwitch[0].Not()).OnlyEnforceIf(OEI)
	for i in range(1,len(L)):
		if mode == 'AscendingRun':
			self.model.Add(self.cellValues[L[i-1][0]][L[i-1][1]] < self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf([runSwitch[i].Not()] + OEI)
			self.model.Add(self.cellValues[L[i-1][0]][L[i-1][1]] >= self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf([runSwitch[i]] + OEI)	
		else:
			self.model.Add(self.cellValues[L[i-1][0]][L[i-1][1]] > self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf([runSwitch[i].Not()] + OEI)
			self.model.Add(self.cellValues[L[i-1][0]][L[i-1][1]] <= self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf([runSwitch[i]] + OEI)	
		self.model.Add(runNumber[i] == runNumber[i-1]).OnlyEnforceIf([runSwitch[i].Not()] + OEI)
		self.model.Add(runNumber[i] == runNumber[i-1]+1).OnlyEnforceIf([runSwitch[i]] + OEI)
	return runNumber

def _selectCellsInRowCol(self,row,col,rc,selectCriteria):
	
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	L = [(row+i*vStep,col+i*hStep) for i in range(self.boardWidth)]
	selectionCells = self._selectCellsOnLine(L,selectCriteria)
	return selectionCells

	
def _terminateCellsOnLine(self,L,selectTerminator,OEI=[]):
	
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
	for x in OEI:
			self.model.AddBoolAnd(terminatorCells).OnlyEnforceIf(x.Not())
	terminatorBools = []
	terminatorNumber = 0
	for terminator in selectTerminator:
		termBools = [self.model.NewBoolVar('TermCriterion{:d}{:d}'.format(terminatorNumber,i)) for i in range(len(L))]
		self.allVars = self.allVars + termBools
		for x in OEI:
			self.model.AddBoolAnd(termBools).OnlyEnforceIf(x.Not())
		match terminator[0]:
			case 'Last':
				self.model.AddBoolAnd([termBools[j].Not() for j in range(len(L)-1)]).OnlyEnforceIf(OEI)
				self.model.AddBoolAnd(termBools[-1]).OnlyEnforceIf(OEI)
			case 'Fixed':
				self.model.AddBoolAnd(termBools[terminator[1]-1]).OnlyEnforceIf(OEI)
				self.model.AddBoolAnd([termBools[j].Not() for j in range(len(L)) if j != terminator[1]-1]).OnlyEnforceIf(OEI)
			case 'SumReached':
				self.model.Add(self.cellValues[L[0][0]][L[0][1]] >= terminator[1]).OnlyEnforceIf([termBools[0]]+OEI)
				self.model.Add(self.cellValues[L[0][0]][L[0][1]] < terminator[1]).OnlyEnforceIf([termBools[0].Not()]+OEI)
				for i in range(1,len(L)):
					self.model.Add(sum(self.cellValues[L[j][0]][L[j][1]] for j in range(i)) < terminator[1]).OnlyEnforceIf([termBools[i]] + OEI)
					self.model.Add(sum(self.cellValues[L[j][0]][L[j][1]] for j in range(i+1)) >= terminator[1]).OnlyEnforceIf([termBools[i]] + OEI)
					c = self.model.NewBoolVar('switch')
					self.model.Add(sum(self.cellValues[L[j][0]][L[j][1]] for j in range(i)) >= terminator[1]).OnlyEnforceIf([c,termBools[i].Not()] + OEI)
					self.model.Add(sum(self.cellValues[L[j][0]][L[j][1]] for j in range(i+1)) < terminator[1]).OnlyEnforceIf([c.Not(),termBools[i].Not()] + OEI)
					self.model.AddBoolAnd(c).OnlyEnforceIf(termBools[i] + OEI)
					self.model.AddBoolAnd(OEI).OnlyEnforceIf(c)
			case 'DigitReached':
				for i in range(len(L)):
					self.model.Add(self.cellValues[L[i][0]][L[i][1]] == terminator[1]).OnlyEnforceIf([termBools[i]] + OEI)
					self.model.Add(self.cellValues[L[i][0]][L[i][1]] != terminator[1]).OnlyEnforceIf([termBools[i].Not()] + OEI)
			case 'DigitSetReached':
				instanceCount = [self.model.NewIntVar(0,len(L),'digitInstanceCount') for j in range(len(L))]
				isInstance = [self.model.NewBoolVar('digitInstanceTest') for j in range(len(L))]
				self.allVars = self.allVars + instanceCount + isInstance
				for x in OEI:
					for j in range(len(L)):
						self.model.Add(instanceCount[j] == 0).OnlyEnforceIf(x.Not())
					self.model.AddBoolAnd(isInstance).OnlyEnforceIf(x.Not())
				for i in range(len(L)):
					digitVars = [self.model.NewBoolVar('digitPicker') for j in range(len(terminator[1]))]
					self.allVars = self.allVars + digitVars
					for x in OEI:
						self.model.AddBoolAnd(digitVars).OnlyEnforceIf(x.Not())
					for j in range(len(terminator[1])):
						self.model.Add(self.cellValues[L[i][0]][L[i][1]] == terminator[1][j]).OnlyEnforceIf([digitVars[j]] + OEI)
						self.model.Add(self.cellValues[L[i][0]][L[i][1]] != terminator[1][j]).OnlyEnforceIf([digitVars[j].Not()] + OEI)
						self.model.AddBoolAnd(isInstance[i]).OnlyEnforceIf([digitVars[j]] + OEI)
					self.model.AddBoolAnd(isInstance[i].Not()).OnlyEnforceIf([digitVars[j].Not() for j in range(len(terminator[1]))] + OEI)
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf([isInstance[0]] + OEI)
				self.model.Add(instanceCount[0] == 0).OnlyEnforceIf([isInstance[0].Not()] + OEI)
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i] == instanceCount[i-1]+1).OnlyEnforceIf([isInstance[i]] + OEI)
					self.model.Add(instanceCount[i] == instanceCount[i-1]).OnlyEnforceIf([isInstance[i].Not()] + OEI)
				self.model.Add(instanceCount[0] == terminator[2]).OnlyEnforceIf([termBools[0]] + OEI)
				self.model.Add(instanceCount[0] < terminator[2]).OnlyEnforceIf([termBools[0].Not()] + OEI)
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i-1] < terminator[2]).OnlyEnforceIf([termBools[i]] + OEI)
					self.model.Add(instanceCount[i] == terminator[2]).OnlyEnforceIf([termBools[i]] + OEI)
					c = self.model.NewBoolVar('switch')
					self.allVars = self.allVars + [c]
					self.model.AddBoolAnd(OEI).OnlyEnforceIf(c)
					self.model.Add(instanceCount[i-1] >= terminator[2]).OnlyEnforceIf([c,termBools[i].Not()] + OEI)
					self.model.Add(instanceCount[i] < terminator[2]).OnlyEnforceIf([c.Not(),termBools[i].Not()] + OEI)
					self.model.AddBoolAnd(c).OnlyEnforceIf([termBools[i]] + OEI)
			case 'ParityChangeReached' | 'EntropyChangeReached' | 'ModularChangeReached' | 'PrimalityChangeReached' | 'DigitSizeChangeReached' |'ParityRepeatReached' | 'EntropyRepeatReached' | 'ModularRepeatReached' | 'PrimalityRepeatReached' | 'DigitSizeRepeatReached':
				if terminator[0][0:-13] not in self._propertyInitialized:
					getattr(self,'_set'+terminator[0][0:-13])()
				myTransition = terminator[0][-13:-7] # 'Change' or 'Repeat'
				instanceCount = [self.model.NewIntVar(0,len(L),terminator[0][0:-13]+'ChangeInstanceCount') for j in range(len(L))]
				isInstance = [self.model.NewBoolVar(terminator[0][0:-13]+'ChangeInstanceTest') for j in range(len(L))]
				self.allVars = self.allVars + instanceCount + isInstance
				for x in OEI:
					for j in range(len(L)):
						self.model.Add(instanceCount[j] == 0).OnlyEnforceIf(x.Not())
					self.model.AddBoolAnd(isInstance).OnlyEnforceIf(x.Not())
				self.model.AddBoolAnd(isInstance[0].Not())  # first cell cannot be a change
				myCells = getattr(self,'cell'+terminator[0][0:-13])
				for i in range(1,len(L)):
					if myTransition == 'Change':
						self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf([isInstance[i]] + OEI)
						self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf([isInstance[i].Not()] + OEI)
					elif myTransition == 'Repeat':
						self.model.Add(myCells[L[i][0]][L[i][1]] == myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf([isInstance[i]] + OEI)
						self.model.Add(myCells[L[i][0]][L[i][1]] != myCells[L[i-1][0]][L[i-1][1]]).OnlyEnforceIf([isInstance[i].Not()] + OEI)
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf([isInstance[0]] + OEI)
				self.model.Add(instanceCount[0] == 0).OnlyEnforceIf([isInstance[0].Not()] + OEI)
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i] == instanceCount[i-1]+1).OnlyEnforceIf([isInstance[i]] + OEI)
					self.model.Add(instanceCount[i] == instanceCount[i-1]).OnlyEnforceIf([isInstance[i].Not()] + OEI)
				self.model.Add(instanceCount[0] == terminator[1]).OnlyEnforceIf([termBools[0]] + OEI)
				self.model.Add(instanceCount[0] < terminator[1]).OnlyEnforceIf([termBools[0].Not()] + OEI)
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i-1] < terminator[1]).OnlyEnforceIf([termBools[i]] + OEI)
					self.model.Add(instanceCount[i] == terminator[1]).OnlyEnforceIf([termBools[i]] + OEI)
					c = self.model.NewBoolVar('switch')
					self.allVars = self.allVars + [c]
					self.model.AddBoolAnd(OEI).OnlyEnforceIf(c)
					self.model.Add(instanceCount[i-1] >= terminator[1]).OnlyEnforceIf([c,termBools[i].Not()] + OEI)
					self.model.Add(instanceCount[i] < terminator[1]).OnlyEnforceIf([c.Not(),termBools[i].Not()] + OEI)
					self.model.AddBoolAnd(c).OnlyEnforceIf([termBools[i]] + OEI)
			case 'Indexed':
				if type(terminator[1]) is int:
					depthIndices = [terminator[1]-1]
				else:
					depthIndices = [x-1 for x in terminator[1]]
				depthVars = [self.model.NewBoolVar('TerminationSelectionCellRow') for j in range(len(depthIndices))]
				self.allVars = self.allVars + depthVars
				self.model.AddBoolOr(depthVars).OnlyEnforceIf(OEI)
				for x in OEI:
					self.model.AddBoolAnd(depthVars).OnlyEnforceIf(x.Not())

				for i in range(len(L)):
					for j in range(len(depthVars)):
						self.model.Add(self.cellValues[L[depthIndices[j]][0]][L[depthIndices[j]][1]] == i+1).OnlyEnforceIf([termBools[i], depthVars[j]] + OEI)
						self.model.Add(self.cellValues[L[depthIndices[j]][0]][L[depthIndices[j]][1]] != i+1).OnlyEnforceIf([termBools[i], depthVars[j].Not()] + OEI)
						
				if len(terminator) > 2:
					if terminator[2]== 'Smallest':
						for j in range(len(depthIndices)):
							for k in range(len(depthIndices)):
								if k != j:
									self.model.Add(self.cellValues[L[depthIndices[j]][0]][L[depthIndices[j]][1]] < self.cellValues[L[depthIndices[k]][0]][L[depthIndices[k]][1]]).OnlyEnforceIf([depthVars[j]] + OEI)
					elif terminator[2] == 'Largest':
						for j in range(len(depthIndices)):
							for k in range(len(depthIndices)):
								if k != j:
									self.model.Add(self.cellValues[L[depthIndices[j]][0]][L[depthIndices[j]][1]] > self.cellValues[L[depthIndices[k]][0]][L[depthIndices[k]][1]]).OnlyEnforceIf([depthVars[j]] + OEI)
			case 'RepeatReached':
				isRepeat = [self.model.NewBoolVar('TerminationRepeatReachedTest') for j in range(len(L))]
				repeatCount = [self.model.NewIntVar(0,len(L),'TerminationRepeatReachedCount') for j in range(len(L))]
				for x in OEI:
					self.model.AddBoolAnd(isRepeat).OnlyEnforceIf(x.Not())
					for j in range(len(L)):
						self.model.Add(repeatCount == 0).OnlyEnforceIf(x.Not())
				self.model.AddBoolAnd(isRepeat[0].Not()).OnlyEnforceIf(OEI)
				self.model.Add(repeatCount[0] == 0).OnlyEnforceIf(OEI)
				self.model.AddBoolAnd(termBools[0].Not()).OnlyEnforceIf(OEI)

				if terminator[1] == 'Last':
					myTarget = self.model.NewIntVar(0,len(L),'TerminationRepeatReachedMaxCount')
					self.model.AddMaxEquality(myTarget,repeatCount)
				else:
					myTarget = terminator[1]
				
				for j in range(1,len(L)):
					isEqual = [self.model.NewBoolVar('TerminationRepeatReachedEqualityChecker') for k in range(j)]
					for x in OEI:
						self.model.AddBoolAnd(isEqual).OnlyEnforceIf(x.Not())
					for k in range(j):
						self.model.Add(self.cellValues[L[k][0]][L[k][1]] == self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([isEqual[k]] + OEI)
						self.model.Add(self.cellValues[L[k][0]][L[k][1]] != self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([isEqual[k].Not()] + OEI)
					self.model.AddBoolOr(isEqual).OnlyEnforceIf([isRepeat[j]] + OEI)
					self.model.AddBoolAnd([x.Not() for x in isEqual]).OnlyEnforceIf([isRepeat[j].Not()] + OEI)
					self.model.Add(repeatCount[j] == repeatCount[j-1]+1).OnlyEnforceIf([isRepeat[j]] + OEI)
					self.model.Add(repeatCount[j] == repeatCount[j-1]).OnlyEnforceIf([isRepeat[j].Not()] + OEI)
				
					self.model.Add(repeatCount[j] == myTarget).OnlyEnforceIf([termBools[j]] + OEI)
					self.model.AddBoolAnd(isRepeat[j]).OnlyEnforceIf([termBools[j]] + OEI)
					self.model.Add(repeatCount[j] != myTarget).OnlyEnforceIf([termBools[j].Not(),isRepeat[j]] + OEI)
			case 'RelatedDigit':
				base = terminator[1]-1
				comparator = terminator[2]
				scale = terminator[3]
				shift = terminator[4]
				instance = terminator[5]
				
				instanceCount = [self.model.NewIntVar(0,len(L),'RelatedDigitInstanceCount') for j in range(len(L))]
				isInstance = [self.model.NewBoolVar('RelatedDigitInstanceTest') for j in range(len(L))]
				for x in OEI:
					for j in range(len(L)):
						self.model.Add(instanceCount[j] == 0).OnlyEnforceIf(x.Not())
					self.model.AddBoolAnd(isInstance).OnlyEnforceIf(x.Not())
				
				for i in range(len(L)):
					match comparator:
						case self.LE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] <= scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([isInstance[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] > scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([isInstance[i].Not()] + OEI)
						case self.EQ:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] == scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([isInstance[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] != scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([isInstance[i].Not()] + OEI)
						case self.GE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] >= scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([isInstance[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] < scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([isInstance[i].Not()] + OEI)
						case self.NE:
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] != scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([isInstance[i]] + OEI)
							self.model.Add(self.cellValues[L[i][0]][L[i][1]] == scale*self.cellValues[L[base][0]][L[base][1]] + shift).OnlyEnforceIf([isInstance[i].Not()] + OEI)
							
				self.model.Add(instanceCount[0] == 1).OnlyEnforceIf([isInstance[0]] + OEI)
				self.model.Add(instanceCount[0] == 0).OnlyEnforceIf([isInstance[0].Not()] + OEI)
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i] == instanceCount[i-1] + 1).OnlyEnforceIf([isInstance[i]] + OEI)
					self.model.Add(instanceCount[i] == instanceCount[i-1]).OnlyEnforceIf([isInstance[i].Not()] + OEI)
					
				if instance == 1:
					self.model.AddBoolAnd(termBools[0]).OnlyEnforceIf([isInstance[0]] + OEI)
					self.model.AddBoolAnd(termBools[0].Not()).OnlyEnforceIf([isInstance[0].Not()] + OEI)
				else:
					self.model.AddBoolAnd([termBools[0].Not()] + OEI)
				
				for i in range(1,len(L)):
					self.model.Add(instanceCount[i] == instance).OnlyEnforceIf([termBools[i]] + OEI)
					self.model.AddBoolAnd(isInstance[i]).OnlyEnforceIf([termBools[i]] + OEI)
					self.model.Add(instanceCount[i] != instance).OnlyEnforceIf([termBools[i].Not(),isInstance[i]] + OEI)
			case 'ModelVariable':
				for i in range(len(L)):
					self.model.Add(terminator[1] == i+1).OnlyEnforceIf([termBools[i]] + OEI)
					self.model.Add(terminator[1] != i+1).OnlyEnforceIf([termBools[i].Not()] + OEI)
									
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
	
def _evaluateHangingClues(self,partial,terminatorCells,value,terminateOn,includeTerminator,comparator=None,forceTermination=True,OEI=[],failedTerminationBehavior='partial'):
	# This does the final configuration of a hanging clue, just extracting the ugly stuff away from the individual functions
	
	if forceTermination == True:
		# One of the existing cells must terminate per the specified conditions
		self.model.AddBoolOr(terminatorCells).OnlyEnforceIf(OEI)
	else:
		if failedTerminationBehavior == 'partial':
			# Otherwise we create a new final terminator as a default. If any other terminators are true, we want
			# this to be false, but otherwise it becomes true.
			newFinalTerminator = self.model.NewBoolVar('AlternateTerminator')
			self.allVars.append(newFinalTerminator)
			self.model.AddBoolAnd(newFinalTerminator).OnlyEnforceIf([x.Not() for x in terminatorCells]+OEI)
			for x in terminatorCells:
				self.model.AddBoolAnd(newFinalTerminator.Not()).OnlyEnforceIf([x]+OEI)
			self.model.AddBoolAnd(OEI).OnlyEnforceIf(newFinalTerminator)
			
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
		else:
			match comparator:
				case self.LE:
					self.model.Add(value >= 0).OnlyEnforceIf(OEI + [x.Not() for x in terminatorCells])
				case self.GE:
					self.model.Add(value <= 0).OnlyEnforceIf(OEI + [x.Not() for x in terminatorCells])
				case self.NE:
					self.model.Add(value != 0).OnlyEnforceIf(OEI + [x.Not() for x in terminatorCells])
				case _:
					self.model.Add(value == 0).OnlyEnforceIf(OEI + [x.Not() for x in terminatorCells])
		
	if terminateOn == 'First':
		if includeTerminator:
			match comparator:
				case self.LE:
					self.model.Add(partial[0] <= value).OnlyEnforceIf([terminatorCells[0]]+OEI)
				case self.GE:
					self.model.Add(partial[0] >= value).OnlyEnforceIf([terminatorCells[0]]+OEI)
				case self.NE:
					self.model.Add(partial[0] != value).OnlyEnforceIf([terminatorCells[0]]+OEI)
				case _:
					self.model.Add(partial[0] == value).OnlyEnforceIf([terminatorCells[0]]+OEI)
		else:
			if type(value) is int and value == 0:
				pass
			else:
				self.model.AddBoolAnd(terminatorCells[0].Not()).OnlyEnforceIf([terminatorCells[0]]+OEI)
		# Note: we are changing the loop limits to range over terminatorCells, since if includeTerminator is 
		# False and forceTermination is False, terminatorCells may be one longer than partial. However, in
		# this case, there is no risk of over-running partial, since we'll be in the "else" clause below,
		# where the indices are one less that the 
		for i in range(1,len(terminatorCells)):
			if includeTerminator:
				match comparator:
					case self.LE:
						self.model.Add(partial[i] <= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)] + OEI)
					case self.GE:
						self.model.Add(partial[i] >= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)] + OEI)
					case self.NE:
						self.model.Add(partial[i] != value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)] + OEI)
					case _:
						self.model.Add(partial[i] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)] + OEI)
			else:
				match comparator:
					case self.LE:
						self.model.Add(partial[i-1] <= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)] + OEI)
					case self.GE:
						self.model.Add(partial[i-1] >= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)] + OEI)
					case self.NE:
						self.model.Add(partial[i-1] != value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)] + OEI)
					case _:
						self.model.Add(partial[i-1] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)] + OEI)
	elif terminateOn == 'Last':
		for i in range(len(terminatorCells)):
			if includeTerminator:
				match comparator:
					case self.LE:
						self.model.Add(partial[i] <= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))] + OEI)
					case self.GE:
						self.model.Add(partial[i] >= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))] + OEI)
					case self.NE:
						self.model.Add(partial[i] != value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))] + OEI)
					case _:
						self.model.Add(partial[i] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))] + OEI)
			else:
				match comparator:
					case self.LE:
						self.model.Add(partial[i-1] <= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))] + OEI)
					case self.GE:
						self.model.Add(partial[i-1] >= value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))] + OEI)
					case self.NE:
						self.model.Add(partial[i-1] != value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))] + OEI)
					case _:
						self.model.Add(partial[i-1] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i+1,len(partial))] + OEI)
				
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
						self.model.Add(partial[i] <= value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]] + OEI)
					case self.GE:
						self.model.Add(partial[i] >= value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]] + OEI)
					case self.NE:
						self.model.Add(partial[i] != value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]] + OEI)
					case _:
						self.model.Add(partial[i] == value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]] + OEI)
			else:
				match comparator:
					case self.LE:
						self.model.Add(partial[i-1] <= value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]] + OEI)
					case self.GE:
						self.model.Add(partial[i-1] >= value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]] + OEI)
					case self.NE:
						self.model.Add(partial[i-1] != value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]] + OEI)
					case _:
						self.model.Add(partial[i-1] == value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]] + OEI)
						
			self.model.AddBoolAnd(terminatorCells[i]).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i].Not()] + OEI)
			  # ensures this varBitmap cannot be chosen if terminatorCells is not set
			for x in OEI:
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf(x.Not())
			  # peg varBitmap in case this line is not used
			  
			for j in range(i):
				c = self.model.NewBoolVar('solutionPickerSwitch')
				self.allVars = self.allVars + [c]
				match comparator:
					case self.LE:
						self.model.Add(partial[j] > value).OnlyEnforceIf(varBitmap[i] + [c] + OEI)
					case self.GE:
						self.model.Add(partial[j] < value).OnlyEnforceIf(varBitmap[i] + [c] + OEI)
					case self.NE:
						self.model.Add(partial[j] == value).OnlyEnforceIf(varBitmap[i] + [c] + OEI)
					case _:
						self.model.Add(partial[j] != value).OnlyEnforceIf(varBitmap[i] + [c] + OEI)
				self.model.AddBoolAnd(terminatorCells[j].Not()).OnlyEnforceIf(varBitmap[i] + [c.Not()] + OEI)
				self.model.AddBoolAnd(c.Not()).OnlyEnforceIf(varBitmap[i] + [terminatorCells[j].Not()] + OEI)
				for k in range(len(terminatorCells)):
					if k != i:
						self.model.AddBoolAnd(c).OnlyEnforceIf(varBitmap[k] + OEI)
				self.model.AddBoolAnd(OEI).OnlyEnforceIf(c)
				  # If any of the OEI variables are false, forces c to be false.
				  
def _partitionLine(self,L,criterion):
	# Splits line into runs
	match criterion[0]:
		case 'ParityRun'|'EntropyRun'|'ModularRun'|'PrimalityRun'|'DigitSizeRun':
			runNumber = self._partitionProperty(L,criterion[0],[])
		case 'AscendingRun'|'DescendingRun':
			runNumber = self._partitionMonotone(L,criterion[0],[])
		case 'Region':
			runNumber = self._partitionRegion(L,[])
	return runNumber	
				