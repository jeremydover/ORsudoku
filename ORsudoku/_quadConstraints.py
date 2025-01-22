def setQuadruple(self,row,col=-1,values=-1):
	if col == -1:
		T = self._procCell(row)
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
			bit1 = self.model.NewBoolVar('Quadruple1Row{:d}Col{:d}Value{:d}'.format(row,col,x))
			bit2 = self.model.NewBoolVar('Quadruple2Row{:d}Col{:d}Value{:d}'.format(row,col,x))
			
			# If bitDouble is true, then we peg bit2 to true, and use bit 1 to determine which diagonal hosts the digits
			self.model.AddBoolAnd([bit2]).OnlyEnforceIf([bitDouble])
			self.model.Add(self.cellValues[row][col] == x).OnlyEnforceIf([bitDouble,bit1])
			self.model.Add(self.cellValues[row+1][col+1] == x).OnlyEnforceIf([bitDouble,bit1])
			self.model.Add(self.cellValues[row][col+1] == x).OnlyEnforceIf([bitDouble,bit1.Not()])
			self.model.Add(self.cellValues[row+1][col] == x).OnlyEnforceIf([bitDouble,bit1.Not()])
			
			# If bitDouble is false, then we set the appropriate cell to x, and set the one opposite it to be not x
			self.model.Add(self.cellValues[row][col] == x).OnlyEnforceIf([bitDouble.Not(),bit1,bit2])
			self.model.Add(self.cellValues[row+1][col+1] != x).OnlyEnforceIf([bitDouble.Not(),bit1,bit2])
			self.model.Add(self.cellValues[row][col+1] == x).OnlyEnforceIf([bitDouble.Not(),bit1,bit2.Not()])
			self.model.Add(self.cellValues[row+1][col] != x).OnlyEnforceIf([bitDouble.Not(),bit1,bit2.Not()])
			self.model.Add(self.cellValues[row+1][col+1] == x).OnlyEnforceIf([bitDouble.Not(),bit1.Not(),bit2.Not()])
			self.model.Add(self.cellValues[row][col] != x).OnlyEnforceIf([bitDouble.Not(),bit1.Not(),bit2.Not()])
			self.model.Add(self.cellValues[row+1][col] == x).OnlyEnforceIf([bitDouble.Not(),bit1.Not(),bit2])
			self.model.Add(self.cellValues[row][col+1] != x).OnlyEnforceIf([bitDouble.Not(),bit1.Not(),bit2])
			
			if values.count(x) == 2:
				# If the digit actually appears twice in the list, force bitDouble to be true
				self.model.AddBoolAnd([bitDouble])					
				
def setQuadrupleArray(self,cells):
	for x in cells: self.setQuadruple(x)

