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
	
def setAntiDiagonalMain(self):
	self.setPointingDifferents(1,1,2,2,self.boardSizeRoot)
	
def setAntiDiagonalOff(self):
	self.setPointingDifferents(1,self.boardWidth,2,self.boardWidth-1,self.boardSizeRoot)

def setMagnitudeMirrorMain(self):
	for i in range(1,self.boardWidth):
		for j in range(i):
			b = self.model.NewBoolVar("magvar")
			self.model.Add(self.cellValues[i][j] <= 5).OnlyEnforceIf(b)
			self.model.Add(self.cellValues[j][i] <= 5).OnlyEnforceIf(b)
			self.model.Add(self.cellValues[i][j] >= 5).OnlyEnforceIf(b.Not())
			self.model.Add(self.cellValues[j][i] >= 5).OnlyEnforceIf(b.Not())

def setMagnitudeMirrorOff(self):
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1-i):
			b = self.model.NewBoolVar("magvar")
			fi = self.boardWidth-1-j
			fj = self.boardWidth-1-i
			self.model.Add(self.cellValues[i][j] <= 5).OnlyEnforceIf(b)
			self.model.Add(self.cellValues[fi][fj] <= 5).OnlyEnforceIf(b)
			self.model.Add(self.cellValues[i][j] >= 5).OnlyEnforceIf(b.Not())
			self.model.Add(self.cellValues[fi][fj] >= 5).OnlyEnforceIf(b.Not())
			
def setMagnitudeAntiMirrorMain(self):
	for i in range(1,self.boardWidth):
		for j in range(i):
			b = self.model.NewBoolVar("magvar")
			self.model.Add(self.cellValues[i][j] <= 5).OnlyEnforceIf(b)
			self.model.Add(self.cellValues[j][i] >= 5).OnlyEnforceIf(b)
			self.model.Add(self.cellValues[i][j] >= 5).OnlyEnforceIf(b.Not())
			self.model.Add(self.cellValues[j][i] <= 5).OnlyEnforceIf(b.Not())

def setMagnitudeAntiMirrorOff(self):
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1-i):
			b = self.model.NewBoolVar("magvar")
			fi = self.boardWidth-1-j
			fj = self.boardWidth-1-i
			self.model.Add(self.cellValues[i][j] <= 5).OnlyEnforceIf(b)
			self.model.Add(self.cellValues[fi][fj] >= 5).OnlyEnforceIf(b)
			self.model.Add(self.cellValues[i][j] >= 5).OnlyEnforceIf(b.Not())
			self.model.Add(self.cellValues[fi][fj] <= 5).OnlyEnforceIf(b.Not())

def setParityMirrorMain(self):
	if self.isParity is False:
		self._setParity()
	for i in range(1,self.boardWidth):
		for j in range(i):
			self.model.Add(self.cellParity[i][j] == self.cellParity[j][i])

def setParityMirrorOff(self):
	if self.isParity is False:
		self._setParity()
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1-i):
			fi = self.boardWidth-1-j
			fj = self.boardWidth-1-i
			self.model.Add(self.cellParity[i][j] == self.cellParity[fi][fj])

def setEntropyMirrorMain(self):
	if self.isEntropy is False:
		self._setEntropy()
	for i in range(1,self.boardWidth):
		for j in range(i):
			self.model.Add(self.cellEntropy[i][j] == self.cellEntropy[j][i])

def setEntropyMirrorOff(self):
	if self.isEntropy is False:
		self._setEntropy()
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1-i):
			fi = self.boardWidth-1-j
			fj = self.boardWidth-1-i
			self.model.Add(self.cellEntropy[i][j] == self.cellEntropy[fi][fj])
			
def setEntropyAntiMirrorMain(self):
	if self.isEntropy is False:
		self._setEntropy()
	for i in range(1,self.boardWidth):
		for j in range(i):
			self.model.Add(self.cellEntropy[i][j] != self.cellEntropy[j][i])

def setEntropyAntiMirrorOff(self):
	if self.isEntropy is False:
		self._setEntropy()
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1-i):
			fi = self.boardWidth-1-j
			fj = self.boardWidth-1-i
			self.model.Add(self.cellEntropy[i][j] != self.cellEntropy[fi][fj])
		
