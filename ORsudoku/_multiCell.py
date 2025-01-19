import math
from ORsudoku.combinationIterator import CombinationIterator

def setFortress(self,inlist):
	inlist = self._procCellList(inlist)
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
		(row,col,hv) = self._procCell(row)
	if self.isKropkiInitialized is not True:
		self.kropkiCells = [(row,col,hv)]
		self.isKropkiInitialized = True
	else:
		self.kropkiCells.append((row,col,hv))
	# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
	bit = self.model.NewBoolVar('KropkiWhiteBiggerDigitRow{:d}Col{:d}HV{:d}'.format(row,col,hv))
	self.allVars.append(bit)
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == self.kropkiDiff).OnlyEnforceIf(bit)
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == -1*self.kropkiDiff).OnlyEnforceIf(bit.Not())

def setKropkiBlack(self,row,col=-1,hv=-1):
	if col == -1:
		(row,col,hv) = self._procCell(row)
	if self.isKropkiInitialized is not True:
		self.kropkiCells = [(row,col,hv)]
		self.isKropkiInitialized = True
	else:
		self.kropkiCells.append((row,col,hv))
	# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
	bit = self.model.NewBoolVar('KropkiBlackBiggerDigitRow{:d}Col{:d}HV{:d}'.format(row,col,hv))
	self.allVars.append(bit)
	self.model.Add(self.cellValues[row][col] == self.kropkiRatio*self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf(bit)
	self.model.Add(self.kropkiRatio*self.cellValues[row][col] == self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf(bit.Not())
	
def setKropkiGray(self,row,col=-1,hv=-1):
	if col == -1:
		(row,col,hv) = self._procCell(row)
	if self.isKropkiInitialized is not True:
		self.kropkiCells = [(row,col,hv)]
		self.isKropkiInitialized = True
	else:
		self.kropkiCells.append((row,col,hv))
	# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
	bit1 = self.model.NewBoolVar('KropkiGrayBiggerDigitRow{:d}Col{:d}HV{:d}'.format(row,col,hv))
	bit2 = self.model.NewBoolVar('KropkiGrayBlackWhiteRow{:d}Col{:d}HV{:d}'.format(row,col,hv))
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == self.kropkiDiff).OnlyEnforceIf([bit1,bit2])
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == -1*self.kropkiDiff).OnlyEnforceIf([bit1.Not(),bit2])
	
	self.model.Add(self.cellValues[row][col] == self.kropkiRatio*self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf([bit1,bit2.Not()])
	self.model.Add(self.kropkiRatio*self.cellValues[row][col] == self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf([bit1.Not(),bit2.Not()])
	self.model.Add(self.cellValues[row][col] != self.cellValues[row+hv][col+(1-hv)]+self.kropkiDiff).OnlyEnforceIf([bit2.Not()])
	self.model.Add(self.cellValues[row][col]+self.kropkiDiff != self.cellValues[row+hv][col+(1-hv)]).OnlyEnforceIf([bit2.Not()])
	# Note: the last two lines are a way to avoid bit flopping in the case where either a black or white dot could be placed...particularly 1/2 pairs in standard Kropki. Basically this is saying that if a dot could be white, it is white. It can only be black if it does not meet the white condition
	
def setKropkiWhiteArray(self,cells):
	for x in cells: self.setKropkiWhite(x)
	
def setKropkiBlackArray(self,cells):
	for x in cells: self.setKropkiBlack(x)
	
def setKropkiGrayArray(self,cells):
	for x in cells: self.setKropkiGray(x)
	
def setKropkiArray(self,cells):
	cellList = self._procCellList(cells)
	for x in cellList:
		if x[3] == self.White:
			self.setKropkiWhite(x[0],x[1],x[2])
		elif x[3] == self.Black:
			self.setKropkiBlack(x[0],x[1],x[2])
		else:
			self.setKropkiGray(x[0],x[1],x[2])

def setKropkiNegative(self):
	if self.isKropkiInitialized is not True:
		self.kropkiCells = []
		self.isKropkiInitialized = True
	self.isKropkiNegative = True
	
def setAntiKropki(self,row,col=-1,hv=-1):
	if col == -1:
		(row,col,hv) = self._procCell(row)
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] != self.kropkiDiff)
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] != -1*self.kropkiDiff)
	self.model.Add(self.cellValues[row][col] != self.kropkiRatio*self.cellValues[row+hv][col+(1-hv)])
	self.model.Add(self.kropkiRatio*self.cellValues[row][col] != self.cellValues[row+hv][col+(1-hv)])
	
def setAntiKropkiArray(self,cells):
	for x in cells: self.setAntiKropki(x)

def _applyKropkiNegative(self):
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			if i < 8 and (i,j,1) not in self.kropkiCells:
				self.setAntiKropki(i,j,1)
			if j < 8 and (i,j,0) not in self.kropkiCells:
				self.setAntiKropki(i,j,0)

