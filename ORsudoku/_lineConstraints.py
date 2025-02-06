from ORsudoku.combinationIterator import CombinationIterator
import math

def setArrow(self,inlist):
	inlist = self._procCellList(inlist)
	self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))))
	
def setHeavyArrow(self,inlist,mult=2):
	inlist = self._procCellList(inlist)
	self.model.Add(mult*self.cellValues[inlist[0][0]][inlist[0][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))))
	
def setDoubleArrow(self,inlist):
	inlist = self._procCellList(inlist)
	self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] + self.cellValues[inlist[-1][0]][inlist[-1][1]]== sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist)-1)))

def setPointingArrow(self,inlist):
	inlist = self._procCellList(inlist)
	# Pointing arrow is an arrow, but it also points, extending in last direction, to its total sum
	self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))))

	vert = inlist[-1][0]-inlist[-2][0] # Vertical delta to compute extension direction
	horiz = inlist[-1][1]-inlist[-2][1] # Horizontal delta to compute extension direction
	
	tcells = [self.cellValues[inlist[-1][0]+k*vert][inlist[-1][1]+k*horiz] for k in range(1,self.boardWidth) if inlist[-1][0]+k*vert in range(self.boardWidth) and inlist[-1][1]+k*horiz in range(self.boardWidth)]
	tvars = [self.model.NewBoolVar('PointingArrowFinderHeadRow{:d}Col{:d}Cell{:d}'.format(inlist[0][0],inlist[0][1],i)) for i in range(len(tcells))]
	for j in range(len(tvars)):
		self.model.Add(tcells[j] == self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf(tvars[j])
		self.model.Add(tcells[j] != self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf(tvars[j].Not())
	self.model.AddBoolOr(tvars)
	
def setMultiDigitSumArrow(self,inlist,n=1):
	# Arrow where the bulb is multiple digits. First n elements of the list are in the circle, most significant (100s or 10s, usually) to least.
	inlist = self._procCellList(inlist)
	circle = self.cellValues[inlist[0][0]][inlist[0][1]]
	for i in range(1,n):
		circle = 10*circle + self.cellValues[inlist[i][0]][inlist[i][1]]
	self.model.Add(circle == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(n,len(inlist))))

def setMissingArrow(self,inlist):
	# Arrow where one end or the other is the sum of the other cells along the arrow
	inlist = self._procCellList(inlist)
	if (len(inlist) > 2):
		c = self.model.NewBoolVar('MissingArrow')
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist)))).OnlyEnforceIf(c)
		self.model.Add(self.cellValues[inlist[-1][0]][inlist[-1][1]] == sum(self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist)-1))).OnlyEnforceIf(c.Not())
	else:
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == self.cellValues[inlist[1][0]][inlist[1][1]])
	
def setRepeatingArrow(self,inlist,repeat=2):
	inlist = self._procCellList(inlist)
	bulb = inlist.pop(0)
	varBitmap = self._varBitmap('RepeatingArrow',math.comb(len(inlist),repeat-1))
	varTrack = 0
	bulbVar = self.cellValues[bulb[0]][bulb[1]]
	
	cI = CombinationIterator(len(inlist)-1,repeat-1)
	comb = cI.getNext()
	while comb is not None:
		ind = [-1] + comb + [len(inlist)-1]
		for j in range(len(ind)-1):
			self.model.Add(sum(self.cellValues[inlist[k][0]][inlist[k][1]] for k in range(ind[j]+1,ind[j+1]+1)) == bulbVar).OnlyEnforceIf(varBitmap[varTrack])
		comb = cI.getNext()
		varTrack = varTrack + 1

def setThermo(self,inlist,slow=False,missing=False,speed=False,broken=False,brokenThreshold=None,brokenMinDrop=None):
	if broken is True:
		if brokenThreshold is None:
			brokenThreshold = self.maxDigit
		if brokenMinDrop is None:
			brokenMinDrop = brokenThreshold - self.minDigit
	else:
		brokenThreshold = 0
		brokenMinDrop = 0
	inlist = self._procCellList(inlist)
	if missing is True:
		M = [self.model.NewBoolVar('ThermoMissingSwitch')]
	else:
		M = [self.model.NewBoolVar('AlwaysTrue')]
		self.model.AddBoolAnd(M[0]).OnlyEnforceIf(M[0].Not())
	Mnot = [x.Not() for x in M]

	# We're setting up an array to allow us to have a structure to decide whether to break or not if we're doing broken thermos
	# For any case, we start with the default. If we are actually broken and have a chance to break due to the region topology
	# we'll replace B and Bnot within the loop.
	baseB = [self.model.NewBoolVar('AlwaysTrue')]
	self.model.AddBoolAnd(baseB[0]).OnlyEnforceIf(baseB[0].Not())
	baseBnot = [x.Not() for x in baseB]

	for j in range(len(inlist)-1):
		if broken is True and self.getRegion(inlist[j][0],inlist[j][1]) != self.getRegion(inlist[j+1][0],inlist[j+1][1]):
			b = self.model.NewBoolVar('ThermoBreakSwitch')
			B = [b]
			Bnot = [b.Not()]
			# The only way breaking is a choice is if the last cell in the region is at the brokenThreshold
			# so we enforce that. However, we do not have the complimentary choice, since even if we are above the
			# threshold we have the opportunity to keep going normally
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] >= brokenThreshold).OnlyEnforceIf(M+Bnot)
			self.model.Add(self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= brokenThreshold).OnlyEnforceIf(Mnot+Bnot)
		else:
			B = baseB
			Bnot = baseBnot
		# This is normal processing, when B is true.
		if slow is True or speed == 'slow':
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] <= self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(M+B)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] >= self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(Mnot+B)
		elif slow is False and speed == 'fast':
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + 1 < self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(M+B)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.cellValues[inlist[j+1][0]][inlist[j+1][1]] + 1).OnlyEnforceIf(Mnot+B)
		elif slow is False and isinstance(speed, int):
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + speed < self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(M+B)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.cellValues[inlist[j+1][0]][inlist[j+1][1]] + speed).OnlyEnforceIf(Mnot+B)
		else:
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(M+B)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(Mnot+B)
		
		# Now the processing if there's a break
		self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= brokenMinDrop).OnlyEnforceIf(M+Bnot)
		self.model.Add(self.cellValues[inlist[j+1][0]][inlist[j+1][1]] - self.cellValues[inlist[j][0]][inlist[j][1]] >= brokenMinDrop).OnlyEnforceIf(Mnot+Bnot)
		
def setSlowThermo(self,inlist,missing=False):
	self.setThermo(inlist,True,missing)
	