def setPrimalityMirrorMain(self):
	if self.isPrimality is False:
		self._setPrimality()
	for i in range(1,self.boardWidth):
		for j in range(i):
			b = self.model.NewBoolVar("primvar")
			self.model.Add(self.cellPrimality[i][j] <= 1).OnlyEnforceIf(b)
			self.model.Add(self.cellPrimality[j][i] <= 1).OnlyEnforceIf(b)
			self.model.Add(self.cellPrimality[i][j] >= 1).OnlyEnforceIf(b.Not())
			self.model.Add(self.cellPrimality[j][i] >= 1).OnlyEnforceIf(b.Not())		

def setPrimalityMirrorOff(self):
	if self.isPrimality is False:
		self._setPrimality()
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1-i):
			b = self.model.NewBoolVar("primvar")
			fi = self.boardWidth-1-j
			fj = self.boardWidth-1-i
			self.model.Add(self.cellPrimality[i][j] <= 1).OnlyEnforceIf(b)
			self.model.Add(self.cellPrimality[fi][fj] <= 1).OnlyEnforceIf(b)
			self.model.Add(self.cellPrimality[i][j] >= 1).OnlyEnforceIf(b.Not())
			self.model.Add(self.cellPrimality[fi][fj] >= 1).OnlyEnforceIf(b.Not())
			
def setPrimalityAntiMirrorMain(self):
	if self.isPrimality is False:
		self._setPrimality()
	for i in range(1,self.boardWidth):
		for j in range(i):
			b = self.model.NewBoolVar("primvar")
			self.model.Add(self.cellPrimality[i][j] <= 1).OnlyEnforceIf(b)
			self.model.Add(self.cellPrimality[j][i] >= 1).OnlyEnforceIf(b)
			self.model.Add(self.cellPrimality[i][j] >= 1).OnlyEnforceIf(b.Not())
			self.model.Add(self.cellPrimality[j][i] <= 1).OnlyEnforceIf(b.Not())

def setPrimalityAntiMirrorOff(self):
	if self.isPrimality is False:
		self._setPrimality()
	for i in range(self.boardWidth-1):
		for j in range(self.boardWidth-1-i):
			b = self.model.NewBoolVar("primvar")
			fi = self.boardWidth-1-j
			fj = self.boardWidth-1-i
			self.model.Add(self.cellPrimality[i][j] <= 1).OnlyEnforceIf(b)
			self.model.Add(self.cellPrimality[fi][fj] >= 1).OnlyEnforceIf(b)
			self.model.Add(self.cellPrimality[i][j] >= 1).OnlyEnforceIf(b.Not())
			self.model.Add(self.cellPrimality[fi][fj] <= 1).OnlyEnforceIf(b.Not())
			
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
				
def setKnightMare(self):
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			ij = self.cellValues[i][j]
			kCells = [self.cellValues[i+k][j+m] for k in [1,2] for m in [-2,-1,1,2] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth]
			for k in kCells:
				self.model.Add(ij + k != 5)
				self.model.Add(ij + k != 15)

def setGeneralizedKnightMare(self,forbiddenDigits=[5,15]):
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			ij = self.cellValues[i][j]
			kCells = [self.cellValues[i+k][j+m] for k in [1,2] for m in [-2,-1,1,2] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth]
			for k in kCells:
				for d in forbiddenDigits:
					self.model.Add(ij + k != d)

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
	
def _setIndexCell(self,row,col,rc):
	# This is the atomic call to set an index condition. Dealing with whether it's a whole row, whether or not there's a negative
	# constraint is dealt with higher level functions. This is not generally meant to be set outside the class.
	# row,col is exactly what you think
	# rc determines whether the cell is indexing its row or its column: 0 -> row, 1 -> column
	
	hStep = 0 if rc == self.Col else 1
	vStep = 0 if rc == self.Row else 1		
	target = row+1 if rc == self.Col else col+1
	varBitmap = self._varBitmap('IndexRow{:d}Col{:d}'.format(row,col),self.boardWidth)
	self.allVars = self.allVars + varBitmap[0]
	
	for k in range(self.boardWidth):
		self.model.Add(self.cellValues[row][col] == k+1).OnlyEnforceIf(varBitmap[k])
		self.model.Add(self.cellValues[row*hStep+k*vStep][col*vStep+k*hStep] == target).OnlyEnforceIf(varBitmap[k])