def setKropkiDifference(self,diff=1):
	# Sets the difference used in all subseqequent white Kropki dots
	self.kropkiDiff = diff
	
def setKropkiRatio(self,ratio=2):
	# Sets the ratio used in all subseqequent black Kropki dots
	self.kropkiRatio = ratio
	
def setGammaEpsilon(self):
	self.setKropkiDifference(5)
	self.setKropkiRatio(3)
				
def setXVV(self,row,col=-1,hv=-1):
	if col == -1:
		(row,col,hv) = self._procCell(row)
	if self.isXVInitialized is not True:
		self.xvCells = [(row,col,hv)]
		self.isXVInitialized = True
	else:
		self.xvCells.append((row,col,hv))
		
	# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
	self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] == 5)
	
def setXVX(self,row,col=-1,hv=-1):
	if col == -1:
		(row,col,hv) = self._procCell(row)
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
	cellList = self._procCellList(cells)
	for x in cellList:
		if x[3] == self.V:
			self.setXVV(x[0],x[1],x[2])
		else:
			self.setXVX(x[0],x[1],x[2])
			
def setAntiXV(self,row,col=-1,hv=-1):
	if col == -1:
		(row,col,hv) = self._procCell(row)
	self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] != 5)
	self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] != 10)
	
def setAntiXVArray(self,cells):
	for x in cells: self.setAntiXV(x)

def setXVNegative(self):
	if self.isXVInitialized is not True:
		self.xvCells = []
		self.isXVInitialized = True
	self.isXVNegative = True
	
def _applyXVNegative(self):
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			if i < 8 and (i,j,1) not in self.xvCells:
				self.setAntiXV(i,j,1)
			if j < 8 and (i,j,0) not in self.xvCells:
				self.setAntiXV(i,j,0)
				
def setXVXVV(self,row,col=-1,hv=-1):
	if col == -1:
		(row,col,hv) = self._procCell(row)
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
		(row,col,hv) = self._procCell(row)
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
	cellList = self._procCellList(cells)
	for x in cellList:
		if x[3] == self.V:
			self.setXVXVV(x[0],x[1],x[2])
		else:
			self.setXVXVX(x[0],x[1],x[2])

def setAntiXVXV(self,row,col=-1,hv=-1):
	if col == -1:
		(row,col,hv) = self._procCell(row)
	self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] != 5)
	self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] != 10)
	self.model.Add(self.cellValues[row][col] + self.cellValues[row+hv][col+(1-hv)] != 15)
	
def setAntiXVXVArray(self,cells):
	for x in cells: self.setAntiXVXV(x)

def setXVXVNegative(self):
	if self.isXVXVInitialized is not True:
		self.xvxvCells = []
		self.isXVXVInitialized = True
	self.isXVXVNegative = True
	
def _applyXVXVNegative(self):
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			if i < 8 and (i,j,1) not in self.xvxvCells:
				self.setAntiXVXV(i,j,1)
			if j < 8 and (i,j,0) not in self.xvxvCells:
				self.setAntiXVXV(i,j,0)

def setXYDifference(self,row,col=-1,hv=-1):
	if col == -1:
		(row,col,hv) = self._procCell(row)
	# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
	if self.isXYDifferenceInitialized is not True:
		self.xyDifferenceCells = [(row,col,hv)]
		self.isXYDifferenceInitialized = True
	else:
		self.xyDifferenceCells.append((row,col,hv))
		
	bit = self.model.NewBoolVar('XYDifferenceBiggerDigitRow{:d}Col{:d}HV{:d}'.format(row,col,hv))
	self.allVars.append(bit)
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == self.cellValues[(1-hv)*row][hv*col]).OnlyEnforceIf(bit)
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] == -1*self.cellValues[(1-hv)*row][hv*col]).OnlyEnforceIf(bit.Not())

def setXYDifferenceArray(self,cells):
	for x in cells: self.setXYDifference(x)

def setAntiXYDifference(self,row,col=-1,hv=-1):
	if col == -1:
		(row,col,hv) = self._procCell(row)
	# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] != self.cellValues[(1-hv)*row][hv*col])
	self.model.Add(self.cellValues[row][col] - self.cellValues[row+hv][col+(1-hv)] != -1*self.cellValues[(1-hv)*row][hv*col])
	
def setAntiXYDifferenceArray(self,cells):
	for x in cells: self.setAntiXYDifference(x)

def setXYDifferenceNegative(self):
	if self.isXYDifferenceInitialized is not True:
		self.xyDifferenceCells = []
		self.isXYDifferenceInitialized = True
	self.isXYDifferenceNegative = True
	
def _applyXYDifferenceNegative(self):
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			if i < 8 and (i,j,1) not in self.xyDifferenceCells:
				self.setAntiXYDifference(i,j,1)
			if j < 8 and (i,j,0) not in self.xyDifferenceCells:
				self.setAntiXYDifference(i,j,0)

