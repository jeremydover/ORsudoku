from ORsudoku.combinationIterator import CombinationIterator

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

def setThermo(self,inlist,slow=False,missing=False,speed=False):
	inlist = self._procCellList(inlist)
	if missing is False:
		for j in range(len(inlist)-1):
			if slow is True or speed == 'slow':
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] <= self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			elif slow is False and speed == 'fast':
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + 1 < self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			elif slow is False and isinstance(speed, int):
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + speed < self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
			else:
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]])
	else:
		c = self.model.NewBoolVar('MissingThermo')
		for j in range(len(inlist)-1):
			if slow is True or speed == 'slow':
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] <= self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(c)
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] >= self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(c.Not())
			elif slow is False and speed == 'fast':
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + 1 < self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(c)
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.cellValues[inlist[j+1][0]][inlist[j+1][1]] + 1).OnlyEnforceIf(c.Not())
			elif slow is False and isinstance(speed, int):
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] + speed < self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(c)
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.cellValues[inlist[j+1][0]][inlist[j+1][1]] + speed).OnlyEnforceIf(c.Not())
			else:
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] < self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(c)
				self.model.Add(self.cellValues[inlist[j][0]][inlist[j][1]] > self.cellValues[inlist[j+1][0]][inlist[j+1][1]]).OnlyEnforceIf(c.Not())
		
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
	
def setvariableLengthThermo(self,bulb,nextCell,slow=False,reflective=False):
	b = self.procCell(bulb)
	n = self.procCell(nextCell)
				
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
	varBitmap = self._varBitmap('10Line',2**(len(inlist)-1))
	varTrack = 0
	for i in range(len(inlist)):
		cI = CombinationIterator(len(inlist)-2,i)
		comb = cI.getNext()
		while comb is not None:
			ind = [-1] + comb + [len(inlist)-1]
			for j in range(len(ind)-1):
				self.model.Add(sum(self.cellValues[inlist[k][0]][inlist[k][1]] for k in range(ind[j]+1,ind[j+1]+1)) == value).OnlyEnforceIf(varBitmap[varTrack])
			comb = cI.getNext()
			varTrack = varTrack + 1
			
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