def _setNonIndexCell(self,row,col,rc):
	# This is the atomic call to set a negative constraint on an index condition. Dealing with whether it's a whole row, whether
	# or not there's a negative constraint is dealt with higher level functions. This is not generally meant to be set outside the class.
	# row,col is exactly what you think
	# rc determines whether the cell is indexing its row or its column: 0 -> row, 1 -> column
			
	hStep = 0 if rc == self.Col else 1
	vStep = 0 if rc == self.Row else 1		
	target = row+1 if rc == self.Col else col+1
	varBitmap = self._varBitmap('IndexRow{:d}Col{:d}'.format(row,col),self.boardWidth-1)
	self.allVars = self.allVars + varBitmap[0]
	
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
		if neg is True:
			inlist0 = []
		else:
			inlist0 = [x for x in range(self.boardWidth)]
	else:
		inlist0 = [x-1 for x in inlist1]
	
	for i in range(self.boardWidth):
		if i in inlist0:
			self._setIndexCell(row0,i,self.Col)
		elif neg is True:
			self._setNonIndexCell(row0,i,self.Col)
			
def setIndexColumn(self,col1,neg=False,inlist1=[]):
	# This sets up an indexing column. Each cell indexes the *row* so don't be surprised when we call 
	# the cell method with rc=0.
	# Row is the column number
	# neg is whether or not there is a negative constraint on cells not in the index list
	# inlist is the list of cells that index vs. not index in the negative constraint scenario
	
	# Convert 1-base to 0-base
	col0 = col1 - 1
	if len(inlist1) == 0:
		if neg is True:
			inlist0 = []
		else:
			inlist0 = [x for x in range(self.boardWidth)]
	else:
		inlist0 = [x-1 for x in inlist1]
	
	for i in range(self.boardWidth):
		if i in inlist0:
			self._setIndexCell(i,col0,self.Row)
		elif neg is True:	
			self._setNonIndexCell(i,col0,self.Row)

def setGlobalWhispers(self,diff=4,gle=2):
	# Every cell must have at least one neighbor which with its difference is at least diff
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			wwwvars = []
			kCells = [self.cellValues[i+k][j+m] for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth]
			for k in kCells:
				cOn = self.model.NewBoolVar('GlobalWhisperUpNeighborGoodRow{:d}Col{:d}'.format(i,j))
				cOrd = self.model.NewBoolVar('GlobalWhisperUpNeighborOrderRow{:d}Col{:d}'.format(i,j))
				if gle == 2:
					self.model.Add(self.cellValues[i][j] - k >= diff).OnlyEnforceIf([cOn,cOrd])
					self.model.Add(k - self.cellValues[i][j] >= diff).OnlyEnforceIf([cOn,cOrd.Not()])
					self.model.Add(self.cellValues[i][j] - k < diff).OnlyEnforceIf([cOn.Not()])
					self.model.Add(k - self.cellValues[i][j] < diff).OnlyEnforceIf([cOn.Not()])
					self.model.AddBoolAnd([cOrd]).OnlyEnforceIf([cOn.Not()])
					wwwvars.append(cOn)
				elif gle == 1:
					self.model.Add(self.cellValues[i][j] - k == diff).OnlyEnforceIf([cOn,cOrd])
					self.model.Add(k - self.cellValues[i][j] == diff).OnlyEnforceIf([cOn,cOrd.Not()])
					self.model.Add(self.cellValues[i][j] - k != diff).OnlyEnforceIf([cOn.Not()])
					self.model.Add(k - self.cellValues[i][j] != diff).OnlyEnforceIf([cOn.Not()])
					self.model.AddBoolAnd([cOrd]).OnlyEnforceIf([cOn.Not()])
					wwwvars.append(cOn)
				elif gle == 0:
					self.model.Add(self.cellValues[i][j] - k <= diff).OnlyEnforceIf([cOn])
					self.model.Add(k - self.cellValues[i][j] <= diff).OnlyEnforceIf([cOn])
					self.model.Add(self.cellValues[i][j] - k > diff).OnlyEnforceIf([cOn.Not(),cOrd])
					self.model.Add(k - self.cellValues[i][j] > diff).OnlyEnforceIf([cOn.Not(),cOrd.Not()])
					self.model.AddBoolAnd([cOrd]).OnlyEnforceIf([cOn])
					wwwvars.append(cOn)
			self.model.AddBoolOr(wwwvars)
			