def setEitherOr(self,row,col=-1,hv=-1,value=-1):
	if col == -1:
		(row,col,hv,value) = self._procCell(row)
	c = self.model.NewBoolVar('EitherOr')
	self.model.Add(self.cellValues[row][col] == value).OnlyEnforceIf(c)
	self.model.Add(self.cellValues[row+hv][col+(1-hv)] == value).OnlyEnforceIf(c.Not())
	
def setEitherOrArray(self,cells):
	for x in cells: self.setEitherOr(x)

def setCloneRegion(self,inlist):
	inlist = list(map(self._procCellList,inlist))
	for j in range(1,len(inlist)):
		for k in range(len(inlist[0])):
			self.model.Add(self.cellValues[inlist[0][k][0]][inlist[0][k][1]] == self.cellValues[inlist[j][k][0]][inlist[j][k][1]])
			
def setDominantCloneRegion(self,inlist,strict=True):
	# Cloned regions where digits in one clone are greater than (by position) all other clones
	inlist = list(map(self._procCellList,inlist))
	for j in range(1,len(inlist)):
		for k in range(len(inlist[0])):
			if strict is True:
				self.model.Add(self.cellValues[inlist[0][k][0]][inlist[0][k][1]] > self.cellValues[inlist[j][k][0]][inlist[j][k][1]])
			else:
				self.model.Add(self.cellValues[inlist[0][k][0]][inlist[0][k][1]] >= self.cellValues[inlist[j][k][0]][inlist[j][k][1]])
				
def setShakenCloneRegion(self,inlist,noRepeat=False):
	inlist = list(map(self._procCellList,inlist))
	cloneCounts = []
	myDigits = list(self.digits)
	for j in range(len(inlist)): # Loop over clones
		# Create the variables which will count the number of appearances of a digit in this clone
		thisCloneCount = []
		for k in range(len(myDigits)): # Loop over the digits
			# Create the count variables
			v = self.model.NewIntVar(0,len(inlist[j]),'numberOfAppearancesOfDigit{:d}inClone{:d}'.format(myDigits[k],j))
			thisCloneCount.append(v)
			if j > 0:
				self.model.Add(cloneCounts[0][k] == v) # Force the total number of appearances of each digit to equal those in the first clone
				
			# Create the Booleans and 0/1 integer to pair cells to digits
			thisDigitCount = []
			for x in inlist[j]:
				v1 = self.model.NewBoolVar('cell{:d}{:d}Is{:d}'.format(x[0],x[1],myDigits[k]))
				v2 = self.model.NewIntVar(0,1,'cell{:d}{:d}Is{:d}'.format(x[0],x[1],myDigits[k]))
				self.model.Add(v2 == 1).OnlyEnforceIf(v1)
				self.model.Add(v2 == 0).OnlyEnforceIf(v1.Not())
				self.model.Add(self.cellValues[x[0]][x[1]] == myDigits[k]).OnlyEnforceIf(v1)
				self.model.Add(self.cellValues[x[0]][x[1]] != myDigits[k]).OnlyEnforceIf(v1.Not())
				thisDigitCount.append(v2)
			self.model.Add(sum(thisDigitCount) == v)
		cloneCounts.append(thisCloneCount)
	
		if noRepeat:
			self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in inlist[j]])
	
def setCage(self,inlist,value = None):
	inlist = self._procCellList(inlist)
	self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in inlist])
	if value is not None:
		self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in inlist) == value)
		
def setRepeatingCage(self,inlist,value):
	inlist = self._procCellList(inlist)
	self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in inlist) == value)
	
def setMedianCage(self,inlist,value):
	inlist = self._procCellList(inlist)
	equalVars = [self.model.NewBoolVar('MedianEqual{:d}'.format(i)) for i in range(len(inlist))]
	gtltVars = [self.model.NewBoolVar('MedianGreaterThan{:d}'.format(i)) for i in range(len(inlist))]
	ternVars = [self.model.NewIntVar(-1,1,'MedianTern{:d}'.format(i)) for i in range(len(inlist))]
	for i in range(len(inlist)):
		self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == value).OnlyEnforceIf([equalVars[i]])
		self.model.AddBoolAnd([gtltVars[i]]).OnlyEnforceIf(equalVars[i])	#Pegs unneeded gtlt to True if equal
		self.model.Add(ternVars[i] == 0).OnlyEnforceIf(equalVars[i])
		self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] > value).OnlyEnforceIf([equalVars[i].Not(),gtltVars[i]])
		self.model.Add(ternVars[i] == 1).OnlyEnforceIf([equalVars[i].Not(),gtltVars[i]])
		self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < value).OnlyEnforceIf([equalVars[i].Not(),gtltVars[i].Not()])
		self.model.Add(ternVars[i] == -1).OnlyEnforceIf([equalVars[i].Not(),gtltVars[i].Not()])
		
	self.model.AddBoolOr(equalVars)	# At least some cell equals the median
	self.model.Add(sum(ternVars) == 0)	# Ensures there are an equal number of values less than vs. greater than the median
	
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
			