def setFastThermo(self,inlist,missing=False):
	self.setThermo(inlist,False,missing,'fast')

def setOddEvenThermo(self,inlist,slow=False,missing=False):
	if 'Parity' not in self._propertyInitialized:
		self._setParity()
	self.setThermo(inlist,slow,missing)
	inlist = self._procCellList(inlist)
	for j in range(len(inlist)-1):
		self.model.Add(self.cellParity[inlist[j][0]][inlist[j][1]] == self.cellParity[inlist[j+1][0]][inlist[j+1][1]])
		
def setSlowOddEvenThermo(self,inlist,missing=False):
	self.setOddEvenThermo(inlist,True,missing)
	
def setMissingThermo(self,inlist,slow=False):
	self.setThermo(inlist,slow,True)
	
def setBrokenThermo(self,inlist,b1=None,b2=None):
	self.setThermo(inlist,broken=True,brokenThreshold=b1,brokenMinDrop=b2)
	
def setDoubleThermo(self,inlist,slow=False,missing=False,increaseCriteria='Both'):
	if 'Parity' not in self._propertyInitialized:
		self._setParity()
	L = self._procCellList(inlist)

	# This Q array is almost never used, except for the weird case where we have missing thermos, and we want to allow the
	# possibility that different parities have bulbs at different ends. So we'll default it to this never true state.
	Q = [self.model.NewBoolVar('AlwaysFalse')]
	self.model.AddBoolAnd(Q[0].Not()).OnlyEnforceIf(Q[0])
	Qnot = Q
	if missing is True:
		M = [self.model.NewBoolVar('DoubleThermoMissingSwitch')]
		if increaseCriteria == 'BothMissing':
			Q = [self.model.NewBoolVar('DoubleThermoMissingOddSwitch')]
			Qnot = [x.Not() for x in Q]
	else:
		M = [self.model.NewBoolVar('AlwaysTrue')]
		self.model.AddBoolAnd(M[0]).OnlyEnforceIf(M[0].Not())
	Mnot = [x.Not() for x in M]
	parityBools = [self.model.NewBoolVar('DoubleThermoParityBools') for j in range(len(L))]
	for i in range(len(L)):
		self.model.Add(self.cellParity[L[i][0]][L[i][1]] == 1).OnlyEnforceIf(parityBools[i])
		self.model.Add(self.cellParity[L[i][0]][L[i][1]] == 0).OnlyEnforceIf(parityBools[i].Not())
		myQ = Q
		myQnot = Qnot
		match increaseCriteria:
			case 'Both':
				P = []
			case 'BothMissing':
				P = [parityBools[i].Not()] # For even digits, we let the M array determine what to do
				myQ = Q + [parityBools[i]]
				myQnot = Qnot + [parityBools[i]]
			case 'MissingOpposite':
				P = [parityBools[i].Not()] # For even digits, we let the M array determine what to do
				myQ = Mnot+[parityBools[i]]	# This forces the odds to increase in the other direction
				myQnot = M+[parityBools[i]]
			case 'Even':
				P = [parityBools[i].Not()]
			case 'Odd':
				P = [parityBools[i]]
			case 'First':
				P = [self.model.NewBoolVar('DoubleThermoParityFirstMatch')]
				self.model.AddBoolAnd(P).OnlyEnforceIf([parityBools[0],parityBools[i]]+M)
				self.model.AddBoolAnd(P).OnlyEnforceIf([parityBools[-1],parityBools[i]]+Mnot)
				self.model.AddBoolAnd(P).OnlyEnforceIf([parityBools[0].Not(),parityBools[i].Not()]+M)
				self.model.AddBoolAnd(P).OnlyEnforceIf([parityBools[-1].Not(),parityBools[i].Not()]+Mnot)
				self.model.AddBoolAnd(P[0].Not()).OnlyEnforceIf([parityBools[0].Not(),parityBools[i]]+M)
				self.model.AddBoolAnd(P[0].Not()).OnlyEnforceIf([parityBools[-1].Not(),parityBools[i]]+Mnot)
				self.model.AddBoolAnd(P[0].Not()).OnlyEnforceIf([parityBools[0],parityBools[i].Not()]+M)
				self.model.AddBoolAnd(P[0].Not()).OnlyEnforceIf([parityBools[-1],parityBools[i].Not()]+Mnot)				
		for j in range(i+1,len(L)):
			c = self.model.NewBoolVar('DoubleThermoParitySwitch')
			self.model.Add(self.cellParity[L[i][0]][L[i][1]] == self.cellParity[L[j][0]][L[j][1]]).OnlyEnforceIf(c)
			self.model.Add(self.cellParity[L[i][0]][L[i][1]] != self.cellParity[L[j][0]][L[j][1]]).OnlyEnforceIf(c.Not())
			if slow is True:
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] <= self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([c]+M+P)
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] >= self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([c]+Mnot+P)
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] <= self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([c]+myQ)
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] >= self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([c]+myQnot)
			else:
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] < self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([c]+M+P)
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] > self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([c]+Mnot+P)
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] < self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([c]+myQ)
				self.model.Add(self.cellValues[L[i][0]][L[i][1]] > self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf([c]+myQnot)
				
def setRemovedBulbThermo(self,inlist,slow=False):
	L = self._procCellList(inlist)
	minCell = self.model.NewIntVar(self.minDigit,self.maxDigit,'RemovedBulbMinimum')
	self.model.AddMinEquality(minCell,[self.cellValues[x[0]][x[1]] for x in L])
	varBitmap = self._varBitmap('RemovedBulbCellSelection',len(L))
	for i in range(len(L)):
		for j in range(i):
			if slow is True:
				self.model.Add(self.cellValues[L[j][0]][L[j][1]] >= self.cellValues[L[j+1][0]][L[j+1][1]]).OnlyEnforceIf(varBitmap[i])
			else:
				self.model.Add(self.cellValues[L[j][0]][L[j][1]] > self.cellValues[L[j+1][0]][L[j+1][1]]).OnlyEnforceIf(varBitmap[i])
		if i > 0:
			self.model.Add(self.cellValues[L[i-1][0]][L[i-1][1]] > self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf(varBitmap[i])
			# Even if thermo is slow, we insist on strict inequality so bulb placement is unique
		for j in range(i+1,len(L)):
			if slow is True:
				self.model.Add(self.cellValues[L[j-1][0]][L[j-1][1]] <= self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf(varBitmap[i])
			else:
				self.model.Add(self.cellValues[L[j-1][0]][L[j-1][1]] < self.cellValues[L[j][0]][L[j][1]]).OnlyEnforceIf(varBitmap[i])
				
def setCountTheOddsLine(self,inlist):
	if 'Parity' not in self._propertyInitialized:
		self._setParity()
		
	inlist = self._procCellList(inlist)
	self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == sum([self.cellParity[inlist[j][0]][inlist[j][1]] for j in range(1,len(inlist))]))

def setKeypadKnightLine(self,inlist):
	if self.boardWidth != 9:
		print('Keypad lines only supported on 9x9 board')
		sys.exit()
	inlist = self._procCellList(inlist)
	for j in range(len(inlist)-1):
		self.model.AddAllowedAssignments([self.cellValues[inlist[j][0]][inlist[j][1]],self.cellValues[inlist[j+1][0]][inlist[j+1][1]]],[(1,6),(1,8),(2,7),(2,9),(3,4),(3,8),(4,3),(4,9),(6,1),(6,7),(7,2),(7,6),(8,1),(8,3),(9,2),(9,4)])
		
def setKeypadKingLine(self,inlist):
	if self.boardWidth != 9:
		print('Keypad lines only supported on 9x9 board')
		sys.exit()
	inlist = self._procCellList(inlist)
	for j in range(len(inlist)-1):
		self.model.AddAllowedAssignments([self.cellValues[inlist[j][0]][inlist[j][1]],self.cellValues[inlist[j+1][0]][inlist[j+1][1]]],[(1,2),(1,4),(1,5),(2,1),(2,4),(2,5),(2,6),(2,3),(3,2),(3,5),(3,6),(4,1),(4,2),(4,5),(4,8),(4,7),(5,1),(5,2),(5,3),(5,4),(5,6),(5,7),(5,8),(5,9),(6,3),(6,2),(6,5),(6,8),(6,9),(7,4),(7,5),(7,8),(8,7),(8,4),(8,5),(8,6),(8,9),(9,8),(9,5),(9,6)])
		
def setPalindromeLine(self,inlist):
	inlist = self._procCellList(inlist)
	for j in range(len(inlist) // 2):
		self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] == self.cellValues[inlist[-j-1][0]][inlist[-j-1][1]])
		
def setParindromeLine(self,inlist):
	if 'Parity' not in self._propertyInitialized:
		self._setParity()
	inlist = self._procCellList(inlist)
	for j in range(len(inlist) // 2):
		self.model.Add(self.cellParity[inlist[j][0]][inlist[j][1]] == self.cellParity[inlist[-j-1][0]][inlist[-j-1][1]])
		
def setWeakPalindromeLine(self,inlist):
	if self.boardWidth != 9:
		print('Keyboard lines only supported on 9x9 board')
		sys.exit()
	inlist = self._procCellList(inlist)
	for j in range(len(inlist) // 2):
		self.model.AddAllowedAssignments([self.cellValues[inlist[j][0]][inlist[j][1]],self.cellValues[inlist[-j-1][0]][inlist[-j-1][1]]],[(1,1),(1,3),(3,1),(3,3),(2,2),(2,4),(4,2),(4,4),(5,5),(5,7),(5,9),(7,5),(7,7),(7,9),(9,5),(9,7),(9,9),(6,6),(6,8),(8,6),(8,8)])

def setParityLine(self,inlist):
	if 'Parity' not in self._propertyInitialized:
		self._setParity()
	inlist = self._procCellList(inlist)
	for j in range(len(inlist)-1):
		self.model.Add(self.cellParity[inlist[j][0]][inlist[j][1]] != self.cellParity[inlist[j+1][0]][inlist[j+1][1]])
		
def setRenbanLine(self,inlist):
	inlist = self._procCellList(inlist)
	self.model.AddAllDifferent([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))])
	for x in range(len(inlist)):
		for y in range(len(inlist)):
			self.model.Add(self.cellValues[inlist[x][0]][inlist[x][1]]-self.cellValues[inlist[y][0]][inlist[y][1]] < len(inlist))
			
def setRenrenbanbanLine(self,inlist):
	inlist = self._procCellList(inlist)
	varBitmap = self._varBitmap('RenrenbanbanLine',math.comb(len(inlist)-1,len(inlist)//2-1))
	varTrack = 0
	cI = CombinationIterator(len(inlist)-2,len(inlist)//2-1)
	comb = cI.getNext()
	while comb is not None:
		for myList in [[x for x in comb] + [len(inlist)-1],[x for x in range(len(inlist)-1) if x not in comb]]:
			for i in range(len(inlist)//2):
				x = inlist[myList[i]]
				for j in range(i+1,len(inlist)//2):
					y = inlist[myList[j]]
					self.model.Add(self.cellValues[x[0]][x[1]] - self.cellValues[y[0]][y[1]] > 0).OnlyEnforceIf(varBitmap[varTrack])
					self.model.Add(self.cellValues[x[0]][x[1]] - self.cellValues[y[0]][y[1]] < len(inlist)//2).OnlyEnforceIf(varBitmap[varTrack])
					self.model.Add(self.cellValues[y[0]][y[1]] - self.cellValues[x[0]][x[1]] < len(inlist)//2).OnlyEnforceIf(varBitmap[varTrack])
		comb = cI.getNext()
		varTrack = varTrack + 1
			
def setNotRenbanLine(self,inlist):
	inlist = self._procCellList(inlist)
	
	distBools = [self.model.NewBoolVar('NotRenbanDistinct') for i in range(len(inlist)) for j in range(len(inlist)) if i < j]
	varTrack = 0
	for i in range(len(inlist)):
		for j in range(i+1,len(inlist)):
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(distBools[varTrack])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] != self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(distBools[varTrack].Not())
			varTrack = varTrack + 1
	
	diffBools = [self.model.NewBoolVar('NotRenbanDistinct') for i in range(len(inlist)) for j in range(len(inlist))]
	varTrack = 0
	for i in range(len(inlist)):
		for j in range(len(inlist)):
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] - self.cellValues[inlist[j][0]][inlist[j][1]] >= len(inlist)).OnlyEnforceIf(diffBools[varTrack])
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] - self.cellValues[inlist[j][0]][inlist[j][1]] < len(inlist)).OnlyEnforceIf(diffBools[varTrack].Not())
			varTrack = varTrack + 1
	self.model.AddBoolOr(distBools + diffBools)
			
def setRunOnRenbanLine(self,inlist,n=5):
	# Each contiguous subsegment of length n is a Renban of length n
	# Note: we could just chunk this out as a bunch of overlapping Renbans, but that'll add a lot of repeated subtraction conditions
	# Let's do the first one that way, so we aren't duplicating quite as much code
	if len(inlist) >= n:
		self.setRenbanLine(inlist[0:n]) # Note: do this before doing procCellList, since the Renban call will proc it
	inlist = self._procCellList(inlist)
	for i in range(n,len(inlist)):
		self.model.AddAllDifferent([self.cellValues[inlist[i-j][0]][inlist[i-j][1]] for j in range(n)])
		for j in range(n):
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]]-self.cellValues[inlist[i-j][0]][inlist[i-j][1]] < n)
			self.model.Add(self.cellValues[inlist[i-j][0]][inlist[i-j][1]]-self.cellValues[inlist[i][0]][inlist[i][1]] < n)
				