def setQuadSum(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
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
		(row,col) = self._procCell(row)
	if 'Battenburg' not in self._constraintInitialized:
		self.battenburgCells = [(row,col)]
		self._constraintInitialized.append('Battenburg')
	else:
		self.battenburgCells.append((row,col))
		
	if 'Parity' not in self._propertyInitialized:
		self._setParity()
		
	# Now that we can track parity globally, only need to check that the three pairs: top, right, and bottom are different parity.
	# This ensures either OE  or  EO
	#                     EO      OE
	self.model.Add(self.cellParity[row][col] != self.cellParity[row][col+1])
	self.model.Add(self.cellParity[row][col+1] != self.cellParity[row+1][col+1])
	self.model.Add(self.cellParity[row+1][col] != self.cellParity[row+1][col+1])
			
def setBattenburgArray(self,cells):
	for x in cells: self.setBattenburg(x)
		
def setBattenburgNegative(self):
	if 'Battenburg' not in self._constraintInitialized:
		self.battenburgCells = []
		self._constraintInitialized.append('Battenburg')
	self._constraintNegative.append('Battenburg')
	
	if 'Parity' not in self._propertyInitialized:
		self._setParity()
		
def setAntiBattenburg(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
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
	
def _applyBattenburgNegative(self):
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1):
			if (i,j) not in self.battenburgCells:
				self.setAntiBattenburg(i,j)

def setEntropyQuad(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	# A 2x2 square of cells is entropic if it includes a low, middle, and high digit
	if 'EntropyQuad' not in self._constraintInitialized:
		self.entropyQuadCells = [(row,col)]
		self._constraintInitialized.append('EntropyQuad')
	else:
		self.entropyQuadCells.append((row,col))
		
	if 'Entropy' not in self._propertyInitialized:
		self._setEntropy()
	
	self.model.AddForbiddenAssignments([self.cellEntropy[row][col],self.cellEntropy[row][col+1],self.cellEntropy[row+1][col],self.cellEntropy[row+1][col+1]],[(0,0,0,0),(1,1,1,1),(2,2,2,2),(0,0,0,1),(0,0,1,0),(0,1,0,0),(1,0,0,0),(0,0,0,2),(0,0,2,0),(0,2,0,0),(2,0,0,0),(1,1,1,0),(1,1,0,1),(1,0,1,1),(0,1,1,1),(1,1,1,2),(1,1,2,1),(1,2,1,1),(2,1,1,1),(2,2,2,0),(2,2,0,2),(2,0,2,2),(0,2,2,2),(2,2,2,1),(2,2,1,2),(2,1,2,2),(1,2,2,2),(0,0,1,1),(0,0,2,2),(1,1,0,0),(1,1,2,2),(2,2,0,0),(2,2,1,1),(0,1,0,1),(0,2,0,2),(1,0,1,0),(1,2,1,2),(2,0,2,0),(2,1,2,1),(0,1,1,0),(0,2,2,0),(1,0,0,1),(1,2,2,1),(2,0,0,2),(2,1,1,2)])
	
def setEntropyQuadArray(self,inlist):
	for x in inlist: self.setEntropyQuad(x)
	
def setEntropyQuadNegative(self):
	if 'EntropyQuad' not in self._constraintInitialized:
		self.entropyQuadCells = []
		self._constraintInitialized.append('EntropyQuad')
	
	if 'Entropy' not in self._propertyInitialized:
		self._setEntropy()
		
	self._constraintNegative.append('EntropyQuad')

def setAntiEntropyQuad(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
		
	if 'Entropy' not in self._propertyInitialized:
		self._setEntropy()
	
	self.model.AddAllowedAssignments([self.cellEntropy[row][col],self.cellEntropy[row][col+1],self.cellEntropy[row+1][col],self.cellEntropy[row+1][col+1]],[(0,0,0,0),(1,1,1,1),(2,2,2,2),(0,0,0,1),(0,0,1,0),(0,1,0,0),(1,0,0,0),(0,0,0,2),(0,0,2,0),(0,2,0,0),(2,0,0,0),(1,1,1,0),(1,1,0,1),(1,0,1,1),(0,1,1,1),(1,1,1,2),(1,1,2,1),(1,2,1,1),(2,1,1,1),(2,2,2,0),(2,2,0,2),(2,0,2,2),(0,2,2,2),(2,2,2,1),(2,2,1,2),(2,1,2,2),(1,2,2,2),(0,0,1,1),(0,0,2,2),(1,1,0,0),(1,1,2,2),(2,2,0,0),(2,2,1,1),(0,1,0,1),(0,2,0,2),(1,0,1,0),(1,2,1,2),(2,0,2,0),(2,1,2,1),(0,1,1,0),(0,2,2,0),(1,0,0,1),(1,2,2,1),(2,0,0,2),(2,1,1,2)])
	
def setAntiEntropyQuadArray(self,inlist):
	for x in inlist: self.setAntiEntropyQuad(x)

def _applyEntropyQuadNegative(self):
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1):
			if (i,j) not in self.entropyQuadCells:
				self.setAntiEntropyQuad(i,j)
				
def setModularQuad(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	# A 2x2 square of cells is entropic if it includes a low, middle, and high digit
	if 'ModularQuad' not in self._constraintInitialized:
		self.modularQuadCells = [(row,col)]
		self._constraintInitialized.append('ModularQuad')
	else:
		self.modularQuadCells.append((row,col))
		
	if 'Modular' not in self._propertyInitialized:
		self._setModular()
	
	self.model.AddForbiddenAssignments([self.cellModular[row][col],self.cellModular[row][col+1],self.cellModular[row+1][col],self.cellModular[row+1][col+1]],[(3,3,3,3),(1,1,1,1),(2,2,2,2),(3,3,3,1),(3,3,1,3),(3,1,3,3),(1,3,3,3),(3,3,3,2),(3,3,2,3),(3,2,3,3),(2,3,3,3),(1,1,1,3),(1,1,3,1),(1,3,1,1),(3,1,1,1),(1,1,1,2),(1,1,2,1),(1,2,1,1),(2,1,1,1),(2,2,2,3),(2,2,3,2),(2,3,2,2),(3,2,2,2),(2,2,2,1),(2,2,1,2),(2,1,2,2),(1,2,2,2),(3,3,1,1),(3,3,2,2),(1,1,3,3),(1,1,2,2),(2,2,3,3),(2,2,1,1),(3,1,3,1),(3,2,3,2),(1,3,1,3),(1,2,1,2),(2,3,2,3),(2,1,2,1),(3,1,1,3),(3,2,2,3),(1,3,3,1),(1,2,2,1),(2,3,3,2),(2,1,1,2)])
	
def setModularQuadArray(self,inlist):
	for x in inlist: self.setModularQuad(x)
	
def setModularQuadNegative(self):
	if 'ModularQuad' not in self._constraintInitialized:
		self.modularQuadCells = []
		self._constraintInitialized.append('ModularQuad')
	
	if 'Modular' not in self._propertyInitialized:
		self._setModular()
		
	self._constraintNegative.append('ModularQuad')

def setAntiModularQuad(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
		
	if 'Modular' not in self._propertyInitialized:
		self._setModular()
	
	self.model.AddAllowedAssignments([self.cellModular[row][col],self.cellModular[row][col+1],self.cellModular[row+1][col],self.cellModular[row+1][col+1]],[(3,3,3,3),(1,1,1,1),(2,2,2,2),(3,3,3,1),(3,3,1,3),(3,1,3,3),(1,3,3,3),(3,3,3,2),(3,3,2,3),(3,2,3,3),(2,3,3,3),(1,1,1,3),(1,1,3,1),(1,3,1,1),(3,1,1,1),(1,1,1,2),(1,1,2,1),(1,2,1,1),(2,1,1,1),(2,2,2,3),(2,2,3,2),(2,3,2,2),(3,2,2,2),(2,2,2,1),(2,2,1,2),(2,1,2,2),(1,2,2,2),(3,3,1,1),(3,3,2,2),(1,1,3,3),(1,1,2,2),(2,2,3,3),(2,2,1,1),(3,1,3,1),(3,2,3,2),(1,3,1,3),(1,2,1,2),(2,3,2,3),(2,1,2,1),(3,1,1,3),(3,2,2,3),(1,3,3,1),(1,2,2,1),(2,3,3,2),(2,1,1,2)])
	
def setAntiModularQuadArray(self,inlist):
	for x in inlist: self.setAntiEntropyQuad(x)

def _applyModularQuadNegative(self):
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1):
			if (i,j) not in self.modularQuadCells:
				self.setAntiModularQuad(i,j)

def _initializeParityQuad(self):
	if 'ParityQuad' not in self._constraintInitialized:
		self._constraintInitialized.append('ParityQuad')
		self.parityQuadCells = []
		self.parityQuadExcluded = [0,4]

	if 'Parity' not in self._propertyInitialized:
		self._setParity()

def setParityQuad(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	self._initializeParityQuad()
	self.parityQuadCells.append((row,col))
	
	for k in self.parityQuadExcluded:
		self.model.Add(sum(self.cellParity[row+i][col+j] for i in range(2) for j in range(2)) != k)

def setParityQuadArray(self,inlist):
	for x in inlist: self.setParityQuad(x)
	
def setParityQuadNegative(self):
	self._initializeParityQuad()
	self._constraintNegative.append('ParityQuad')

def setAntiParityQuad(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	self._initializeParityQuad()
		
	varBitmap = self._varBitmap('AntiParityQuad',len(self.parityQuadExcluded))
	for k in range(len(self.parityQuadExcluded)):
		self.model.Add(sum(self.cellParity[row+i][col+j] for i in range(2) for j in range(2)) == self.parityQuadExcluded[k]).OnlyEnforceIf(varBitmap[k])
			
def setAntiParityQuadArray(self,inlist):
	for x in inlist: self.setAntiParityQuad(x)

def _applyParityQuadNegative(self):
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1):
			if (i,j) not in self.parityQuadCells:
				self.setAntiParityQuad(i,j)
				
def setParityQuadExclusions(self,inlist=[0,4]):
	self._initializeParityQuad()
	self.parityQuadExcluded = inlist

def _initializeEntropyBattenburg(self):
	if 'EntropyBattenburg' not in self._constraintInitialized:
		self.entropyBattenburgCells = []
		self._constraintInitialized.append('EntropyBattenburg')
		
	if 'Entropy' not in self._propertyInitialized:
		self._setEntropy()
		
def setEntropyBattenburg(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	# A 2x2 square of cells is an entropy battenburg if no two adjacent cells on the quad have the same rank
	self._initializeEntropyBattenburg()
	self.entropyBattenburgCells.append((row,col))
	
	self.model.Add(self.cellEntropy[row][col] != self.cellEntropy[row][col+1])
	self.model.Add(self.cellEntropy[row][col+1] != self.cellEntropy[row+1][col+1])
	self.model.Add(self.cellEntropy[row+1][col+1] != self.cellEntropy[row+1][col])
	self.model.Add(self.cellEntropy[row+1][col] != self.cellEntropy[row][col])
	
def setEntropyBattenburgArray(self,inlist):
	for x in inlist: self.setEntropyBattenburg(x)
	
def setAntiEntropyBattenburg(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	self._initializeEntropyBattenburg()
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
	self._initializeEntropyBattenburg()
	self._constraintNegative.append('EntropyBattenburg')
	
def _applyEntropyBattenburgNegative(self):
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1):
			if (i,j) not in self.entropyBattenburgCells:
				self.setAntiEntropyBattenburg(i,j)
				
def setQuadMaxArrow(self,row,col=-1,dir1=-1,dir2=-1):
	# row,col defines the 2x2 to which the arrow applies
	# dir1,dir2 defines which cell the arrow points to
	if col == -1:
		(row,col,dir1,dir2) = self._procCell(row)
	
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
		(row,col,value) = self._procCell(row)

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
	if 'Parity' not in self._propertyInitialized:
		self._setParity()
		
	if col == -1:
		T = self._procCell(row)
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
		(row,col,value) = self._procCell(row)
	if 'ConsecutiveQuad' not in self._constraintInitialized:
		self.consecutiveQuadCells = [(row,col,hv)]
		self._constraintInitialized.append('ConsecutiveQuad')
	else:
		self.consecutiveQuadCells.append((row,col,hv))

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
		(row,col) = self._procCell(row)
	self.setConsecutiveQuad(row,col,sudoku.White)

def setConsecutiveQuadWhiteArray(self,cells):
	for x in cells: self.setConsecutiveQuadWhite(x)
	
def setConsecutiveQuadBlack(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	self.setConsecutiveQuad(row,col,sudoku.Black)

def setConsecutiveQuadBlackArray(self,cells):
	for x in cells: self.setConsecutiveQuadBlack(x)	
	
def setConsecutiveQuadArray(self,cells):
	cellList = self._procCellList(cells)
	for x in cellList:
		if x[2] == sudoku.White:
			self.setConsecutiveQuadWhite(x[0],x[1])
		else:
			self.setConsecutiveQuadBlack(x[0],x[1])

def setAntiConsecutiveQuad(self,row,col=-1):
	# To label a single cell as specifically not having any consecutive pairs
	if col == -1:
		(row,col) = self._procCell(row)
	if 'ConsecutiveQuad' not in self._constraintInitialized:
		self.consecutiveQuadCells = [(row,col,hv)]
		self._constraintInitialized.append('ConsecutiveQuad')
	self.setConsecutiveQuad(row,col,2)
	
def setAntiConsecutiveQuadArray(self,cells):
	for x in cells: self.setAntiConsecutiveQuad(x)

def setConsecutiveQuadNegative(self):
	if 'ConsecutiveQuad' not in self._constraintInitialized:
		self.consecutiveQuadCells = [(row,col,hv)]
		self._constraintInitialized.append('ConsecutiveQuad')
	self._constraintNegative.append('ConsecutiveQuad')
	
def _applyConsecutiveQuadNegative(self):
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1):
			if (i,j) not in self.consecutiveQuadCells:
				self.setAntiConsecutiveQuad(i,j)	
	
def setDiagonalConsecutivePairs(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
		
	self.model.Add(self.cellValues[row][col] != self.cellValues[row+1][col+1])
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+1][col+1] <= 1)
	self.model.Add(self.cellValues[row+1][col+1] - self.cellValues[row][col] <= 1)
	self.model.Add(self.cellValues[row][col+1] != self.cellValues[row+1][col])
	self.model.Add(self.cellValues[row][col+1] - self.cellValues[row+1][col] <= 1)
	self.model.Add(self.cellValues[row+1][col] - self.cellValues[row][col+1] <= 1)
	
def setDiagonalConsecutivePairsArray(self,cells):
	for x in cells: self.DiagonalConsecutivePairs(x)