def setMOTECage(self,inlist):
	# A MOTE cage has more odd than even cells
	inlist = self._procCellList(inlist)
	if self.isParity is False:
		self._setParity()
	self.model.Add(sum([self.cellParity[inlist[i][0]][inlist[i][1]] for i in range(len(inlist))]) >= (len(inlist)+2)//2)
	
def setMETOCage(self,inlist):
	# A METO cage has more even than odd cells
	inlist = self._procCellList(inlist)
	if self.isParity is False:
		self._setParity()
	self.model.Add(sum([self.cellParity[inlist[i][0]][inlist[i][1]] for i in range(len(inlist))]) <= (len(inlist)-1)//2)
	
def setUniparityCage(self,inlist):
	# A uniparity cage has cells with only one parity
	inlist = self._procCellList(inlist)
	if self.isParity is False:
		self._setParity()
	for i in range(len(inlist)-1):
		self.model.Add(self.cellParity[inlist[i][0]][inlist[i][1]] == self.cellParity[inlist[i+1][0]][inlist[i+1][1]])
		
def setEquiparityCage(self,inlist):
	inlist = self._procCellList(inlist)
	if self.isParity is False:
		self._setParity()
	self.model.Add(2*sum([self.cellParity[inlist[i][0]][inlist[i][1]] for i in range(len(inlist))]) == len(inlist))
	
def setAllOddOrEven(self,inlist):
	if self.isParity is False:
		self._setParity()
	inlist = set(self._procCellList(inlist))
	
	for i in range(len(self.regions)):
		rList = list(inlist & set(self.regions[i]))
		if len(rList) > 1:
			for j in range(1,len(rList)):
				self.model.Add(self.cellParity[rList[0][0]][rList[0][1]] == self.cellParity[rList[j][0]][rList[j][1]])

def setPuncturedCage(self,inlist,value,puncture=1):
	# A punctured cage is one with no repeated digits, where the given value is the sum of some subset of 
	# digits in the cage, less the number of punctured digits. So a cage containing 1,2,3,4 could be clued
	# with 6, 7, 8 or 9.
	inlist = self._procCellList(inlist)
	
	varBitmap = self._varBitmap('PuncturedCageRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1]),math.comb(len(inlist),puncture))
	varTrack = 0
	
	cI = CombinationIterator(len(inlist)-1,puncture)
	comb = cI.getNext()
	
	while comb is not None:
		self.model.Add(sum(self.cellValues[inlist[i][0]][inlist[i][1]] for i in range(len(inlist)) if i not in comb) == value).OnlyEnforceIf(varBitmap[varTrack])
		varTrack = varTrack + 1
		comb = cI.getNext()
		
def setPsychoKillerCage(self,inlist,value):
	inlist = self._procCellList(inlist)
	refDigits = []
	for i in range(len(inlist)):
		relRow = inlist[i][0] % 3
		relCol = inlist[i][1] % 3
		varBitmap = self._varBitmap('PsychoKillerRow{:d}Col{:d}'.format(inlist[i][0],inlist[i][1]),self.boardWidth)
		c = self.model.NewIntVar(1,self.boardWidth,'PKRefDigit')
		for j in range(self.boardWidth):
			refRow = 3*(j//3) + relRow
			refCol = 3*(j%3) + relCol
			self.model.Add(c == self.cellValues[refRow][refCol]).OnlyEnforceIf(varBitmap[j])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == j+1).OnlyEnforceIf(varBitmap[j])
		refDigits.append(c)
	self.model.Add(sum(refDigits) == value)

def setKnappDanebenCage(self,inlist,value):
	inlist = self._procCellList(inlist)
	self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in inlist])
	c = self.model.NewBoolVar('KnappDaneben')
	self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in inlist) == value+1).OnlyEnforceIf(c)
	self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in inlist) == value-1).OnlyEnforceIf(c.Not())
	
def setEqualSumCages(self,inlist):
	# A list of lists of cells, such that the sum of cells in each list is the same
	thisList = self._procCellList(inlist[0])
	baseSum = sum(self.cellValues[x[0]][x[1]] for x in thisList)
	for i in range(1,len(inlist)):
		thisList = self._procCellList(inlist[1])
		self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in thisList) == baseSum)

def setCapsule(self,inlist):
	# A capsule has the same number of even and odd digits
	self.setEquiparityCage(inlist)
		