def setMinWhispersLine(self,inlist,value):
	# Sets a whispers line where the minimum difference between two adjacent cells on the line is value
	inlist = self._procCellList(inlist)
	for j in range(len(inlist)-1):
		bit = self.model.NewBoolVar('MaxWhisperBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
		self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= value).OnlyEnforceIf(bit)
		self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= -1*value).OnlyEnforceIf(bit.Not())

def setMaxWhispersLine(self,inlist,value):
	# Sets a whispersline where the maximum difference between two adjacent cells on the line is value
	inlist = self._procCellList(inlist)
	for j in range(len(inlist)-1):
		self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] <= value)
		self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+1][0]][inlist[j+1][1]] >= -1*value)

def setGermanWhispersLine(self,inlist):
	self.setMinWhispersLine(inlist,5)
		
def setDutchWhispersLine(self,inlist):
	self.setMinWhispersLine(inlist,4)
		
def setChineseWhispersLine(self,inlist):
	self.setMaxWhispersLine(inlist,2)
	
def setMinExtendedWhispersLine(self,inlist,difference,reach):
	# Sets a whispers line where the minimum difference between two cells at most reach apart on the line is value 
	inlist = self._procCellList(inlist)
	for j in range(len(inlist)-1):
		for k in range(1,min(reach+1,len(inlist)-j)):
			bit = self.model.NewBoolVar('MinExtendedWhisperBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+k][0]][inlist[j+k][1]] >= difference).OnlyEnforceIf(bit)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+k][0]][inlist[j+k][1]] <= -1*difference).OnlyEnforceIf(bit.Not())
			
def setMaxExtendedWhispersLine(self,inlist,difference,reach):
	# Sets a whispers line where the maximum difference between two cells at most reach apart on the line is value 
	inlist = self._procCellList(inlist)
	for j in range(len(inlist)-1):
		for k in range(1,min(reach+1,len(inlist)-j)):
			bit = self.model.NewBoolVar('MaxExtendedWhisperBiggerRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1]))
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+k][0]][inlist[j+k][1]] <= difference).OnlyEnforceIf(bit)
			self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] - self.cellValues[inlist[j+k][0]][inlist[j+k][1]] >= -1*difference).OnlyEnforceIf(bit.Not())
			
