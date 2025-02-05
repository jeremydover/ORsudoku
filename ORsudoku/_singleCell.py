def setGiven(self,row,col=-1,value=-1):
	if col == -1:
		(row,col,value) = self._procCell(row)
	self.model.Add(self.cellValues[row][col] == value)

def setGivenArray(self,cells):
	for x in cells:	self.setGiven(x)

def setMinMaxCell(self,row,col=-1,minmax=-1):
	if col == -1:
		(row,col,minmax) = self._procCell(row)
	if row > 0:
		self.model.Add(self.cellValues[row][col] < self.cellValues[row-1][col]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row-1][col])
	if row < self.boardWidth-1:
		self.model.Add(self.cellValues[row][col] < self.cellValues[row+1][col]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row+1][col])
	if col > 0:
		self.model.Add(self.cellValues[row][col] < self.cellValues[row][col-1]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row][col-1])
	if col < self.boardWidth-1:
		self.model.Add(self.cellValues[row][col] < self.cellValues[row][col+1]) if minmax == 0 else self.model.Add(self.cellValues[row][col] > self.cellValues[row][col+1])
setMaxMinCell = setMinMaxCell
		
def setMinCell(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	self.setMinMaxCell(row,col,self.Min)

def setMaxCell(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	self.setMinMaxCell(row,col,self.Max)
	
def setMinMaxArray(self,cells):
	for x in cells: self.setMinMaxCell(x)

def setMaxMinArray(self,cells):
	for x in cells: self.setMinMaxCell(x)
	
def setMinArray(self,cells):
	for x in cells: self.setMinCell(x)
	
def setMaxArray(self,cells):
	for x in cells: self.setMaxCell(x)
	
def setEvenOdd(self,row,col=-1,parity=-1):
	if col == -1:
		(row,col,parity) = self._procCell(row)
	self.model.AddModuloEquality(parity,self.cellValues[row][col],2)

def setOddEven(self,row,col=-1,parity=-1):
	self.setEvenOdd(row,col,parity)
	
def setEven(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	self.setEvenOdd(row,col,self.Even)
	
def setOdd(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	self.setEvenOdd(row,col,self.Odd)
	
def setEvenArray(self,cells):
	for x in cells: self.setEven(x)
	
def setOddArray(self,cells):
	for x in cells: self.setOdd(x)
	
def setEvenOddArray(self,cells):
	for x in cells: self.setEvenOdd(x)

def setOddEvenArray(self,cells):
	for x in cells: self.setOddEven(x)
	
def setNeighborSum(self,row,col=-1):
	# Cell whose value is the sum of its orthogonally adjacent neighbors
	if col == -1:
		(row,col) = self._procCell(row)
	sCells = [self.cellValues[row+k][col+m] for k in [-1,0,1] for m in [-1,0,1] if abs(k) != abs(m) and row+k >= 0 and row+k < self.boardWidth and col+m >= 0 and col+m < self.boardWidth]
	self.model.Add(sum(sCells) == self.cellValues[row][col])

def	setNeighbourSum(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	self.setNeighborSum(row,col)
	
def setNeighborSumArray(self,cells):
	for x in cells: self.setNeighborSum(x)
	
def	setNeighbourSumArray(self,cells):
	self.setNeighborSum(cells)

def setFriendly(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	
	if 'Friendly' not in self._constraintInitialized:	
		self.friendlyCells = [(row,col)]
		self._constraintInitialized.append('Friendly')
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
	
def setUnfriendly(self,row,col=-1):
	# To label a single cell as specifically not friendly
	if col == -1:
		(row,col) = self._procCell(row)
	self.model.Add(self.cellValues[row][col] != row+1)
	self.model.Add(self.cellValues[row][col] != col+1)
	rowInd = row // self.boardSizeRoot
	colInd = col // self.boardSizeRoot
	box = 3*rowInd + colInd
	self.model.Add(self.cellValues[row][col] != box+1)			
	
def setUnfriendlyArray(self,cells):
	for x in cells: self.setUnfriendly(x)

def setFriendlyNegative(self):
	if 'Friendly' not in self._constraintInitialized:	
		self.friendlyCells = []
		self._constraintInitialized.append('Friendly')
	self._constraintNegative.append('Friendly')
	
def _applyFriendlyNegative(self):
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			if (i,j) not in self.friendlyCells:
				self.setUnfriendly(i,j)
				
def setScary(self,row,col=-1,diff=3):
	if col == -1:
		(row,col) = self._procCell(row)
	nCells = {(row+i,col+j) for i in [-1,0,1] for j in [-1,0,1] if (i,j) != (0,0)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)}
	for x in nCells:
		c = self.model.NewBoolVar('ScaryCell')
		self.model.Add(self.cellValues[row][col] - self.cellValues[x[0]][x[1]] >= diff).OnlyEnforceIf(c)
		self.model.Add(self.cellValues[x[0]][x[1]] - self.cellValues[row][col] >= diff).OnlyEnforceIf(c.Not())

def setPencilmarks(self,row1,col1=-1,values=-1):
	# A list of allowed values in the cell
	if col1 == -1:
		T = self._procCell(row1)
		row = T[0]
		col = T[1]
		values = [T[i] for i in range(2,len(T))]
	else:
		row = row1 - 1
		col = col1 - 1
		
	self.model.AddAllowedAssignments([self.cellValues[row][col]],[(x,) for x in values])
	
def setPencilmarksArray(self,list):
	for x in list: self.setPencilmarks(x)

def setSearchNine(self,row1,col1,uldr,digit=9):
	# A search nine clue indicates the distance and direction of a 9 from the clued cell. The distance is the cell value, the arrow clue points
	row = row1 - 1
	col = col1 - 1
	if uldr == self.Up:
		maxD = row
		minD = self.boardWidth-1-row
		hStep = 0
		vStep = -1
	elif uldr == self.Down:
		maxD = self.boardWidth-1-row
		minD = row
		hStep = 0
		vStep = 1
	elif uldr == self.Left:
		maxD = col
		minD = self.boardWidth-1-col
		hStep = -1
		vStep = 0
	else:
		maxD = self.boardWidth-1-col
		minD = col
		hStep = 1
		vStep = 0

	allowableDigits = [x for x in self.digits if 0 <= x <= maxD or 0 <= -1*x <= minD]
	varBitmap = self._varBitmap('SearchNineRow{:d}Col{:d}'.format(row,col),len(allowableDigits))
	varTrack = 0
	if type(digit) is list:
		digitBitmap = self._varBitmap('SearchNineDigitsRow{:d}Col{:d}'.format(row,col),len(digit))
	for x in allowableDigits:
		self.model.Add(self.cellValues[row][col] == x).OnlyEnforceIf(varBitmap[varTrack])
		if type(digit) is list:
			for i in range(len(digit)):
				self.model.Add(self.cellValues[row+x*vStep][col+x*hStep] == digit[i]).OnlyEnforceIf(varBitmap[varTrack]+digitBitmap[i])
		else:
			self.model.Add(self.cellValues[row+x*vStep][col+x*hStep] == digit).OnlyEnforceIf(varBitmap[varTrack])
		varTrack = varTrack + 1

def setLogicBomb(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	if (row < 2) or (row >= self.boardWidth-2) or (col < 2) or (col >= self.boardWidth-2):
		print("Logic bomb clues must be at least 2 cells away from every border")
		sys.exit()
	kCells = [self.cellValues[row+k][col+m] for k in [-2,-1,1,2] for m in [-2,-1,1,2] if abs(k) != abs(m)] + [self.cellValues[row][col]]
	self.model.AddAllDifferent(kCells)
	
def assertNumberOfLogicBombs(self,num):
	self.logicCounts = []
	for i in range(2,self.boardWidth-2):
		for j in range(2,self.boardWidth-2):
			b = self.model.NewBoolVar('LB')
			c = self.model.NewIntVar(0,1,'LB')
			self.model.Add(c == 0).OnlyEnforceIf(b.Not())
			self.model.Add(c == 1).OnlyEnforceIf(b)
			kCells = [self.cellValues[i+k][j+m] for k in [-2,-1,1,2] for m in [-2,-1,1,2] if abs(k) != abs(m)] + [self.cellValues[i][j]]
			for k in range(9):
				for m in range(k+1,9):
					self.model.Add(kCells[k] != kCells[m]).OnlyEnforceIf(b)
			self.logicCounts.append(c)
	self.model.Add(sum(self.logicCounts) == num)

def setCupid(self,row1,col1,row2,col2):
	row = row1 - 1
	col = col1 - 1
	hStep = col2 - col1
	vStep = row2 - row1
	cells = list({(row+i*vStep,col+i*hStep) for i in range(1,self.boardWidth)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)})
	vars = [self.model.NewBoolVar('') for i in range(len(cells))]
	for i in range(len(cells)):
		self.model.Add(self.cellValues[cells[i][0]][cells[i][1]] == self.cellValues[row][col]).OnlyEnforceIf(vars[i])
		self.model.Add(self.cellValues[cells[i][0]][cells[i][1]] != self.cellValues[row][col]).OnlyEnforceIf(vars[i].Not())
	self.model.AddBoolOr(vars)
	
def setNearestNeighbor(self,row1,col1,pointers):
	row = row1 - 1
	col = col1 - 1
	if type(pointers) is int:
		pointers = [pointers]
	allNeighbors = {(row+i,col+j) for i in [-1,0,1] for j in [-1,0,1] if abs(i) != abs(j)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)}
	vDict = {}
	# Need for cell transform clues. self.minDigit is the smallest base digit, not necessarily as transformed.
	myMin = min(self.digits)
	myMax = max(self.digits)
	
	for x in allNeighbors:
		bV = self.model.NewBoolVar('')
		vDict[x] = self.model.NewIntVar(0,myMax-myMin,'')
		self.model.Add(self.cellValues[row][col] > self.cellValues[x[0]][x[1]]).OnlyEnforceIf(bV)
		self.model.Add(vDict[x] == self.cellValues[row][col] - self.cellValues[x[0]][x[1]]).OnlyEnforceIf(bV)
		self.model.Add(self.cellValues[row][col] < self.cellValues[x[0]][x[1]]).OnlyEnforceIf(bV.Not())
		self.model.Add(vDict[x] == self.cellValues[x[0]][x[1]] - self.cellValues[row][col]).OnlyEnforceIf(bV.Not())
	pointedNeighbors = {(row + (1-x//2)*(-1)**(x%2 + 1),col + (x//2)*(-1)**(x%2 + 1)) for x in pointers}
	for x in pointedNeighbors:
		for y in allNeighbors:
			if y in pointedNeighbors:
				self.model.Add(vDict[x] == vDict[y])
			else:
				self.model.Add(vDict[x] < vDict[y])
				
def setNearestNeighbour(self,row1,col1,pointers):
	self.setNearestNeighbor(row1,col1,pointers)

def setDifferentNeighbors(self,row1,col1,includeCell=False):
	# A different neighbor constraint asserts that the digit in the cell is the number of distinct digits in the cell's (8-cell) neighborhood...h/t clover!
	row = row1 - 1
	col = col1 - 1
	neighborSet = {(row+i,col+j) for i in [-1,0,1] for j in [-1,0,1] if (i,j) != (0,0)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)}
	if includeCell:
		neighborSet.add((row,col))
	neighbors = list(neighborSet)
	
	digits = list(self.digits)
	digitCellBools = [[self.model.NewBoolVar('Digit NeighborPairs') for i in range(len(digits))] for j in range(len(neighbors))]
	digitCellInts = [[self.model.NewIntVar(0,1,'DigitCellPairs') for i in range(len(digits))] for j in range(len(neighbors))]
	digitBools = [self.model.NewBoolVar('DigitCounts') for i in range(len(digits))]
	digitInts = [self.model.NewIntVar(0,1,'DigitCounts') for i in range(len(digits))]
	for j in range(len(neighbors)):
		for i in range(len(digits)):
			self.model.Add(self.cellValues[neighbors[j][0]][neighbors[j][1]] == digits[i]).OnlyEnforceIf(digitCellBools[j][i])
			self.model.Add(self.cellValues[neighbors[j][0]][neighbors[j][1]] != digits[i]).OnlyEnforceIf(digitCellBools[j][i].Not())
			self.model.Add(digitCellInts[j][i] == 1).OnlyEnforceIf(digitCellBools[j][i])
			self.model.Add(digitCellInts[j][i] == 0).OnlyEnforceIf(digitCellBools[j][i].Not())
			
	for i in range(len(digits)):
		self.model.Add(sum([digitCellInts[j][i] for j in range(len(neighbors))]) > 0).OnlyEnforceIf(digitBools[i])
		self.model.Add(sum([digitCellInts[j][i] for j in range(len(neighbors))]) == 0).OnlyEnforceIf(digitBools[i].Not())
		self.model.Add(digitInts[i] == 1).OnlyEnforceIf(digitBools[i])
		self.model.Add(digitInts[i] == 0).OnlyEnforceIf(digitBools[i].Not())
	
	varBitmap = self._varBitmap('DifferentNeighborsRow{:d}Col{:d}'.format(row,col),len(digits))
	
	for i in range(len(digits)):
		self.model.Add(sum([digitInts[i] for i in range(len(digits))]) == digits[i]).OnlyEnforceIf(varBitmap[i])
		self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])

def setDifferentNeighbours(self,row1,col1,includeCell=False):
	self.setDifferentNeighbors(row1,col1,includeCell)

def setSlingshot(self,row1,col1,tail,head):
	# Asserts that the digit in the tail direction from cell (row,col) appears in in the direction of the head, where the distance is given by the digit in (row,col)
	
	row = row1-1
	col = col1-1
	
	# Find variable that must be matched
	if tail == self.Up:
		matchVar = self.cellValues[row-1][col]
	elif tail == self.Down:
		matchVar = self.cellValues[row+1][col]
	elif tail == self.Left:
		matchVar = self.cellValues[row][col-1]
	else:
		matchVar = self.cellValues[row][col+1]
	
	# Figure parameters for placement direction
	if head == self.Up:
		cand = row
		hStep = 0
		vStep = -1
	elif head == self.Down:
		cand = self.boardWidth - row - 1
		hStep = 0
		vStep = 1
	elif head == self.Left:
		cand = col
		hStep = -1
		vStep = 0
	else:
		cand = self.boardWidth - col - 1
		hStep = 1
		vStep = 0
	
	varBitmap = self._varBitmap('SlingshotRow{:d}Col{:d}'.format(row,col),cand)
	for i in range(1,cand+1):
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == matchVar).OnlyEnforceIf(varBitmap[i-1])
			self.model.Add(self.cellValues[row][col] == i).OnlyEnforceIf(varBitmap[i-1])
			
def _initializeNeighborSet(self):
	if 'NeighborSet' not in self._constraintInitialized:
		self._constraintInitialized.append('NeighborSet')
		self.neighborSetProperty = 'Entropy'
		self.neighborSetPropertyInitialized = False
		self.neighborSetCells = []
			
def _setNeighborSetBase(self,row,col,pm,prop=None):
	# Asserts a cell will (pm = 1) or won't (pm = -1) have an adjacent cell with the same property (prop)
	
	self._initializeNeighborSet()
	if prop is None:
		prop = self.neighborSetProperty

	neighbors = list({(row-1,col),(row+1,col),(row,col-1),(row,col+1)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)})
	neighborBools = [self.model.NewBoolVar('NeighborSetNeighborTests') for j in range(len(neighbors))]
	
	if type(prop) == str:
		if prop not in self._constraintInitialized:
			getattr(self,'_set'+prop)()
		myCells = getattr(self,'cell'+prop)	
		for j in range(len(neighbors)):
			self.model.Add(myCells[row][col] == myCells[neighbors[j][0]][neighbors[j][1]]).OnlyEnforceIf(neighborBools[j])
			self.model.Add(myCells[row][col] != myCells[neighbors[j][0]][neighbors[j][1]]).OnlyEnforceIf(neighborBools[j].Not())
			
	elif type(prop) == list or type(prop) == set:
		thisDigitBools = []
		for x in prop:
			c = self.model.NewBoolVar('BaseCellTestDigit{:d}'.format(x))
			self.model.Add(self.cellValues[row][col] == x).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[row][col] != x).OnlyEnforceIf(c.Not())
			thisDigitBools.append(c)
		thisDigitIn = self.model.NewBoolVar('BaseCellTest')
		self.model.AddBoolOr(thisDigitBools).OnlyEnforceIf(thisDigitIn)
		self.model.AddBoolAnd([x.Not() for x in thisDigitBools]).OnlyEnforceIf(thisDigitIn.Not())

		for j in range(len(neighbors)):
			thisNeighborBools = []
			for x in prop:
				c = self.model.NewBoolVar('NeighborTestDigit{:d}'.format(x))
				self.model.Add(self.cellValues[neighbors[j][0]][neighbors[j][1]] == x).OnlyEnforceIf(c)
				self.model.Add(self.cellValues[neighbors[j][0]][neighbors[j][1]] != x).OnlyEnforceIf(c.Not())
				thisNeighborBools.append(c)
			neighborIn = self.model.NewBoolVar('NeighborTest')
			self.model.AddBoolOr(thisNeighborBools).OnlyEnforceIf(neighborIn)
			self.model.AddBoolAnd([x.Not() for x in thisNeighborBools]).OnlyEnforceIf(neighborIn.Not())
			self.model.Add(sum([thisDigitIn,neighborIn]) == 1).OnlyEnforceIf(neighborBools[j].Not())
			self.model.AddBoolOr([thisDigitIn,neighborIn.Not()]).OnlyEnforceIf(neighborBools[j])
			self.model.AddBoolOr([thisDigitIn.Not(),neighborIn]).OnlyEnforceIf(neighborBools[j])
			
	if pm == 1:
		self.model.AddBoolOr(neighborBools)
		self.neighborSetCells.append((row,col))
	if pm == -1:
		self.model.AddBoolAnd([x.Not() for x in neighborBools])
		
def setPosNeighborSet(self,row1,col1=-1,prop=None):
	if col1 == -1:
		(row,col) = self._procCell(row1)
	else:
		row = row1 - 1
		col = col1 - 1
	self._setNeighborBase(row,col,1,prop)
	
def setPosNeighbourSet(self,row,col,prop=None):
	self._setNeighborSet(row,col,prop)
	
def setNegNeighborSet(self,row,col,prop=None):
	if col1 == -1:
		(row,col) = self._procCell(row1)
	else:
		row = row1 - 1
		col = col1 - 1
	self._setNeighborBase(row,col,-1,prop)
	
def setNegNeighbourSet(self,row,col,prop=None):
	self.setAntiNeighborSet(row,col,prop)
	
def setPosNeighborSetArray(self,inlist1,prop=None):
	inlist = self._procCellList(inlist1)
	for x in inlist: self._setNeighborSetBase(x[0],x[1],1,prop)
	
def setPosNeighbourSetArray(self,inlist1,prop=None):
	self.setPosNeighborSetArray(inlist1,prop)
	
def setNegNeighborSetArray(self,inlist1,prop=None):
	inlist = self._procCellList(inlist1)
	for x in inlist: self._setNeighborSetBase(x[0],x[1],-1,prop)
	
def setNegNeighbourSetArray(self,inlist1,prop=None):
	self.setNegNeighborSetArray(inlist1,prop)

def setNeighborSetArray(self,inlist1,prop=None):
	inlist = self._procCellList(inlist1)
	for x in inlist: self._setNeighborSetBase(x[0],x[1],x[2],prop)

def setNeighbourSetArray(self,inlist1,prop=None):
	self.setNeighborArray(inlist1,prop)

def setNeighborSetProperty(self,prop):
	self._initializeNeighborSet()
	self.neighborSetProperty = prop

def setNeighbourSetProperty(self,prop):
	self.setNeighborSetProperty(prop)
	
def setNeighborSetNegative(self):
	self._initializeNeighborSet()
	self._constraintNegative.append('NeighborSet')
	
def setNeighbourSetNegative(self):
	self.setNeighbourSetNegative()
	
def _applyNeighborSetNegative(self):
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			if (i,j) not in self.neighborSetCells:
				self._setNeighborSetBase(i,j,-1)
				
def setRemoteClone(self,row1,col1=-1,dir1=-1,dir2=-1):
	if col1 == -1:
		(row1,col1,dir1,dir2) = self._procCell(row1)
	row = row1 - 1
	col = col1 - 1
	
	# Forces dir1 to be Up/Down, dir2 to be Left/Right
	if dir1 > dir2:
		dir1,dir2 = dir2,dir1
	
	vStep = 2*dir1 - 1 # Transforms 0,1 to -1,1
	hStep = 2*dir2 - 5 # Transforms 2,3 to -1,1
	maxCand = min(max(-row*vStep,(self.boardWidth-1-row)*vStep),max(-col*hStep,(self.boardWidth-1-col)*hStep))
	varBitmap = self._varBitmap('RemoteCloneDigitPicker',maxCand)
	for j in range(1,maxCand+1):
		self.model.Add(self.cellValues[row][col] == j).OnlyEnforceIf(varBitmap[j-1])
		self.model.Add(self.cellValues[row+j*vStep][col] == self.cellValues[row][col+j*hStep]).OnlyEnforceIf(varBitmap[j-1])
		