def setDavidAndGoliath(self,inlist,borderDigit=5,borderType=0):
	# The pair contains at least one David digit and at least one Goliath digit, where any overlapping digit itself meets both conditions
	inlist = self._procCellList(inlist)
	d = [self.model.NewBoolVar('david') for i in range(2)]
	g = [self.model.NewBoolVar('goliath') for i in range(2)]
	for i in range(2):
		if borderType <= 0: # borderDigit is a David digit
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] <= borderDigit).OnlyEnforceIf(d[i])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] > borderDigit).OnlyEnforceIf(d[i].Not())
		else:
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < borderDigit).OnlyEnforceIf(d[i])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] >= borderDigit).OnlyEnforceIf(d[i].Not())
		if borderType >= 0: # borderDigit is a Goliath digit
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] >= borderDigit).OnlyEnforceIf(g[i])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < borderDigit).OnlyEnforceIf(g[i].Not())
		else:
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] > borderDigit).OnlyEnforceIf(d[i])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] <= borderDigit).OnlyEnforceIf(g[i].Not())
	self.model.AddBoolOr(d)
	self.model.AddBoolOr(g)

def setDigitCountCage(self,inlist,value):
	# A digit count cage specifies the number of distinct digits that appear in the cage...h/t clover!
	inlist = self._procCellList(inlist)
	digits = list(self.digits)
	digitCellBools = [[self.model.NewBoolVar('DigitCellPairs') for i in range(len(digits))] for j in range(len(inlist))]
	digitCellInts = [[self.model.NewIntVar(0,1,'DigitCellPairs') for i in range(len(digits))] for j in range(len(inlist))]
	digitBools = [self.model.NewBoolVar('DigitCounts') for i in range(len(digits))]
	digitInts = [self.model.NewIntVar(0,1,'DigitCounts') for i in range(len(digits))]
	for j in range(len(inlist)):
		for i in range(len(digits)):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] == digits[i]).OnlyEnforceIf(digitCellBools[j][i])
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] != digits[i]).OnlyEnforceIf(digitCellBools[j][i].Not())
			self.model.Add(digitCellInts[j][i] == 1).OnlyEnforceIf(digitCellBools[j][i])
			self.model.Add(digitCellInts[j][i] == 0).OnlyEnforceIf(digitCellBools[j][i].Not())
			
	for i in range(len(digits)):
		self.model.Add(sum([digitCellInts[j][i] for j in range(len(inlist))]) > 0).OnlyEnforceIf(digitBools[i])
		self.model.Add(sum([digitCellInts[j][i] for j in range(len(inlist))]) == 0).OnlyEnforceIf(digitBools[i].Not())
		self.model.Add(digitInts[i] == 1).OnlyEnforceIf(digitBools[i])
		self.model.Add(digitInts[i] == 0).OnlyEnforceIf(digitBools[i].Not())
	
	self.model.Add(sum([digitInts[i] for i in range(len(digits))]) == value)

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

def setZone(self,inlist,values,nulls={}):
	# A zone is an area with potentially repeating values; the clue is a list of digits that must appear in the zone
	inlist = self._procCellList(inlist)
	for x in set(values):
		xVars = []
		for i in range(len(inlist)):
			c = self.model.NewBoolVar('ZoneR{:d}C{:d}V{:d}'.format(inlist[i][0],inlist[i][1],x))
			# Tie Boolean to integer so we can count instances
			cI = self.model.NewIntVar(0,1,'ZoneIntR{:d}C{:d}V{:d}'.format(inlist[i][0],inlist[i][1],x))
			self.model.Add(cI == 1).OnlyEnforceIf(c)
			self.model.Add(cI == 0).OnlyEnforceIf(c.Not())
			xVars.append(cI)
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == x).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] != x).OnlyEnforceIf(c.Not())
			
		self.model.Add(sum(xVars) == values.count(x))
		
	for x in nulls:
		xVars = []
		for i in range(len(inlist)):
			c = self.model.NewBoolVar('ZoneR{:d}C{:d}V{:d}'.format(inlist[i][0],inlist[i][1],x))
			# Tie Boolean to integer so we can count instances
			cI = self.model.NewIntVar(0,1,'ZoneIntR{:d}C{:d}V{:d}'.format(inlist[i][0],inlist[i][1],x))
			self.model.Add(cI == 1).OnlyEnforceIf(c)
			self.model.Add(cI == 0).OnlyEnforceIf(c.Not())
			xVars.append(cI)
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == x).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] != x).OnlyEnforceIf(c.Not())
			
		self.model.Add(sum(xVars) == 0)
		
def setLookAndSayCage(self,inlist,value):
	# A look and say is basically a zone, possibly with nulls. Just need to parse the string and pass to setZone
	s = list(value)
	values=[]
	nulls=set()
	while len(s) > 0:
		count = int(s.pop(0))
		value = int(s.pop(0))
		if count == 0:
			nulls.add(value)
		else:
			values = values + [value for i in range(count)]
	self.setZone(inlist,values,nulls)
	