def setRunOnNabnerLine(self,inlist):
	self.setMinExtendedWhispersLine(inlist,2,3)
	
def setEntropicWhispersLine(self,inlist):
	self.setMinExtendedWhispersLine(inlist,3,2)
		
def setEntropicLine(self,inlist):
	inlist = self._procCellList(inlist)
	if 'Entropy' not in self._propertyInitialized:
		self._setEntropy()
	
	if len(inlist) == 2:
		self.model.Add(self.cellEntropy[inlist[0][0]][inlist[0][1]] != self.cellEntropy[inlist[1][0]][inlist[1][1]])
	else:
		for j in range(len(inlist)-2):
			self.model.AddAllDifferent([self.cellEntropy[inlist[j][0]][inlist[j][1]],self.cellEntropy[inlist[j+1][0]][inlist[j+1][1]],self.cellEntropy[inlist[j+2][0]][inlist[j+2][1]]])

def setModularLine(self,inlist):
	inlist = self._procCellList(inlist)
	if 'Modular' not in self._propertyInitialized:
		self._setModular()
	
	if len(inlist) == 2:
		self.model.Add(self.cellModular[inlist[0][0]][inlist[0][1]] != self.cellModular[inlist[1][0]][inlist[1][1]])
	else:
		for j in range(len(inlist)-2):
			self.model.AddAllDifferent([self.cellModular[inlist[j][0]][inlist[j][1]],self.cellModular[inlist[j+1][0]][inlist[j+1][1]],self.cellModular[inlist[j+2][0]][inlist[j+2][1]]])
			
def setBetweenLine(self,inlist):
	inlist = self._procCellList(inlist)
	c = self.model.NewBoolVar('BetweenRow{:d}Col{:d}ToRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1],inlist[-1][0],inlist[-1][1]))
	
	# Case c true: first element of line is largest
	self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c)
	for j in range(1,len(inlist)-1):
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c)
		self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c)
		
	# Case c false: last element of line is largest
	self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] < self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c.Not())
	for j in range(1,len(inlist)-1):
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] < self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c.Not())
		self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c.Not())
		