def setCloseNeighbors(self):
	self.setGlobalWhispers(diff=1,gle=1)

def setCloseNeighbours(self):
	self.setCloseNeighbors()
			
def setGlobalNeighborSum(self,sums=[],exceptions=[]):
	# Every cell must have an orthogonal neighbor with which it sums to a value in sums, unless the digit is in exceptions
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			
			# This section creates variables determining if the digit in this cell is one of the exceptions. We have a variable for each exception, and then a catch all "not them"
			# This is a bit different of an idiom than we usually use. For each of the affirmative 
			# cases, we define exactly the value of the cell, so all is good
			# For the "other" case, we define the condition negatively by saying none of the exceptions are met in that case
			exVars = self._varBitmap('GNSRow{:d}Col{:d}'.format(i,j),len(exceptions)+1)
			for k in range(len(exceptions)):
				self.model.Add(self.cellValues[i][j] == exceptions[k]).OnlyEnforceIf(exVars[k])
				self.model.Add(self.cellValues[i][j] != exceptions[k]).OnlyEnforceIf(exVars[len(exceptions)])
			gnsvars = []
			kCells = [self.cellValues[i+k][j+m] for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth]
			for k in kCells:
				cOn = self.model.NewBoolVar('GlobalWhisperUpNeighborGoodRow{:d}Col{:d}'.format(i,j))
				# Note: we have to bury cOn if we're in one of the exceptions. This will consequently bury the varBitmap
				for m in range(len(exceptions)):
					self.model.AddBoolAnd(cOn.Not()).OnlyEnforceIf(exVars[m])
				
				varBitmap = self._varBitmap('GNSRow{:d}Col{:d}'.format(i,j),len(sums))
				self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf(cOn.Not())
				for m in range(len(sums)):
					self.model.Add(self.cellValues[i][j] + k == sums[m]).OnlyEnforceIf([cOn]+varBitmap[m]+exVars[len(exceptions)])
					self.model.Add(self.cellValues[i][j] + k != sums[m]).OnlyEnforceIf([cOn.Not()]+exVars[len(exceptions)])
				gnsvars.append(cOn)
			self.model.AddBoolOr(gnsvars).OnlyEnforceIf(exVars[len(exceptions)])
			
def setGlobalNeighbourSum(self,sums=[],exceptions=[]):
	self.setGlobalNeighborSum(sums,exceptions)

def setGlobalEntropy(self):
	self.setEntropyQuadArray([(i,j) for i in range(1,self.boardWidth) for j in range(1,self.boardWidth)])
	
def setGlobalModular(self):
	self.setModularQuadArray([(i,j) for i in range(1,self.boardWidth) for j in range(1,self.boardWidth)])
	
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
			
def setRepellingDigit(self,value,inlist):
	#A repelling digit has a list of other digits it cannot be adjacent to
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			c = self.model.NewBoolVar('RepellingDigitD{:d}R{:d}C{:d}'.format(value,i,j))
			self.model.Add(self.cellValues[i][j] == value).OnlyEnforceIf(c)
			kCells = [self.cellValues[i+k][j+m] for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m) and i+k >= 0 and i+k < self.boardWidth and j+m >= 0 and j+m < self.boardWidth]
			for k in range(len(kCells)):
				for m in inlist:
					self.model.Add(kCells[k] != m).OnlyEnforceIf(c)
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
				varBitmap = self._sudoku_varBitmap('GSPRow{:d}Col{:d}'.format(i,j),len(pairs))
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