def setPsychoLookAndSayCage(self,inlist,value):
	inlist = self._procCellList(inlist)
	# First use the copied psycho code to get a list of variables to which the psycho cage actually refers
	refDigits = []
	for i in range(len(inlist)):
		relRow = inlist[i][0] % 3
		relCol = inlist[i][1] % 3
		varBitmap = self._varBitmap('PsychoKillerRow{:d}Col{:d}'.format(inlist[i][0],inlist[i][1]),self.boardWidth)
		c = self.model.NewIntVar(1,self.boardWidth,'PKRefDigit')
		for j in range(self.boardWidth):
			refRow = 3*(j//3) + relRow
			refCol = 3*(j%3) + relCol
			self.model.Add(c == self.cellValues[refRow][refCol]).OnlyEnforceIf(varBitmap[j])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == j+1).OnlyEnforceIf(varBitmap[j])
		refDigits.append(c)
	
	# Now, we need to count digits amongst these referred variables. We copy the look-and-say parsing code to get a value and its number of appearances.
	s = list(value)
	while len(s) > 0:
		count = int(s.pop(0))
		x = int(s.pop(0))
		
		# Now we should be able to copy the cell counting code from zones to get us home.
		xVars = []
		for i in range(len(refDigits)):
			c = self.model.NewBoolVar('PsychoLookAndSayR{:d}C{:d}V{:d}'.format(inlist[i][0],inlist[i][1],x))
			# Tie Boolean to integer so we can count instances
			cI = self.model.NewIntVar(0,1,'PsychoLookAndSayIntR{:d}C{:d}V{:d}'.format(inlist[i][0],inlist[i][1],x))
			self.model.Add(cI == 1).OnlyEnforceIf(c)
			self.model.Add(cI == 0).OnlyEnforceIf(c.Not())
			xVars.append(cI)
			self.model.Add(refDigits[i] == x).OnlyEnforceIf(c)
			self.model.Add(refDigits[i] != x).OnlyEnforceIf(c.Not())
			
		self.model.Add(sum(xVars) == count)
		
def setOrderSumCages(self,inlist,slow=False,repeat=False):
	# A list of cages whose sum increases based on the order in the list
	inlist = list(map(self._procCellList,inlist))
	for j in range(len(inlist)):
		if repeat is False:
			self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in inlist[j]])
		if j < len(inlist)-1:
			if slow is True:
				self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in inlist[j]) <= sum(self.cellValues[x[0]][x[1]] for x in inlist[j]))
			else:
				self.model.Add(sum(self.cellValues[x[0]][x[1]] for x in inlist[j]) < sum(self.cellValues[x[0]][x[1]] for x in inlist[j]))

def setMagicSquare(self,row,col=-1):
	if col == -1:
		(row,col) = self._procCell(row)
	tSum = (self.boardWidth+1)*self.boardSizeRoot // 2
	for i in range(self.boardSizeRoot):
		self.model.Add(sum(self.cellValues[row+i][col+j] for j in range(self.boardSizeRoot)) == tSum) # Row sum
		self.model.Add(sum(self.cellValues[row+j][col+i] for j in range(self.boardSizeRoot)) == tSum) # Column sum
	
	self.model.Add(sum(self.cellValues[row+j][col+j] for j in range(self.boardSizeRoot)) == tSum) # Main diagonal sum
	self.model.Add(sum(self.cellValues[row+j][col+self.boardSizeRoot-1-j] for j in range(self.boardSizeRoot)) == tSum) # Off diagonal sum
	
def setEntropkiWhite(self,row,col=-1,hv=-1):
	if self.isEntropy is False:
		self._setEntropy()
	if col == -1:
		(row,col,hv) = self._procCell(row)
	# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
	self.model.Add(self.cellEntropy[row][col] != self.cellEntropy[row+hv][col+(1-hv)])
	
def setEntropkiBlack(self,row,col=-1,hv=-1):
	if self.isEntropy is False:
		self._setEntropy()
	if col == -1:
		(row,col,hv) = self._procCell(row)
	# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
	self.model.Add(self.cellEntropy[row][col] == self.cellEntropy[row+hv][col+(1-hv)])

def setEntropkiWhiteArray(self,cells):
	for x in cells: self.setEntropkiWhite(x)
	
def setEntropkiBlackArray(self,cells):
	for x in cells: self.setEntropkiBlack(x)
	
def setEntropkiArray(self,cells):
	cellList = self._procCellList(cells)
	for x in cellList:
		if x[3] == self.White:
			self.setEntropkiWhite(x[0],x[1],x[2])
		else:
			self.setEntropkiBlack(x[0],x[1],x[2])
			
def setParityDotWhite(self,row,col=-1,hv=-1):
	if self.isParity is False:
		self._setParity()
	if col == -1:
		(row,col,hv) = self._procCell(row)
	# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
	self.model.Add(self.cellParity[row][col] != self.cellParity[row+hv][col+(1-hv)])
	
def setParityDotBlack(self,row,col=-1,hv=-1):
	if self.isParity is False:
		self._setParity()
	if col == -1:
		(row,col,hv) = self._procCell(row)
	# Note: row,col is the top/left cell of the pair, hv = 0 -> horizontal, 1 -> vertical
	self.model.Add(self.cellParity[row][col] == self.cellParity[row+hv][col+(1-hv)])