def setLockoutLine(self,inlist):
	inlist = self._procCellList(inlist)
	c = self.model.NewBoolVar('LockoutRow{:d}Col{:d}ToRow{:d}Col{:d}'.format(inlist[0][0],inlist[0][1],inlist[-1][0],inlist[-1][1]))
	self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] - self.cellValues[inlist[-1][0]][inlist[-1][1]] >= 4).OnlyEnforceIf(c)
	self.model.Add(self.cellValues[inlist[-1][0]][inlist[-1][1]] - self.cellValues[inlist[0][0]][inlist[0][1]] >= 4).OnlyEnforceIf(c.Not())
	
	for j in range(1,len(inlist)-1):
		# c picks whether cell is greater than both endpoints, or less
		c = self.model.NewBoolVar('LockoutMidRow{:d}Col{:d}FromRow{:d}Col{:d}ToRow{:d}Col{:d}'.format(inlist[j][0],inlist[j][1],inlist[0][0],inlist[0][1],inlist[-1][0],inlist[-1][1]))
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] > self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c)
		self.model.Add(self.cellValues[inlist[-1][0]][inlist[-1][1]] > self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c)
		self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] < self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c.Not())
		self.model.Add(self.cellValues[inlist[-1][0]][inlist[-1][1]] < self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(c.Not())
		
def setRegionSumLine(self,inlist):
	inlist = self._procCellList(inlist)
	sumSets = []
	for region in self.regions:
		tempSum = [self.cellValues[x[0]][x[1]] for x in set(region) & set(inlist)]
		if len(tempSum) != 0: sumSets.append(tempSum)

	baseSum = sum(x for x in sumSets[0])
	for i in range(1,len(sumSets)):
		self.model.Add(sum(x for x in sumSets[i]) == baseSum)
		
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
			sumSets.append([self.cellValues[x[0]][x[1]] for x in inlist[currentRegionStart:j]])
			currentRegionStart = j
			currentRegion = thisRegion
	# Need to do it again since the last segment is left in the queue.	
	sumSets.append([self.cellValues[x[0]][x[1]] for x in inlist[currentRegionStart:]])

	baseSum = sum(sumSets[0])
	for i in range(1,len(sumSets)):
		self.model.Add(sum(sumSets[i]) == baseSum)
		
def setRegionometer(self,inlist):
	# Region boundaries break the line into segments, and the sum on each segment must increase from one end to the other
	inlist = self._procCellList(inlist)
	
	# Code to create the segment sums is directly stolen from RegionSegmentSumLines
	sumSets = []
	currentRegionStart = 0
	for i in range(len(self.regions)):
		if len({inlist[0]} & set(self.regions[i])) > 0: currentRegion = i
	for j in range(1,len(inlist)):
		for i in range(len(self.regions)):
			if len({inlist[j]} & set(self.regions[i])) > 0: thisRegion = i
		if thisRegion != currentRegion:
			sumSets.append([self.cellValues[x[0]][x[1]] for x in inlist[currentRegionStart:j]])
			currentRegionStart = j
			currentRegion = thisRegion
	# Need to do it again since the last segment is left in the queue.	
	sumSets.append([self.cellValues[x[0]][x[1]] for x in inlist[currentRegionStart:]])

	bit = self.model.NewBoolVar('RegionmeterEnd')
	for i in range(0,len(sumSets)-1):
		self.model.Add(sum(sumSets[i]) < sum(sumSets[i+1])).OnlyEnforceIf(bit)
		self.model.Add(sum(sumSets[i]) > sum(sumSets[i+1])).OnlyEnforceIf(bit.Not())

def setDoublingLine(self,inlist):
	# Every digit that appears on a doubling line appears exactly twice
	inlist = self._procCellList(inlist)
	
	vars = [[None for j in range(len(inlist))] for i in range(len(inlist))]
	for i in range(len(inlist)):
		for j in range(i+1,len(inlist)):
			cB = self.model.NewBoolVar('DoublingLineBool')
			cI = self.model.NewIntVar(0,1,'DoublingLineIntCell{:d}{:d}'.format(i,j))
			self.model.Add(cI == 1).OnlyEnforceIf(cB)		# Ties the two variables together
			self.model.Add(cI == 0).OnlyEnforceIf(cB.Not())	# Int version needed to add
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] == self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(cB)
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] != self.cellValues[inlist[j][0]][inlist[j][1]]).OnlyEnforceIf(cB.Not())
			vars[i][j] = cI
			vars[j][i] = cI
	
	for i in range(len(inlist)):
		self.model.Add(sum(vars[i][j] for j in range(len(inlist)) if j != i) == 1)	#For each cell along line, exactly one cell has a matching value
		
def setShiftLine(self,inlist):
	# Like a palindrome, except one side of the line is uniformly one larger than its counterpart on the other side
	inlist = self._procCellList(inlist)
	c = self.model.NewBoolVar('ShiftLineR{:d}C{:d}'.format(inlist[0][0],inlist[0][1]))
	for j in range(len(inlist) // 2):
		self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] == self.cellValues[inlist[-j-1][0]][inlist[-j-1][1]] + 1).OnlyEnforceIf(c)
		self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + 1 == self.cellValues[inlist[-j-1][0]][inlist[-j-1][1]]).OnlyEnforceIf(c.Not())
		
def setUpAndDownLine(self,inlist):
	inlist = self._procCellList(inlist)
	c = self.model.NewBoolVar('UpAndDownLineR{:d}C{:d}'.format(inlist[0][0],inlist[0][1]))
	for i in range(len(inlist)-1):
		if i % 2 == 0:
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] > self.cellValues[inlist[i+1][0]][inlist[i+1][1]]).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < self.cellValues[inlist[i+1][0]][inlist[i+1][1]]).OnlyEnforceIf(c.Not())
		else:
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] < self.cellValues[inlist[i+1][0]][inlist[i+1][1]]).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] > self.cellValues[inlist[i+1][0]][inlist[i+1][1]]).OnlyEnforceIf(c.Not())

def setAverageLine(self,inlist):
	inlist = self._procCellList(inlist)
	self.model.Add((len(inlist)-1)*self.cellValues[inlist[0][0]][inlist[0][1]] == sum([self.cellValues[inlist[i][0]][inlist[i][1]] for i in range(1,len(inlist))]))
	
def setNabnerLine(self,inlist):
	# All cells on the line have a difference of at least 2, so we put each pair as its own line
	for i in range(len(inlist)):
		for j in range(i+1,len(inlist)):
			self.setMinWhispersLine([inlist[i],inlist[j]],2)
			
def setParityCountLine(self,inlist):
	if 'Parity' not in self._propertyInitialized:
		self._setParity()
	inlist = self._procCellList(inlist)
	c = self.model.NewBoolVar('ParityCountLine')
	e = self.model.NewBoolVar('ParityCountLine')	# Variable to test if endpoints are equal, in which case we prevent c from flapping.
	self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] + self.cellValues[inlist[-1][0]][inlist[-1][1]] == len(inlist))
	self.model.Add(sum(self.cellParity[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))) == self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf(c)
	self.model.Add(sum(self.cellParity[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))) == self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(c.Not())
	
	self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(e)
	self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] != self.cellValues[inlist[-1][0]][inlist[-1][1]]).OnlyEnforceIf(e.Not())
	self.model.AddBoolAnd(c).OnlyEnforceIf(e)
	