def setRotationalPairs(self):
	for i in range((self.boardWidth + 1)//2):
		for j in range(self.boardWidth):
			if (i == self.boardWidth//2) and (j >= i): continue	# Does top half of board, and if there is a center row, do left half of it
			for k in range(i,(self.boardWidth + 1)//2):
				for m in range(self.boardWidth):
					if (k == i) and (m <= j): continue
					if (k == self.boardWidth//2) and (m >= k): continue
					c = self.model.NewBoolVar('')
					self.model.Add(self.cellValues[i][j] == self.cellValues[k][m]).OnlyEnforceIf(c)
					self.model.Add(self.cellValues[self.boardWidth-1-i][self.boardWidth-1-j] == self.cellValues[self.boardWidth-1-k][self.boardWidth-1-m]).OnlyEnforceIf(c)
					self.model.Add(self.cellValues[i][j] != self.cellValues[k][m]).OnlyEnforceIf(c.Not())
					self.model.Add(self.cellValues[self.boardWidth-1-i][self.boardWidth-1-j] != self.cellValues[self.boardWidth-1-k][self.boardWidth-1-m]).OnlyEnforceIf(c.Not())
					
def setNoThreeInARowParity(self):
	if self.isParity is False:
		self._setParity()
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
			varBitmap = self._sudoku_varBitmap('RotorOffset'.format(i,j),8)
			self.model.AddBoolAnd(varBitmap[0]).OnlyEnforceIf(c.Not())		# Pegs variables if there is no match
			for n in range(8):
				for p in range(8):
					self.model.Add(self.cellValues[3*i+1+w[p][0]][3*j+1+w[p][1]] == self.cellValues[3*k+1+w[(p+n)%8][0]][3*m+1+w[(p+n)%8][1]]).OnlyEnforceIf(varBitmap[n]+[c])

def setNoConsecutiveSum(self,sums=[]):
	for i in range(self.boardWidth):
		for j in range(self.boardWidth-1):
			for x in sums:
				self.model.Add(self.cellValues[i][j]+self.cellValues[i][j+1] != x)
				self.model.Add(self.cellValues[j][i]+self.cellValues[j+1][i] != x)
				
def setNoSeven(self):
	self.setNoConsecutiveSum([7])

def setCountingCircles(self,inlist):
	inlist = self._procCellList(inlist)
	for d in self.digits:
		circleDigit = []
		for x in inlist:
			dx = self.model.NewBoolVar('countingCircle')
			dxInt = self.model.NewIntVar(0,1,'countingCircle')
			circleDigit.append(dxInt)
			self.model.Add(dxInt == 1).OnlyEnforceIf(dx)
			self.model.Add(dxInt == 0).OnlyEnforceIf(dx.Not())
			
			self.model.Add(self.cellValues[x[0]][x[1]] == d).OnlyEnforceIf(dx)
			self.model.Add(self.cellValues[x[0]][x[1]] != d).OnlyEnforceIf(dx.Not())
		
		dAppears = self.model.NewBoolVar('countingCircleValueAppears')
		self.model.Add(sum(circleDigit) == d).OnlyEnforceIf(dAppears)
		self.model.Add(sum(circleDigit) == 0).OnlyEnforceIf(dAppears.Not())
		
def setOffsetDigit(self,digit):
	# The digit that appears below the offset digit is its number of cells away from the offset digit in its row
	digitPlace = []
	for i in range(self.boardWidth):
		tempArray = []
		for j in range(self.boardWidth):
			tempCell = self.model.NewBoolVar('digitPlace{:d}{:d}{:d}'.format(digit,i,j))
			self.model.Add(self.cellValues[i][j] == digit).OnlyEnforceIf(tempCell)
			self.model.Add(self.cellValues[i][j] != digit).OnlyEnforceIf(tempCell.Not())
			tempArray.append(tempCell)
		digitPlace.insert(i,tempArray) 
	
	for j in range(1,self.boardWidth):
		for k in range(self.boardWidth):
			for m in range(self.boardWidth):
				self.model.Add(self.cellValues[j][k] == abs(m-k)).OnlyEnforceIf([digitPlace[j-1][k],digitPlace[j][m]])