def setParityDotWhiteArray(self,cells):
	for x in cells: self.setParityDotWhite(x)
	
def setParityDotBlackArray(self,cells):
	for x in cells: self.setParityDotBlack(x)
	
def setParityDotArray(self,cells):
	cellList = self._procCellList(cells)
	for x in cellList:
		if x[3] == self.White:
			self.setParityDotWhite(x[0],x[1],x[2])
		else:
			self.setParityDotBlack(x[0],x[1],x[2])

def setGenetic(self,inlist):
	inlist = self._procCellList(inlist)
	if self.isEntropy is False:
		self._setEntropy()
	if self.isParity is False:
		self._setParity()
		
	p1Parity = self.model.NewBoolVar('GeneticsP1ParityMatchRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1]))
	p1Entropy = self.model.NewBoolVar('GeneticsP1EntropyMatchRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1]))
	p2Parity = self.model.NewBoolVar('GeneticsP2ParityMatchRow{:d}Col{:d}'.format(inlist[1][0],inlist[1][1]))
	p2Entropy = self.model.NewBoolVar('GeneticsP2EntropyMatchRow{:d}Col{:d}'.format(inlist[1][0],inlist[1][1]))
	
	self.model.Add(self.cellParity[inlist[0][0]][inlist[0][1]] == self.cellParity[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p1Parity)
	self.model.Add(self.cellParity[inlist[0][0]][inlist[0][1]] != self.cellParity[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p1Parity.Not())
	self.model.Add(self.cellParity[inlist[1][0]][inlist[1][1]] == self.cellParity[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p2Parity)
	self.model.Add(self.cellParity[inlist[1][0]][inlist[1][1]] != self.cellParity[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p2Parity.Not())
	self.model.Add(self.cellEntropy[inlist[0][0]][inlist[0][1]] == self.cellEntropy[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p1Entropy)
	self.model.Add(self.cellEntropy[inlist[0][0]][inlist[0][1]] != self.cellEntropy[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p1Entropy.Not())
	self.model.Add(self.cellEntropy[inlist[1][0]][inlist[1][1]] == self.cellEntropy[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p2Entropy)
	self.model.Add(self.cellEntropy[inlist[1][0]][inlist[1][1]] != self.cellEntropy[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(p2Entropy.Not())
	
	self.model.AddBoolOr([p1Parity,p2Parity])	#Inherit parity from a parent
	self.model.AddBoolOr([p1Entropy,p2Entropy])	#Inherit entropy from a parent
	self.model.AddBoolOr([p1Parity,p1Entropy])	#Inherit something from parent 1
	self.model.AddBoolOr([p2Parity,p2Entropy])	#Inherit something from parent 2
	
def setGeneticArray(self,cells):
	for x in cells: self.setGenetic(x)
	
def setParitySnake(self,row1,col1,row2,col2,parity=None):
	if self.isParity is False:
		self._setParity()
	r1 = row1 - 1
	c1 = col1 - 1
	r2 = row2 - 1
	c2 = col2 - 1
	if parity is None:
		parity = self.cellParity[r1][c1]
		
	self.model.Add(self.cellParity[r1][c1] == parity)
	self.model.Add(self.cellParity[r2][c2] == parity)
	
	pathBool = []
	pathInt = []
	for i in range(self.boardWidth):
		tB = []
		tI = []
		for j in range(self.boardWidth):
			cB = self.model.NewBoolVar('snake{:d}{:d}'.format(i,j))
			cI = self.model.NewIntVar(0,1,'snake{:d}{:d}'.format(i,j))
			self.model.Add(cI == 1).OnlyEnforceIf(cB)
			self.model.Add(cI == 0).OnlyEnforceIf(cB.Not())
			tB.append(cB)
			tI.append(cI)
		pathBool.insert(i,tB)
		pathInt.insert(i,tI)
		
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			if (i,j) == (r1,c1) or (i,j) == (r2,c2):
				self.model.Add(sum(pathInt[x[0]][x[1]] for x in self.getOrthogonalNeighbors(i,j)) == 1)
				self.model.AddBoolAnd(pathBool[i][j])
			else:
				self.model.Add(sum(pathInt[x[0]][x[1]] for x in self.getOrthogonalNeighbors(i,j)) == 2).OnlyEnforceIf(pathBool[i][j])
				self.model.Add(self.cellParity[i][j] == parity).OnlyEnforceIf(pathBool[i][j])
				
def setConsecutiveChainRegion(self,inlist):
	self.setRenbanLine(inlist)		# Ensures region contains a set of consecutive digits of the right size
	inlist = self._procCellList(inlist)
	inset = set(inlist)
	rMin = self._varBitmap('ConsecutiveChainRegionMin',len(inlist))
	rMax = self._varBitmap('ConsecutiveChainRegionMax',len(inlist))
	for i in range(len(inlist)):
		for j in range(len(inlist)):
			if i == j:
				# Just null out this case...a value can't be both min and max
				self.model.AddBoolAnd([rMin[i][0].Not()]).OnlyEnforceIf(rMin[i]+rMax[j])
			else:
				# First, enforce min and max constraints regardless of whether or not both conditions are SAT
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(rMin[i])
				self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(rMax[j])
				
				# Now construct the chain
				for k in range(len(inlist)):
					x = inlist[k]
					neigh = inset & {(x[0]-1,x[1]),(x[0]+1,x[1]),(x[0],x[1]-1),(x[0],x[1]+1)}
					if len(neigh) == 1:
						if k == i:
							for y in neigh:
								self.model.Add(self.cellValues[y[0]][y[1]] - self.cellValues[x[0]][x[1]] == 1).OnlyEnforceIf(rMin[i]+rMax[j])
						elif k == j:
							for y in neigh:
								self.model.Add(self.cellValues[x[0]][x[1]] - self.cellValues[y[0]][y[1]] == 1).OnlyEnforceIf(rMin[i]+rMax[j])
						else:
							self.model.AddBoolAnd(rMin[i][0].Not()).OnlyEnforceIf(rMin[i]+rMax[j])
					else:
						c = self._varBitmap('ConsecutiveChainRegion',len(neigh))
						d = self._varBitmap('ConsecutiveChainRegion',len(neigh))
						varTrack = 0
						if k == i:
							for y in neigh:
								# If min, only enforce single neighbor
								self.model.Add(self.cellValues[y[0]][y[1]] - self.cellValues[x[0]][x[1]] == 1).OnlyEnforceIf(c[varTrack]+rMin[i]+rMax[j])
								varTrack = varTrack + 1
							# Peg d variables in this case
							self.model.AddBoolAnd(d[0]).OnlyEnforceIf(rMin[i]+rMax[j])
						elif k == j:
							for y in neigh:
								# If max, only enforce single neighbor
								self.model.Add(self.cellValues[x[0]][x[1]] - self.cellValues[y[0]][y[1]] == 1).OnlyEnforceIf(c[varTrack]+rMin[i]+rMax[j])
								varTrack = varTrack + 1
							# Peg d variables in this case
							self.model.AddBoolAnd(d[0]).OnlyEnforceIf(rMin[i]+rMax[j])
						else:
							for y in neigh:
								# c enforces bigger neighbor, d enforces smaller neighbor
								self.model.Add(self.cellValues[y[0]][y[1]] - self.cellValues[x[0]][x[1]] == 1).OnlyEnforceIf(c[varTrack]+rMin[i]+rMax[j])
								self.model.Add(self.cellValues[x[0]][x[1]] - self.cellValues[y[0]][y[1]] == 1).OnlyEnforceIf(d[varTrack]+rMin[i]+rMax[j])
								varTrack = varTrack + 1
	
def setAntiQueenCell(self,row,col=-1,r2=-1,c2=-1):
	# The digit in an anti-queen cell cannot repeat on any diagonal. If a second cell is given, only repeats in the direction of the given cell are forbidden
	if col == -1:
		T = self._procCell(row)
		row = T[0]
		col = T[1]
		values = [T[i] for i in range(2,len(T))]
		if len(values) == 2:
			r2 = values[0] - 1
			c2 = values[1] - 1
		else:
			r2 = -1
	
	if r2 == -1:
		# No repeats on any diagonals
		dCells = {(row+m*k,col+n*k) for k in range(1,self.boardWidth) for m in [-1,1] for n in [-1,1]} & {(k,m) for k in range(self.boardWidth) for m in range(self.boardWidth)}
	else:
		m = r2 - row
		n = c2 - col
		dCells = {(row+m*k,col+n*k) for k in range(1,self.boardWidth)} & {(k,j) for k in range(self.boardWidth) for j in range(self.boardWidth)}

	for x in dCells:
		self.model.Add(self.cellValues[x[0]][x[1]] != self.cellValues[row][col])
        
def setTripleTab(self,row1,col1,uldr,digits,cellCount=3):
	row = row1 - 1
	col = col1 - 1
	if uldr == self.Up:
		hStep = 0
		vStep = -1
	elif uldr == self.Down:
		hStep = 0
		vStep = 1
	elif uldr == self.Left:
		hStep = -1
		vStep = 0
	else:
		hStep = 1
		vStep = 0
	
	for d in digits:
		cells = list({(row+i*vStep,col+i*hStep) for i in range(1,cellCount+1)} & {(i,j) for i in range(self.boardWidth) for j in range(self.boardWidth)})
		vars = [self.model.NewBoolVar('') for i in range(len(cells))]
		for i in range(len(cells)):
			self.model.Add(self.cellValues[cells[i][0]][cells[i][1]] == d).OnlyEnforceIf(vars[i])
			self.model.Add(self.cellValues[cells[i][0]][cells[i][1]] != d).OnlyEnforceIf(vars[i].Not())
		self.model.AddBoolOr(vars)