def set10Line(self,inlist,value=10):
	inlist = self._procCellList(inlist)
	if inlist[0] == inlist[-1]:
		# This is the cyclic case
		del inlist[-1] # Don't want the second iteration screwing up our sum
		cyclic = True
	else:
		cyclic = False
	
	myMaxDigit = max(self.digits)
	smSeg = value // myMaxDigit + (0 if value % myMaxDigit == 0 else 1)
	maxNumSeg = len(inlist) // smSeg + (0 if len(inlist) % smSeg == 0 else 1)
	segment = [self.model.NewIntVar(0,maxNumSeg,'10LineSegmentNumber') for j in range(len(inlist))]
	self.model.Add(segment[0] == 0)
	
	# Man, allowing cyclic 10 lines is a pain in the botox. Normally I'd just make all the variables and jam, but it's
	# so much model clutter in the line case. I think I'm just going to accept the clutter here.
	if cyclic:
		backInSeg0 = [self.model.NewBoolVar('10LineReturnToSegment0') for i in range(len(inlist))]
		self.model.AddBoolAnd(backInSeg0[0].Not()).OnlyEnforceIf(backInSeg0[0]) # Bury the first one
		for i in range(1,len(inlist)):
			self.model.AddBoolAnd([backInSeg0[j].Not() for j in range(len(inlist)) if j != i]).OnlyEnforceIf(backInSeg0[i])
			self.model.Add(segment[i] - segment[i-1] <= 1).OnlyEnforceIf(backInSeg0[i].Not())
			self.model.Add(segment[i] - segment[i-1] >= 0).OnlyEnforceIf(backInSeg0[i].Not())
			for j in range(i,len(inlist)):
				self.model.Add(segment[j] == 0).OnlyEnforceIf(backInSeg0[i])
	else:
		for i in range(1,len(inlist)):
			self.model.Add(segment[i] - segment[i-1] <= 1)
			self.model.Add(segment[i] - segment[i-1] >= 0)
	
	# Not needed in the pure line case, but in the cyclic case
	segMax = self.model.NewIntVar(0,maxNumSeg,'10LineMaxSegUsed')
	self.model.AddMaxEquality(segMax,segment)
	# This is not strictly needed, but I think it might actually help speed things up
	self.model.Add(sum(self.cellValues[inlist[i][0]][inlist[i][1]] for i in range(len(inlist))) == value*segMax+value)
	
	for j in range(maxNumSeg):
		# Decide if segment is used
		c = self.model.NewBoolVar('10LineSegmentUsed')
		self.model.Add(segMax >= j).OnlyEnforceIf(c)
		self.model.Add(segMax < j).OnlyEnforceIf(c.Not())
		segBool = [self.model.NewBoolVar('10LineSegmentTest{:d}'.format(j)) for k in range(len(inlist))]
		segInts = [self.model.NewIntVar(min(self.minDigit,0),myMaxDigit,'10LineSegmentSum{:d}'.format(j)) for k in range(len(inlist))]
		for i in range(len(inlist)):
			self.model.Add(segment[i] == j).OnlyEnforceIf(segBool[i])
			self.model.Add(segment[i] != j).OnlyEnforceIf(segBool[i].Not())
			self.model.Add(segInts[i] == self.cellValues[inlist[i][0]][inlist[i][1]]).OnlyEnforceIf(segBool[i])
			self.model.Add(segInts[i] == 0).OnlyEnforceIf(segBool[i].Not())
		
		self.model.Add(sum(segInts) == value).OnlyEnforceIf(c)
		self.model.Add(sum(segInts) == 0).OnlyEnforceIf(c.Not())
			
			
def setClockLine(self,inlist):
	inlist = self._procCellList(inlist)
	for i in range(len(inlist)-1):
		c = self.model.NewBoolVar('ClockLineDiff')
		g = self.model.NewBoolVar('ClockLineGT')
		self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] - self.cellValues[inlist[i+1][0]][inlist[i+1][1]] == 2).OnlyEnforceIf([c,g])
		self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]] - self.cellValues[inlist[i+1][0]][inlist[i+1][1]] == 7).OnlyEnforceIf([c.Not(),g])
		self.model.Add(self.cellValues[inlist[i+1][0]][inlist[i+1][1]] - self.cellValues[inlist[i][0]][inlist[i][1]] == 2).OnlyEnforceIf([c,g.Not()])
		self.model.Add(self.cellValues[inlist[i+1][0]][inlist[i+1][1]] - self.cellValues[inlist[i][0]][inlist[i][1]] == 7).OnlyEnforceIf([c.Not(),g.Not()])
		
def setMagicLine(self,inlist):
	inlist = self._procCellList(inlist)
	for i in range(len(inlist)-3):
		sum1 = sum(self.cellValues[inlist[i+j][0]][inlist[i+j][1]] for j in range(3))
		sum2 = sum(self.cellValues[inlist[i+j+1][0]][inlist[i+j+1][1]] for j in range(3))
		varBitmap = self._varBitmap('magicLine',3)
		self.model.Add(sum1 == 15).OnlyEnforceIf(varBitmap[0])
		self.model.Add(sum2 != 15).OnlyEnforceIf(varBitmap[0])
		self.model.Add(sum1 != 15).OnlyEnforceIf(varBitmap[1])
		self.model.Add(sum2 == 15).OnlyEnforceIf(varBitmap[1])
		self.model.Add(sum1 == 15).OnlyEnforceIf(varBitmap[2])
		self.model.Add(sum2 == 15).OnlyEnforceIf(varBitmap[2])
		
def setConsecutiveLine(self,inlist):
	self.setRenbanLine(inlist)
	self.setMissingThermo(inlist)
	
def setZipperLine(self,inlist):
	inlist = self._procCellList(inlist)
	l = len(inlist)
	if l % 2 == 0:
		target = self.cellValues[inlist[(l//2) - 1][0]][inlist[(l//2) - 1][1]] + self.cellValues[inlist[l // 2][0]][inlist[l // 2][1]]
		test = (l-2) // 2
	else:
		target = self.cellValues[inlist[(l-1) // 2][0]][inlist[(l-1) // 2][1]]
		test = (l-1) // 2
	for i in range(test):
		self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]]+self.cellValues[inlist[l-1-i][0]][inlist[l-1-i][1]] == target)

def setLineSumLine(self,inlist):
	inlist = self._procCellList(inlist)
	mySum = sum([self.cellValues[x[0]][x[1]] for x in inlist])
	vars = [self.model.NewBoolVar('') for i in range(len(inlist))]
	for i in range(len(inlist)):
		self.model.Add(mySum == 2*self.cellValues[inlist[i][0]][inlist[i][1]]).OnlyEnforceIf(vars[i])
	self.model.AddBoolOr(vars)
	
def setUniquePairsLines(self,listOfLists):
	allPairMarkers = []
	for inlist in listOfLists:
		inlist = self._procCellList(inlist)
		self.model.AddAllDifferent([self.cellValues[inlist[j][0]][inlist[j][1]] for j in range(len(inlist))])
		for x in range(len(inlist)):
			for y in range(x+1,len(inlist)):
				marker1 = self.model.NewIntVar(self.minDigit*(self.digitRange+1)+self.minDigit,self.maxDigit*(self.digitRange+1)+self.maxDigit,"variableName")
				self.model.Add(marker1 == self.cellValues[inlist[x][0]][inlist[x][1]]*(self.digitRange+1)+self.cellValues[inlist[y][0]][inlist[y][1]])
				allPairMarkers.append(marker1)
				marker2 = self.model.NewIntVar(self.minDigit*(self.digitRange+1)+self.minDigit,self.maxDigit*(self.digitRange+1)+self.maxDigit,"variableName")
				self.model.Add(marker2 == self.cellValues[inlist[y][0]][inlist[y][1]]*(self.digitRange+1)+self.cellValues[inlist[x][0]][inlist[x][1]])
				allPairMarkers.append(marker2)
	self.model.AddAllDifferent(allPairMarkers)
	
def setCellIndexLines(self,listOfLists):
	endBools = []
	for thislist in listOfLists:
		inlist = self._procCellList(thislist)
		rowBitmap = self._varBitmap('CellLine',self.boardWidth)
		colBitmap = self._varBitmap('CellLine',self.boardWidth)
		endBool = self.model.NewBoolVar('CellLine')
		endBools.append(endBool)
		for j in range(self.boardWidth):
			self.model.Add(self.cellValues[inlist[1][0]][inlist[1][1]] == j+1).OnlyEnforceIf(colBitmap[j])
			for i in range(self.boardWidth):
				self.model.Add(self.cellValues[inlist[0][0]][inlist[0][1]] == i+1).OnlyEnforceIf(rowBitmap[i]+[endBool])
				self.model.Add(self.cellValues[inlist[2][0]][inlist[2][1]] == i+1).OnlyEnforceIf(rowBitmap[i]+[endBool.Not()])
				self.model.Add(self.cellValues[i][j] == self.cellValues[inlist[2][0]][inlist[2][1]]).OnlyEnforceIf(rowBitmap[i]+colBitmap[j]+[endBool])
				self.model.Add(self.cellValues[i][j] == self.cellValues[inlist[0][0]][inlist[0][1]]).OnlyEnforceIf(rowBitmap[i]+colBitmap[j]+[endBool.Not()])

	for i in range(len(listOfLists)):
		iInlist = self._procCellList(listOfLists[i])
		for j in range(i+1,len(listOfLists)):
			jInlist = self._procCellList(listOfLists[j])
			self.model.Add(self.cellValues[iInlist[1][0]][iInlist[1][1]] != self.cellValues[jInlist[1][0]][jInlist[1][1]])
			self.model.Add(self.cellValues[iInlist[0][0]][iInlist[0][1]] != self.cellValues[jInlist[0][0]][jInlist[0][1]]).OnlyEnforceIf([endBools[i],endBools[j]])
			self.model.Add(self.cellValues[iInlist[2][0]][iInlist[2][1]] != self.cellValues[jInlist[2][0]][jInlist[2][1]]).OnlyEnforceIf([endBools[i],endBools[j]])
			self.model.Add(self.cellValues[iInlist[2][0]][iInlist[2][1]] != self.cellValues[jInlist[0][0]][jInlist[0][1]]).OnlyEnforceIf([endBools[i].Not(),endBools[j]])
			self.model.Add(self.cellValues[iInlist[0][0]][iInlist[0][1]] != self.cellValues[jInlist[2][0]][jInlist[2][1]]).OnlyEnforceIf([endBools[i].Not(),endBools[j]])
			self.model.Add(self.cellValues[iInlist[2][0]][iInlist[2][1]] != self.cellValues[jInlist[2][0]][jInlist[2][1]]).OnlyEnforceIf([endBools[i].Not(),endBools[j].Not()])
			self.model.Add(self.cellValues[iInlist[0][0]][iInlist[0][1]] != self.cellValues[jInlist[0][0]][jInlist[0][1]]).OnlyEnforceIf([endBools[i].Not(),endBools[j].Not()])
			self.model.Add(self.cellValues[iInlist[2][0]][iInlist[2][1]] != self.cellValues[jInlist[0][0]][jInlist[0][1]]).OnlyEnforceIf([endBools[i],endBools[j].Not()])
			self.model.Add(self.cellValues[iInlist[0][0]][iInlist[0][1]] != self.cellValues[jInlist[2][0]][jInlist[2][1]]).OnlyEnforceIf([endBools[i],endBools[j].Not()])

def setSplitPeaLine(self,inlist):
	inlist = self._procCellList(inlist)
	endSame = self.model.NewBoolVar('SplitPeaLine')
	firstTens = self.model.NewBoolVar('SplitPeaLine')
	firstEnd = self.cellValues[inlist[0][0]][inlist[0][1]]
	lastEnd = self.cellValues[inlist[len(inlist)-1][0]][inlist[len(inlist)-1][1]]
	lineSum = sum(self.cellValues[inlist[i][0]][inlist[i][1]] for i in range(1,len(inlist)-1))
	
	self.model.Add(firstEnd == lastEnd).OnlyEnforceIf(endSame)
	self.model.Add(lineSum == 10*firstEnd+lastEnd).OnlyEnforceIf(endSame)
	self.model.AddBoolAnd(firstTens).OnlyEnforceIf(endSame) # Force other bool to be true...not needed in this case
	
	self.model.Add(firstEnd != lastEnd).OnlyEnforceIf(endSame.Not())
	self.model.Add(lineSum == 10*firstEnd+lastEnd).OnlyEnforceIf([endSame.Not(),firstTens])
	self.model.Add(lineSum == firstEnd+10*lastEnd).OnlyEnforceIf([endSame.Not(),firstTens.Not()])
	
def setSequenceLine(self,inlist):
	inlist = self._procCellList(inlist)
	for i in range(1,len(inlist)):
		self.model.Add(self.cellValues[inlist[i][0]][inlist[i][1]]-self.cellValues[inlist[i-1][0]][inlist[i-1][1]] == self.cellValues[inlist[1][0]][inlist[1][1]]-self.cellValues[inlist[0][0]][inlist[0][1]])

def setIndexLine(self,inlist):
	inlist = self._procCellList(inlist)
	myVars = [self.model.NewIntVar(0,self.maxDigit-self.minDigit,'indexLineVars') for i in range(len(inlist))]
	for i in range(len(inlist)):
		self.model.Add(myVars[i] == self.cellValues[inlist[i][0]][inlist[i][1]] - self.minDigit)
	self.model.AddInverse(myVars,myVars)
	
def setLotLine(self,inlist,lotIndex,prop):
	inlist = self._procCellList(inlist)
	match prop:
		case 'ParityChange' | 'EntropyChange' | 'ModularChange' | 'PrimalityChange':
			countBools = self._selectCellsOnLine(inlist,[(prop,'before')])
		case 'MatchParity' | 'MatchEntropy' | 'MatchModular' | 'MatchPrimality':
			countBools = self._selectCellsOnLine(inlist,[(prop,lotIndex)])
		case 'UniqueDigits':
			countBools = self._selectCellsOnLine(inlist,[('DigitInstance','First')])
		case 'Even' | 'Odd':
			countBools = self._selectCellsOnLine(inlist,[('Parity',self.EQ,getattr(self,prop))])
		case 'Low' | 'Middle' | 'High':
			countBools = self._selectCellsOnLine(inlist,[('Entropy',self.EQ,getattr(self,prop))])
		case 'Mod0' | 'Mod1' | 'Mod2':
			countBools = self._selectCellsOnLine(inlist,[('Modular',self.EQ,int(prop[-1]))])

			
	countInts = [self.model.NewIntVar(0,1,'lotCellCount') for j in range(len(countBools))]
	for i in range(len(countBools)):
		self.model.Add(countInts[i] == 1).OnlyEnforceIf(countBools[i])
		self.model.Add(countInts[i] == 0).OnlyEnforceIf(countBools[i].Not())
	self.model.Add(self.cellValues[inlist[lotIndex-1][0]][inlist[lotIndex-1][1]] == sum(countInts))

def setConditionalSumLine(self,inlist,value,selectSummands=None,selectTerminator=None,terminateOnFirst=True,includeTerminator=True):
	# Copied from setHangingSum, an external clue. Just a line version, should be straightforward since the underlying support
	# functions were converted to lines.
	L = self._procCellList(inlist)
	
	# Need for cell transform clues. self.minDigit is the smallest base digit, not necessarily as transformed.
	myMin = min(self.digits)
	myMax = max(self.digits)
	
	partialSum = [self.model.NewIntVar(min(0,self.boardWidth*myMin),self.boardWidth*myMax,'HangingSumPartialSum{:d}'.format(i)) for i in range(len(L))]
		
	selectionCells = self._selectCellsOnLine(L,selectSummands)
	
	# Tie the variables together
	self.model.Add(partialSum[0] == self.cellValues[L[0][0]][L[0][1]]).OnlyEnforceIf(selectionCells[0])
	self.model.Add(partialSum[0] == 0).OnlyEnforceIf(selectionCells[0].Not())
	for i in range(1,len(L)):
		self.model.Add(partialSum[i] == partialSum[i-1] + self.cellValues[L[i][0]][L[i][1]]).OnlyEnforceIf(selectionCells[i])
		self.model.Add(partialSum[i] == partialSum[i-1]).OnlyEnforceIf(selectionCells[i].Not())
	
	# Now create terminator conditions
	terminatorCells = self._terminateCellsOnLine(L,selectTerminator)
	
	self._evaluateHangingClues(partialSum,terminatorCells,value,terminateOnFirst,includeTerminator)
	
def setConditionalCountLine(self,inlist,value,selectSummands=None,selectTerminator=None,terminateOnFirst=True,includeTerminator=True):
	# Copied from setConditionalSumLine, for counts instead of sums
	
	L = self._procCellList(inlist)
	partialCount = [self.model.NewIntVar(0,len(L),'ConditionalCountPartialCounts{:d}'.format(i)) for i in range(len(L))]
		
	selectionCells = self._selectCellsOnLine(L,selectSummands)
	
	# Tie the variables together
	self.model.Add(partialCount[0] == 1).OnlyEnforceIf(selectionCells[0])
	self.model.Add(partialCount[0] == 0).OnlyEnforceIf(selectionCells[0].Not())
	for i in range(1,len(L)):
		self.model.Add(partialCount[i] == partialCount[i-1] + 1).OnlyEnforceIf(selectionCells[i])
		self.model.Add(partialCount[i] == partialCount[i-1]).OnlyEnforceIf(selectionCells[i].Not())
	
	# Now create terminator conditions
	terminatorCells = self._terminateCellsOnLine(L,selectTerminator)
	
	self._evaluateHangingClues(partialCount,terminatorCells,value,terminateOnFirst,includeTerminator)
	
def setConditionalInstanceLine(self,inlist,values,selectSummands=None,selectTerminator=None,terminateOnFirst=True,includeTerminator=True,negativeConstraint=False):
	L = self._procCellList(inlist)
	myDigits = list(self.digits)
	
	selectionCells = self._selectCellsOnLine(L,selectSummands)
	
	digitMatch = [[self.model.NewBoolVar('MatchForDigit{:d}Cell{:d}'.format(myDigits[d],j)) for j in range(len(L))] for d in range(len(myDigits))]
	matchToHere = [[self.model.NewBoolVar('MatchToHere{:d}Cell{:d}'.format(myDigits[d],j)) for j in range(len(L))] for d in range(len(myDigits))]
	matchToHereInt = [[self.model.NewIntVar(0,1,'MatchToHere{:d}Cell{:d}'.format(myDigits[d],j)) for j in range(len(L))] for d in range(len(myDigits))]
	partialMatch = [self.model.NewIntVar(0,len(L),'PartialMatchCounts') for j in range(len(L))]
	
	for j in range(len(L)):
		for d in range(len(myDigits)):
			self.model.Add(self.cellValues[L[j][0]][L[j][1]] == myDigits[d]).OnlyEnforceIf([digitMatch[d][j],selectionCells[j]])
			self.model.Add(self.cellValues[L[j][0]][L[j][1]] != myDigits[d]).OnlyEnforceIf([digitMatch[d][j].Not(),selectionCells[j]])
			self.model.AddBoolAnd(digitMatch[d][j].Not()).OnlyEnforceIf(selectionCells[j].Not())
			self.model.AddBoolOr([digitMatch[d][k] for k in range(j+1)]).OnlyEnforceIf(matchToHere[d][j])
			self.model.AddBoolAnd([digitMatch[d][k].Not() for k in range(j+1)]).OnlyEnforceIf(matchToHere[d][j].Not())
			self.model.Add(matchToHereInt[d][j] == 1).OnlyEnforceIf(matchToHere[d][j])
			self.model.Add(matchToHereInt[d][j] == 0).OnlyEnforceIf(matchToHere[d][j].Not())
		self.model.Add(partialMatch[j] == sum([matchToHereInt[d][j] for d in range(len(myDigits)) if myDigits[d] in values]))
	
	# Now create terminator conditions
	terminatorCells = self._terminateCellsOnLine(L,selectTerminator)
	
	self._evaluateHangingClues(partialMatch,terminatorCells,len(values),terminateOnFirst,includeTerminator)
	
	if negativeConstraint == True:
		for j in range(len(L)):
			if includeTerminator is True:
				self.model.Add(sum([matchToHereInt[d][j] for d in range(len(myDigits)) if myDigits[d] not in values]) == 0).OnlyEnforceIf(terminatorCells[j])
			else:
				self.model.Add(sum([matchToHereInt[d][j-1] for d in range(len(myDigits)) if myDigits[d] not in values]) == 0).OnlyEnforceIf(terminatorCells[j])
			
	