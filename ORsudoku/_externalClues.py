def setLittleKiller(self,row1,col1,row2,col2,value):
	# row1,col1 is the position of the first cell in the sum
	# row2,col2 is the position of the second cell in the sum
	
	# Note: leave cell specs 1-based, since the call to setRepeatingCage will 0-base them
	hStep = col2 - col1
	vStep = row2 - row1
	cells = [(row1+vStep*k,col1+hStep*k) for k in range(self.boardWidth) if row1+vStep*k-1 in range(self.boardWidth) and col1+hStep*k-1 in range(self.boardWidth)]
	self.setRepeatingCage(cells,value)
	
def setXSumBase(self,row1,col1,rc,value,pm):
	#row,col are the coordinates of the cell containing the length, value is the sum
	#rc: 0 -> if adding in row, 1 -> if adding in column. Needed for corner cells.
	#pm: determines if these are normal X-sums (including the digit) or reverse X-Sums (sum on the other side)
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	sumRow = row if rc == self.Row or pm == 1 else self.boardWidth-1-row
	sumCol = col if rc == self.Col or pm == 1 else self.boardWidth-1-col
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	hStep = pm * hStep	# Change direction in case we're doing reverse
	vStep = pm * vStep
	
	digits = list(self.digits)
	varBitmap = self._varBitmap('XSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(digits))
		
	for i in range(len(digits)):
		if digits[i] == 0:
			# In this case we have to have a null sum, which must be 0.
			if value == 0:
				self.model.Add(self.cellValues[sumRow][sumCol] == 0).OnlyEnforceIf(varBitmap[i])
			else:
				self.model.AddBoolAnd([varBitmap[i][0].Not()]).OnlyEnforceIf(varBitmap[i])		
				# If value is not 0, then 0 is not a valid digit and this case cannot occur, but there's no arithmetic way to express this	
		elif abs(digits[i]) > self.boardWidth:
			# Digit is too big to have a reasonable sum, so disallow
			self.model.AddBoolAnd([varBitmap[i][0].Not()]).OnlyEnforceIf(varBitmap[i])	
		elif digits[i] > 0:
			self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])
			self.model.Add(sum(self.cellValues[sumRow+j*vStep][sumCol+j*hStep] for j in range(digits[i])) == value).OnlyEnforceIf(varBitmap[i])
		else: # So if a digit is negative, we reverse the intended direction
			mySumRow = self.boardWidth-1-sumRow if rc == self.Col else sumRow
			mySumCol = self.boardWidth-1-sumCol if rc == self.Row else sumCol
			myHStep = -1 * hStep
			myVStep = -1 * vStep				
			self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])
			self.model.Add(sum(self.cellValues[mySumRow+j*myVStep][mySumCol+j*myHStep] for j in range(-1*digits[i])) == value).OnlyEnforceIf(varBitmap[i])
			
def setXSum(self,row1,col1,rc,value):
	self.setXSumBase(row1,col1,rc,value,1)
	
def setReverseXSum(self,row1,col1,rc,value):
	self.setXSumBase(row1,col1,rc,value,-1)
			
def setDoubleXSum(self,row1,col1,rc,value):
	# A double X sum clue gives the sum of the X sums from each direction (top/bottom or left/right) in the clued row or column.
	row = row1 - 1 if rc == self.Row else 0
	col = col1 - 1 if rc == self.Col else 0
	hStep = 0 if rc == self.Col else 1
	vStep = 0 if rc == self.Row else 1
	
	digits = [x for x in self.digits if abs(x) <= self.boardWidth]
	varBitmap = self._varBitmap('doubleXSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(digits)*len(digits))
		
	varTrack = 0
	for i in range(len(digits)):
		myRow = self.boardWidth-1 if rc == self.Col and digits[i] < 0 else row
		myCol = self.boardWidth-1 if rc == self.Row and digits[i] < 0 else col
		myVStep = vStep if digits[i] > 0 else -1 * vStep
		myHStep = hStep if digits[i] > 0 else -1 * hStep
		sumIVars = [self.cellValues[myRow+k*myVStep][myCol+k*myHStep] for k in range(abs(digits[i]))]
		for j in range(len(digits)):
			otherRow = self.boardWidth-1 if rc == self.Col else row
			otherCol = self.boardWidth-1 if rc == self.Row else col
			self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[varTrack])
			self.model.Add(self.cellValues[otherRow][otherCol] == digits[j]).OnlyEnforceIf(varBitmap[varTrack])
			myRow = 0 if rc == self.Col and digits[j] < 0 else otherRow
			myCol = 0 if rc == self.Row and digits[j] < 0 else otherCol
			myVStep = -1*vStep if digits[j] > 0 else vStep
			myHStep = -1*hStep if digits[j] > 0 else hStep
			sumJVars = [self.cellValues[myRow+k*myVStep][myCol+k*myHStep] for k in range(abs(digits[j]))]
			
			myVars = sumIVars + sumJVars
			if len(myVars) == 0:
				# In this case both digits are zero, could happen in a weird 0-8, double or nothing scenario
				if value == 0: # This is always true
					self.model.AddBoolAnd([varBitmap[varTrack][0]]).OnlyEnforceIf(varBitmap[varTrack])
				else: # This is never true
					self.model.AddBoolAnd([varBitmap[varTrack][0].Not()]).OnlyEnforceIf(varBitmap[varTrack])
			else:
				self.model.Add(sum(myVars) == value).OnlyEnforceIf(varBitmap[varTrack])
			varTrack = varTrack + 1

def setXAverageBase(self,row1,col1,rc,value,pm):
	#row,col are the coordinates of the cell containing the length, value is the sum
	#rc: 0 -> if adding in row, 1 -> if adding in column. Needed for corner cells.
	#pm: determines if these are normal X-averages (including the digit) or reverse X-Averages (sum on the other side)
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	sumRow = row if rc == self.Row or pm == 1 else self.boardWidth-1-row
	sumCol = col if rc == self.Col or pm == 1 else self.boardWidth-1-col
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	hStep = pm * hStep	# Change direction in case we're doing reverse
	vStep = pm * vStep
	
	digits = list(self.digits)
	varBitmap = self._varBitmap('XSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(digits))
		
	for i in range(len(digits)):
		if digits[i] == 0:
			# In this case we have to have a null sum, which must be 0.
			if value == 0:
				self.model.Add(self.cellValues[sumRow][sumCol] == 0).OnlyEnforceIf(varBitmap[i])
			else:
				self.model.AddBoolAnd([varBitmap[i][0].Not()]).OnlyEnforceIf(varBitmap[i])		
				# If value is not 0, then 0 is not a valid digit and this case cannot occur, but there's no arithmetic way to express this	
		elif abs(digits[i]) > self.boardWidth:
			# Digit is too big to have a reasonable sum, so disallow
			self.model.AddBoolAnd([varBitmap[i][0].Not()]).OnlyEnforceIf(varBitmap[i])	
		elif digits[i] > 0:
			self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])
			self.model.Add(sum(self.cellValues[sumRow+j*vStep][sumCol+j*hStep] for j in range(digits[i])) == value*digits[i]).OnlyEnforceIf(varBitmap[i])
		else: # So if a digit is negative, we reverse the intended direction
			mySumRow = self.boardWidth-1-sumRow if rc == self.Col else sumRow
			mySumCol = self.boardWidth-1-sumCol if rc == self.Row else sumCol
			myHStep = -1 * hStep
			myVStep = -1 * vStep				
			self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])
			self.model.Add(sum(self.cellValues[mySumRow+j*myVStep][mySumCol+j*myHStep] for j in range(-1*digits[i])) == value*digits[i]).OnlyEnforceIf(varBitmap[i])

def setXAverage(self,row1,col1,rc,value):
	self.setXAverageBase(row1,col1,rc,value,1)
	
def setReverseXAverage(self,row1,col1,rc,value):
	self.setXAverageBase(row1,col1,rc,value,-1)

def setXKropki(self,row1,col1,rc,wb,neg=False):
	# row,col are the coordinates of the cell containing the Kropki position, so no 9s allowed
	# rc is whether the cell is poiting to the row or column 0->row, 1->column
	# wb whether kropki is white or black, 0->white,1->black
	# neg: True if Kropki implies no other Kropkis can occur in row/col
		
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)		
	
	allowableDigits = [x for x in self.digits if x >= 1 and x <=self.boardWidth-1]
	varBitmap = self._varBitmap('XKropkiPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits))
	lgr = self.model.NewBoolVar('XKropkiLargerRow{:d}Col{:d}RC{:d}'.format(row,col,rc))
	
	for i in range(len(allowableDigits)):
		self.model.Add(self.cellValues[row][col] == allowableDigits[i]).OnlyEnforceIf(varBitmap[i])
		for j in range(self.boardWidth-1):
			firstCell = self.cellValues[row+j*vStep][col+j*hStep]
			secondCell = self.cellValues[row+(j+1)*vStep][col+(j+1)*hStep]				
			if j == allowableDigits[i]-1:
				# First case: difference 1
				if wb == self.White:
					self.model.Add(firstCell - secondCell == 1).OnlyEnforceIf(varBitmap[i] + [lgr])
					self.model.Add(secondCell - firstCell == 1).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
				# Ratio 2
				else:
					self.model.Add(firstCell - 2*secondCell == 0).OnlyEnforceIf(varBitmap[i] + [lgr])
					self.model.Add(secondCell - 2*firstCell == 0).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
			else:
				# Nothing forced...unless negative constraint
				if neg is True:
					if wb == self.White:
						self.model.Add(firstCell - secondCell != 1).OnlyEnforceIf(varBitmap[i] + [lgr])
						self.model.Add(secondCell - firstCell != 1).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
					else:
						self.model.Add(firstCell - 2*secondCell != 0).OnlyEnforceIf(varBitmap[i] + [lgr])
						self.model.Add(secondCell - 2*firstCell != 0).OnlyEnforceIf(varBitmap[i] + [lgr.Not()])
						
def setNumberedRoomBase(self,row1,col1,rc,value,pm):
	# row,col are the coordinates of the cell containing the index of the target cell
	# rc is whether things are row/column
	# value is the target value to place
	# pm: determines if these are normal numbered rooms or reverse (count from the opposite side)
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	posRow = row if rc == self.Row or pm == 1 else self.boardWidth-1-row
	posCol = col if rc == self.Col or pm == 1 else self.boardWidth-1-col
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	hStep = pm * hStep	# Change direction in case we're doing reverse
	vStep = pm * vStep
	
	digits = list(self.digits)
	varBitmap = self._varBitmap('NumRoomPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(digits))
	
	for i in range(len(digits)):
		if digits[i] == 0 or abs(digits[i]) > self.boardWidth:	# No place to put digit...bury these cases
			self.model.AddBoolAnd([varBitmap[i][0].Not()]).OnlyEnforceIf(varBitmap[i])
		elif digits[i] > 0:
			self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])
			self.model.Add(self.cellValues[posRow+(digits[i]-1)*vStep][posCol+(digits[i]-1)*hStep] == value).OnlyEnforceIf(varBitmap[i])
		else: # So if a digit is negative, we reverse the intended direction
			myPosRow = self.boardWidth-1-posRow if rc == self.Col else posRow
			myPosCol = self.boardWidth-1-posCol if rc == self.Row else posCol
			myHStep = -1 * hStep
			myVStep = -1 * vStep				
			self.model.Add(self.cellValues[row][col] == digits[i]).OnlyEnforceIf(varBitmap[i])
			self.model.Add(self.cellValues[myPosRow+(-1*digits[i]-1)*myVStep][myPosCol+(-1*digits[i]-1)*myHStep] == value).OnlyEnforceIf(varBitmap[i])
	
def setNumberedRoom(self,row1,col1,rc,value):
	self.setNumberedRoomBase(row1,col1,rc,value,1)
	
def setReverseNumberedRoom(self,row1,col1,rc,value):
	self.setNumberedRoomBase(row1,col1,rc,value,-1)

def setSandwichSum(self,row1,col1,rc,value,digits=[]):
	# row,col are the coordinates of the cell containing the index of the target cell
	# rc is whether things are row/column
	# value is the sum of values between two given digits (highest and lowest by default)
	# digits the two digits in the digit set to bound the sandwich sums
	
	# If digits is null, set it to highest and lowest
	if len(digits) == 0:
		digits = [self.minDigit,self.maxDigit]
		
	# Convert from 1-base to 0-base: note, we allow clues on the bottom/right ends now too
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	varBitmap = self._varBitmap('SandwichPositionsRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth*(self.boardWidth-1))
	
	# We loop over all possible positions for the sandwich digits
	varTrack = 0
	for i in range(self.boardWidth):
		for j in range(self.boardWidth):
			if i == j:
				continue
			else:
				self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == digits[0]).OnlyEnforceIf(varBitmap[varTrack])
				self.model.Add(self.cellValues[row+j*vStep][col+j*hStep] == digits[1]).OnlyEnforceIf(varBitmap[varTrack])

			if i > j:
				myMax = i
				myMin = j
			else:
				myMax = j
				myMin = i

			if (myMax - myMin) == 1:
				# This is an adjacent case
				if value == 0:
					pass # There is no additional constraint to put here
				else:
					self.model.AddBoolAnd(varBitmap[varTrack][0].Not()).OnlyEnforceIf(varBitmap[varTrack])
			else:
				self.model.Add(sum(self.cellValues[row+k*vStep][col+k*hStep] for k in range(myMin+1,myMax)) == value).OnlyEnforceIf(varBitmap[varTrack])
				
			varTrack = varTrack + 1

def setOpenfacedSandwichSum(self,row1,col1,rc,value,digit=9):
	# Also known as before 9, like a sandwich sum, but clue is the sum of all digits prior to the stopper digit, usually 9.
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	varBitmap = self._varBitmap('OFSandwichPosRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
	
	for i in range(self.boardWidth):
		self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == digit).OnlyEnforceIf(varBitmap[i])
		if i == 0:
			if value != 0:
				self.model.AddBoolAnd([varBitmap[i][0].Not()]).OnlyEnforceIf(varBitmap[i])	# Bury it, cannot be this case.
		else:
			self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(i)) == value).OnlyEnforceIf(varBitmap[i])

def setShortSandwichSum(self,row1,col1,rc,value,depth=6):
	# row,col are the coordinates of the cell containing the index of the target cell
	# rc is whether things are row/column
	# value is the sum of values between the smallest and largest values in the first <depth> cells from the clue
	# depth defaults to 6 but can be set to any value greater than 2. Well, it could be 2 as well, but that'd be pretty dumb.
	
	# Convert from 1-base to 0-base: note, we allow clues on the bottom/right ends now too
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	varBitmap = self._varBitmap('SandwichPositionsRow{:d}Col{:d}RC{:d}'.format(row,col,rc),depth*(depth-1))
	
	# We loop over all possible positions for the sandwich digits
	varTrack = 0
	for i in range(depth):
		for j in range(depth):
			if i == j:
				continue
			else:
				for k in range(depth):
					if k != i:
						self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] > self.cellValues[row+k*vStep][col+k*hStep]).OnlyEnforceIf(varBitmap[varTrack])
					if k != j:
						self.model.Add(self.cellValues[row+j*vStep][col+j*hStep] < self.cellValues[row+k*vStep][col+k*hStep]).OnlyEnforceIf(varBitmap[varTrack])

			if i > j:
				myMax = i
				myMin = j
			else:
				myMax = j
				myMin = i

			if (myMax - myMin) == 1:
				# This is an adjacent case
				if value == 0:
					pass # There is no additional constraint to put here
				else:
					self.model.AddBoolAnd(varBitmap[varTrack][0].Not()).OnlyEnforceIf(varBitmap[varTrack])
			else:
				self.model.Add(sum(self.cellValues[row+k*vStep][col+k*hStep] for k in range(myMin+1,myMax)) == value).OnlyEnforceIf(varBitmap[varTrack])
				
			varTrack = varTrack + 1
			
def setBeforeNine(self,row1,col1,rc,value):
	self.setOpenfacedSandwichSum(row1,col1,rc,value,digit=9)

def setBattlefield(self,row1,col1,rc,value):
	# row,col are the coordinates of the cell next to the clue
	# rc is whether things are row/column
	# value is the sum of uncovered, or double covered, cells in the row, where the first cell on either side indicates the 
	# number of cells covered from each direction
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else 1
	vStep = 0 if rc == self.Row else 1
	rFirst = row if rc == self.Row else 0
	cFirst = col if rc == self.Col else 0
	rLast = row if rc == self.Row else self.boardWidth-1
	cLast = col if rc == self.Col else self.boardWidth-1
	
	if value == 0:
		self.model.Add(self.cellValues[rFirst][cFirst] + self.cellValues[rLast][cLast] == self.boardWidth)
	else:
		allowableDigits = [x for x in self.digits if x >= 1 and x <=self.boardWidth]
		varBitmap = self._varBitmap('BattlefieldRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits)*(len(allowableDigits)-1))
		
		varTrack = 0
		for i in range(len(allowableDigits)):
			for j in range(len(allowableDigits)):
				if i == j: continue
				self.model.Add(self.cellValues[rFirst][cFirst] == allowableDigits[i]).OnlyEnforceIf(varBitmap[varTrack])
				self.model.Add(self.cellValues[rLast][cLast] == allowableDigits[j]).OnlyEnforceIf(varBitmap[varTrack])
				if (allowableDigits[i]+allowableDigits[j]) < self.boardWidth:
					# Add up gap between
					self.model.Add(sum(self.cellValues[rFirst+k*vStep][cFirst+k*hStep] for k in range(allowableDigits[i],self.boardWidth - allowableDigits[j])) == value).OnlyEnforceIf(varBitmap[varTrack])
				elif (allowableDigits[i]+allowableDigits[j]) == self.boardWidth:
					if value != 0: # Nothing in the middle, so cannot work if value !=0. If value = 0, no further constraints.
						self.model.AddBoolAnd([varBitmap[varTrack][0],varBitmap[varTrack][0].Not()]).OnlyEnforceIf(varBitmap[varTrack])
				else:
					self.model.Add(sum(self.cellValues[rFirst+k*vStep][cFirst+k*hStep] for k in range(self.boardWidth - allowableDigits[j],allowableDigits[i])) == value).OnlyEnforceIf(varBitmap[varTrack])
				varTrack = varTrack + 1
			
def setPositionSum(self,row1,col1,rc,positionSum=None,valueSum=None):
	# row,col are the coordinates of the cell next to the clues
	# rc is whether things are row/column
	# positionSum is the sum of the first two cells in the row/column
	# valueSum is the sum of the cells which the first two cells index
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	allowableDigits = [x for x in self.digits if x >= 1 and x <=self.boardWidth]
	varBitmap = self._varBitmap('PositionSumRow{:d}Col{:d}RC{:d}'.format(row,col,rc),len(allowableDigits)*(len(allowableDigits)-1))
	
	varTrack = 0
	for i in range(len(allowableDigits)):
		for j in range(len(allowableDigits)):
			if i == j: continue
			self.model.Add(self.cellValues[row][col] == allowableDigits[i]).OnlyEnforceIf(varBitmap[varTrack])
			self.model.Add(self.cellValues[row+vStep][col+hStep] == allowableDigits[j]).OnlyEnforceIf(varBitmap[varTrack])
			if positionSum is not None:
				self.model.Add(self.cellValues[row][col] + self.cellValues[row+vStep][col+hStep] == positionSum).OnlyEnforceIf(varBitmap[varTrack])
			if valueSum is not None:
				self.model.Add(self.cellValues[row+(allowableDigits[i]-1)*vStep][col+(allowableDigits[i]-1)*hStep] + self.cellValues[row+(allowableDigits[j]-1)*vStep][col+(allowableDigits[j]-1)*hStep] == valueSum).OnlyEnforceIf(varBitmap[varTrack])
			varTrack = varTrack + 1

def _setDigitsInBlock(self,inlist,values):
	# The list of values must appear in the listed cells
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
			
		self.model.Add(sum(xVars) >= values.count(x))

def setOutside(self,row1,col1,rc,valueList):
	# row,col are the coordinates of the cell next to the clues
	# rc is whether things are row/column
	# valueList is a list of values that must appear in the first region in that direction
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	if 'Outside' not in self._constraintInitialized:
		self._constraintInitialized.append('Outside')
		self.outsideLength = -1

	if self.outsideLength == -1:
		# Clue is based on the region
		candCells = {(row+i*vStep,col+i*hStep) for i in range(self.boardWidth)}
		for i in range(len(self.regions)):
			if len({(row,col)} & set(self.regions[i])) > 0: currentRegion = i
		
		clueCells = list(candCells & set(self.regions[currentRegion]))
	else:
		# Clue is based on number of cells, independent of region
		clueCells = [(row+i*vStep,col+i*hStep) for i in range(self.outsideLength)]
		
	self._setDigitsInBlock(clueCells,valueList)
	
def setOutsideDiagonal(self,row1,col1,row2,col2,valueList):
	# row1,col1 is the position of the first cell on the diagonal
	# row2,col2 is the position of the second cell on the diagonal
	row = row1 - 1
	col = col1 - 1
	hStep = col2 - col1
	vStep = row2 - row1
	
	if 'Outside' not in self._constraintInitialized:
		self._constraintInitialized.append('Outside')
		self.outsideLength = -1
		
	if self.outsideLength == -1:
		# Clue is based on the region
		candCells = {(row+i*vStep,col+i*hStep) for i in range(self.boardWidth)}
		for i in range(len(self.regions)):
			if len({(row,col)} & set(self.regions[i])) > 0: currentRegion = i
		
		clueCells = list(candCells & set(self.regions[currentRegion]))
	else:
		# Clue is based on length
		clueCells = list({(row+i*vStep,col+i*hStep) for i in range(self.outsideLength)} & {(j,k) for j in range(self.boardWidth) for k in range(self.boardWidth)})
	self._setDigitsInBlock(clueCells,valueList)

def setOutsideLength(self,value):
	if 'Outside' not in self._constraintInitialized:
		self._constraintInitialized.append('Outside')
	self.outsideLength = value

def setCornerEdge(self,box1,ce,valueList):
	# box is the box number to which to apply the clue. 1-based so, upper left corner is 1, to its right is 2, etc.
	# ce specifies whether the clue is for corner (0) or edge (1). Use class variable Corner and Edge
	# valueList is the list of values to appear in these locations
	
	box = box1 - 1
	boxRow = box // self.boardSizeRoot
	boxCol = box % self.boardSizeRoot
	ulRow = self.boardSizeRoot * boxRow	# Cell in upper left corner of box
	ulCol = self.boardSizeRoot * boxCol
		
	for i in range(self.boardSizeRoot):
		for j in range(self.boardSizeRoot):
			if ((i > 0) and (i < self.boardSizeRoot - 1) and (j > 0) and (j < self.boardSizeRoot - 1)) or\
				((ce == self.Corner) and (i % (self.boardSizeRoot-1) != 0 or j % (self.boardSizeRoot-1) != 0)) or\
				((ce == self.Edge) and (i % (self.boardSizeRoot-1) == 0 and j % (self.boardSizeRoot-1) == 0)):	# Middle, edge, and corner square
					for k in valueList: self.model.Add(self.cellValues[ulRow+i][ulCol+j] != k)
					
def setRossini(self,row1,col1,udlr):
	# row,col is the cell next to the clue
	# udlr determines whether the arrow points up/down or left/right
	# value is optional. By default the increase condition holds in the first region, but if value is set it will hold
	# only for a fixed number of cells.
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	rc = self.Row if udlr >= self.Left else self.Col
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)

	if 'Rossini' not in self._constraintInitialized:
		self.rossiniLength = -1
		self.rossiniCells = [(row,col,rc)]
		self._constraintInitialized.append('Rossini')
	else:
		self.rossiniCells.append((row,col,rc))
	
	if self.rossiniLength == -1:	# We are using the default region-based cluing
		for i in range(len(self.regions)):
			if len({(row,col)} & set(self.regions[i])) > 0: region = i
		clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.boardWidth) if len({(row+i*vStep,col+i*hStep)} & set(self.regions[region])) > 0]
	else:
		clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.rossiniLength)]
		
	# So this is weird in external cluing, that the arrows are absolute with respect to the grid. So a left arrow on a row, regardless
	# of which side it is on, indicates the values increase from right to left. In this case, arrows on right or bottom are in the
	# "wrong" order, since they proceed from the edge into the grid (which is usually what you want.) So we reverse the array in these cases.
	
	if (rc == self.Row and col != 0) or (rc == self.Col and row != 0):
		clueCells.reverse()
		
	if udlr == self.Top or udlr == self.Left:		# Same value as self.Left
		for i in range(len(clueCells)-1):
			self.model.Add(clueCells[i] > clueCells[i+1])
	else:
		for i in range(len(clueCells)-1):
			self.model.Add(clueCells[i] < clueCells[i+1])
			
def setRossiniLength(self,value):
	if 'Rossini' not in self._constraintInitialized:
		self.rossiniCells = [(row,col,rc)]
		self._constraintInitialized.append('Rossini')
	self.rossiniLength = value

def setRossiniNegative(self):
	if 'Rossini' not in self._constraintInitialized:
		self.rossiniLength = -1
		self.rossiniCells = [(row,col,rc)]
		self._constraintInitialized.append('Rossini')
	self._constraintNegative.append('Rossini')
	
def _applyRossiniNegative(self):
	for i in range(0,self.boardWidth,self.boardWidth-1):	# Gives two values 0 and self.boardWidth-1...picks top/bottom , left/right
		for j in range(self.boardWidth):					# Pick which index to process
			for k in range(2):									# Pick row/col
				row = j if k is self.Row else i
				col = j if k is self.Col else i
				if (row,col,k) not in self.rossiniCells:
					hStep = 0 if k == self.Col else (1 if col == 0 else -1)
					vStep = 0 if k == self.Row else (1 if row == 0 else -1)
					if self.rossiniLength == -1:	# We are using the default region-based cluing
						for m in range(len(self.regions)):
							if len({(row,col)} & set(self.regions[m])) > 0: region = m
						clueCells = [self.cellValues[row+m*vStep][col+m*hStep] for m in range(self.boardWidth) if len({(row+m*vStep,col+m*hStep)} & set(self.regions[region])) > 0]
					else:
						clueCells = [self.cellValues[row+m*vStep][col+m*hStep] for m in range(self.rossiniLength)]
					# Note: no need to reverse since we're going to exclude a run in either direction
					
					# We're going to test each triple for an up-down, or down-up pattern
					varlist = []
					n = len(clueCells)
					for x in range(n):
						for y in range(x+1,n):
							for z in range(y+1,n):
								good = self.model.NewBoolVar('RossiniNeg')
								ud = self.model.NewBoolVar('RossiniNeg')
								self.model.Add(clueCells[x] < clueCells[y]).OnlyEnforceIf([good,ud])
								self.model.Add(clueCells[z] < clueCells[y]).OnlyEnforceIf([good,ud])
								self.model.Add(clueCells[x] > clueCells[y]).OnlyEnforceIf([good,ud.Not()])
								self.model.Add(clueCells[z] > clueCells[y]).OnlyEnforceIf([good,ud.Not()])
								self.model.Add(clueCells[x] < clueCells[y]).OnlyEnforceIf([good.Not(),ud])
								self.model.Add(clueCells[y] < clueCells[z]).OnlyEnforceIf([good.Not(),ud])
								self.model.Add(clueCells[x] > clueCells[y]).OnlyEnforceIf([good.Not(),ud.Not()])
								self.model.Add(clueCells[y] > clueCells[z]).OnlyEnforceIf([good.Not(),ud.Not()])
								varlist.append(good)
					self.model.AddBoolOr(varlist)		# Just need one triple to be good
								
def setMaxAscending(self,row1,col1,rc,value):
	# row,col are the coordinates of the cell containing the index of the target cell
	# rc is whether things are row/column
	# value is the length of the longest adjacent ascending run, looking from the clue
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	incBools = [self.model.NewBoolVar('MaxAscendingIncBoolRow{:d}Col{:d}RC{:d}'.format(row,col,rc)) for i in range(self.boardWidth-1)]
	incInts = [self.model.NewIntVar(0,1,'MaxAscendingIncIntRow{:d}Col{:d}RC{:d}'.format(row,col,rc)) for i in range(self.boardWidth-1)]
	for i in range(len(incBools)):
		self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] < self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep]).OnlyEnforceIf(incBools[i])
		self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] >= self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep]).OnlyEnforceIf(incBools[i].Not())
		self.model.Add(incInts[i] == 1).OnlyEnforceIf(incBools[i])
		self.model.Add(incInts[i] == 0).OnlyEnforceIf(incBools[i].Not())
		
	if value == 1:		# In this case the row/col must be strictly decreasing
		self.model.AddBoolAnd([x.Not() for x in incBools])
	else:
		lenBools = [self.model.NewBoolVar('MaxAscendingLenBoolRow{:d}Col{:d}RC{:d}'.format(row,col,rc)) for i in range(self.boardWidth+1-value)]
		for i in range(self.boardWidth+1-value):
			self.model.Add(sum([incInts[j] for j in range(i,i+value-1)]) == value-1).OnlyEnforceIf(lenBools[i])
			self.model.Add(sum([incInts[j] for j in range(i,i+value-1)]) < value-1).OnlyEnforceIf(lenBools[i].Not())
		self.model.AddBoolOr(lenBools)	#There is a run of length value
		
		for i in range(self.boardWidth-value):	#There is no longer run
			self.model.Add(sum([incInts[j] for j in range(i,i+value)]) < value)

def setSkyscraper(self,row1,col1,rc,value):
	# row,col are the coordinates of the cell containing the index of the target cell
	# rc is whether things are row/column
	# value is the number of digits that can be "seen" (i.e. are greater than all their predecessors) from the direction of the clue
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	# Create Boolean variables to determine where cell i in the row (from the correct direction) is greater than each of its predecessors
	incVars = [[]]
	for i in range(1,self.boardWidth):
		t = []
		for j in range(i):
			c = self.model.NewBoolVar('SkyscraperRow{:d}Col{:d}Cell{:d}Cell{:d}'.format(row,col,i,j))
			t.append(c)
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] > self.cellValues[row+j*vStep][col+j*hStep]).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] < self.cellValues[row+j*vStep][col+j*hStep]).OnlyEnforceIf(c.Not())
		incVars.insert(i,t)
	
	seenBools = [self.model.NewBoolVar('SkyscraperSeenBool{:d}{:d}'.format(row+i*vStep,col+i*hStep)) for i in range(self.boardWidth)]
	seenInts = [self.model.NewIntVar(0,1,'SkyscraperSeenInt{:d}{:d}'.format(row+i*vStep,col+i*hStep)) for i in range(self.boardWidth)]
	for i in range(self.boardWidth):
		self.model.Add(seenInts[i] == 1).OnlyEnforceIf(seenBools[i])
		self.model.Add(seenInts[i] == 0).OnlyEnforceIf(seenBools[i].Not())
		
	# Need to treat i=0 separately, since it is always seen, so seenBool[0] is always true
	self.model.AddBoolAnd([seenBools[0]])
	
	for i in range(1,self.boardWidth):
		self.model.AddBoolAnd(incVars[i]).OnlyEnforceIf(seenBools[i])
		self.model.AddBoolAnd([seenBools[i]]).OnlyEnforceIf(incVars[i])
		
	self.model.Add(sum([seenInts[i] for i in range(self.boardWidth)]) == value)
	
def setSkyscraperSum(self,row1,col1,rc,value):
	# row,col are the coordinates of the cell containing the index of the target cell
	# rc is whether things are row/column
	# value is the SUM of the digits that can be "seen" (i.e. are greater than all their predecessors) from the direction of the clue
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	# Create Boolean variables to determine where cell i in the row (from the correct direction) is greater than each of its predecessors
	incVars = [[]]
	for i in range(1,self.boardWidth):
		t = []
		for j in range(i):
			c = self.model.NewBoolVar('SkyscraperRow{:d}Col{:d}Cell{:d}Cell{:d}'.format(row,col,i,j))
			t.append(c)
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] > self.cellValues[row+j*vStep][col+j*hStep]).OnlyEnforceIf(c)
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] < self.cellValues[row+j*vStep][col+j*hStep]).OnlyEnforceIf(c.Not())
		incVars.insert(i,t)
	
	seenBools = [self.model.NewBoolVar('SkyscraperSeenBool{:d}{:d}'.format(row+i*vStep,col+i*hStep)) for i in range(self.boardWidth)]
	seenInts = [self.model.NewIntVar(min(self.minDigit,0),self.maxDigit,'SkyscraperSeenInt{:d}{:d}'.format(row+i*vStep,col+i*hStep)) for i in range(self.boardWidth)]
	for i in range(self.boardWidth):
		self.model.Add(seenInts[i] == self.cellValues[row+i*vStep][col+i*hStep]).OnlyEnforceIf(seenBools[i])
		self.model.Add(seenInts[i] == 0).OnlyEnforceIf(seenBools[i].Not())
		
	# Need to treat i=0 separately, since it is always seen, so seenBool[0] is always true
	self.model.AddBoolAnd([seenBools[0]])
	
	for i in range(1,self.boardWidth):
		self.model.AddBoolAnd(incVars[i]).OnlyEnforceIf(seenBools[i])
		self.model.AddBoolAnd([seenBools[i]]).OnlyEnforceIf(incVars[i])
		
	self.model.Add(sum([seenInts[i] for i in range(self.boardWidth)]) == value)

def setNextToNine(self,row1,col1,rc,values,digit=9):
	if type(values) is int:
		values  = [values]
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	varBitmap = self._varBitmap('NextToNineRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
	lr = self.model.NewBoolVar('NextToNineLeftRightChoice')
	lrA = [lr,lr.Not()]
	for i in range(self.boardWidth):
		self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == digit).OnlyEnforceIf(varBitmap[i])
		for j in range(len(values)):
			if i == 0:
				self.model.Add(self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep] == values[j]).OnlyEnforceIf(varBitmap[i])
				self.model.AddBoolAnd([lr]).OnlyEnforceIf(varBitmap[i])
			elif i == self.boardWidth - 1:
				self.model.Add(self.cellValues[row+(i-1)*vStep][col+(i-1)*hStep] == values[j]).OnlyEnforceIf(varBitmap[i])
				self.model.AddBoolAnd([lr.Not()]).OnlyEnforceIf(varBitmap[i])
			else:
				# If there are two values, the %2 trick in the variable ensures they alternate, so that values are put on different sides
				self.model.Add(self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep] == values[j]).OnlyEnforceIf(varBitmap[i] + [lrA[j%2]])
				self.model.Add(self.cellValues[row+(i-1)*vStep][col+(i-1)*hStep] == values[j]).OnlyEnforceIf(varBitmap[i] + [lrA[(j+1)%2]])
				
def setNextToNineSum(self,row1,col1,rc,value,digit=9):
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	varBitmap = self._varBitmap('NextToNineRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
	for i in range(self.boardWidth):
		self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == digit).OnlyEnforceIf(varBitmap[i])
		neighbors = {i-1,i+1} & {j for j in range(self.boardWidth)}
		self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in neighbors) == value).OnlyEnforceIf(varBitmap[i])

def setMaximumRun(self,row1,col1,rc,value,length=3):
	# row,col are the coordinates of the cell containing the index of the target cell
	# rc is whether things are row/column
	# value is the largest sum of any contiguous set of triplets in the clued row/column
	# length is the number of cells to add to create the sum
	
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	numSums = self.boardWidth - length + 1
	runVars = [self.model.NewBoolVar('MaximumRunVar') for i in range(numSums)]
	for i in range(numSums):
		self.model.Add(sum(self.cellValues[row+(i+j)*vStep][col+(i+j)*hStep] for j in range(length)) == value).OnlyEnforceIf(runVars[i])
		self.model.Add(sum(self.cellValues[row+(i+j)*vStep][col+(i+j)*hStep] for j in range(length)) < value).OnlyEnforceIf(runVars[i].Not())
	self.model.AddBoolOr(runVars)
	
def setMaximumTriplet(self,row1,col1,rc,value):
	self.setMaximumRun(row1,col1,rc,value,length=3)
	
def setDescriptivePair(self,row1,col1,rc,values):
	# Value is a list of two digits XY: either X appears in the Yth place, or Y appears in the Xth place in the row/column
	if type(values) is int:
		values = tuple(map(int,list(str(values))))
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	c = self.model.NewBoolVar('DescriptivePair')
	
	myRow = row if values[0] > 0 or rc == self.Row else self.boardWidth-1-row
	myCol = col if values[0] > 0 or rc == self.Col else self.boardWidth-1-col
	myHStep = hStep if values[0] > 0 else -1*hStep
	myVStep = vStep if values[0] > 0 else -1*vStep
	self.model.Add(self.cellValues[myRow+(abs(values[0])-1)*myVStep][myCol+(abs(values[0])-1)*myHStep] == values[1]).OnlyEnforceIf(c)
	
	myRow = row if values[1] > 0 or rc == self.Row else self.boardWidth-1-row
	myCol = col if values[1] > 0 or rc == self.Col else self.boardWidth-1-col
	myHStep = hStep if values[1] > 0 else -1*hStep
	myVStep = vStep if values[1] > 0 else -1*vStep
	self.model.Add(self.cellValues[myRow+(abs(values[1])-1)*myVStep][myCol+(abs(values[1])-1)*myHStep] == values[0]).OnlyEnforceIf(c.Not())

def setMinimax(self,row1,col1,rc,value,length=-1):
	# row,col is the cell next to the clue
	# rc is whether things are row/column
	# value is the value of the sum of the largest and smallest digits in the range
	# length: if not present, range over which to find min/max is defined by the region the clue is next to
	# If given, the clue will instead work on a fixed number of cells from the edge
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)

	if length == -1:	# We are using the default region-based cluing
		for i in range(len(self.regions)):
			if len({(row,col)} & set(self.regions[i])) > 0: region = i
		clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.boardWidth) if len({(row+i*vStep,col+i*hStep)} & set(self.regions[region])) > 0]
	else:
		clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(length)]
		
	# OK, we copied that from Rossini, now the hard part: min/max. Best just to do it, since that's
	# usually the best for these LP problems.
	minVars = [self.model.NewBoolVar('minimax') for i in range(len(clueCells))]
	maxVars = [self.model.NewBoolVar('minimax') for i in range(len(clueCells))]
	for i in range(len(clueCells)):
		for j in range(i,len(clueCells)):
			self.model.Add(clueCells[i] >= clueCells[j]).OnlyEnforceIf(maxVars[i])
			self.model.Add(clueCells[i] >= clueCells[j]).OnlyEnforceIf(minVars[j])
			self.model.Add(clueCells[i] <= clueCells[j]).OnlyEnforceIf(minVars[i])
			self.model.Add(clueCells[i] <= clueCells[j]).OnlyEnforceIf(maxVars[j])
			self.model.Add(clueCells[i]+clueCells[j] == value).OnlyEnforceIf([maxVars[j],minVars[i]])
			self.model.Add(clueCells[i]+clueCells[j] == value).OnlyEnforceIf([maxVars[i],minVars[j]])
	self.model.AddBoolOr(minVars)
	self.model.AddBoolOr(maxVars)
	
def setMaximin(self,row1,col1,rc,value,length=-1):
	# row,col is the cell next to the clue
	# rc is whether things are row/column
	# value is the value of the difference of the largest and smallest digits in the range
	# length: if not present, range over which to find min/max is defined by the region the clue is next to
	# If given, the clue will instead work on a fixed number of cells from the edge
	
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)

	if length == -1:	# We are using the default region-based cluing
		for i in range(len(self.regions)):
			if len({(row,col)} & set(self.regions[i])) > 0: region = i
		clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(self.boardWidth) if len({(row+i*vStep,col+i*hStep)} & set(self.regions[region])) > 0]
	else:
		clueCells = [self.cellValues[row+i*vStep][col+i*hStep] for i in range(length)]
		
	# OK, we copied that from Rossini, now the hard part: min/max. Best just to do it, since that's
	# usually the best for these LP problems.
	minVars = [self.model.NewBoolVar('maximin') for i in range(len(clueCells))]
	maxVars = [self.model.NewBoolVar('maximin') for i in range(len(clueCells))]
	for i in range(len(clueCells)):
		for j in range(i,len(clueCells)):
			self.model.Add(clueCells[i] >= clueCells[j]).OnlyEnforceIf(maxVars[i])
			self.model.Add(clueCells[i] >= clueCells[j]).OnlyEnforceIf(minVars[j])
			self.model.Add(clueCells[i] <= clueCells[j]).OnlyEnforceIf(minVars[i])
			self.model.Add(clueCells[i] <= clueCells[j]).OnlyEnforceIf(maxVars[j])
			self.model.Add(clueCells[j]-clueCells[i] == value).OnlyEnforceIf([maxVars[j],minVars[i]])
			self.model.Add(clueCells[i]-clueCells[j] == value).OnlyEnforceIf([maxVars[i],minVars[j]])
	self.model.AddBoolOr(minVars)
	self.model.AddBoolOr(maxVars)

def setFullRank(self,row1,col1,rc,value):
	if self.isFullRank is False:
		self._setFullRank()
		
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	i = row if rc==self.Row else col
	j = rc
	k = (0 if col == 0 else 1) if rc==self.Row else (0 if row == 0 else 1)
	self.model.Add(self.rcRank[4*i+2*j+k] == value)

def setParityParty(self,row1,col1,rc,value):
	if self.isParity is False:
		self._setParity()
		
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	varBitmap = self._varBitmap('ParityParty{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
	for i in range(self.boardWidth):
		self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(i)) == value).OnlyEnforceIf(varBitmap[i])
		if i > 1:
			for j in range(1,i-1):
				self.model.Add(self.cellParity[row][col] == self.cellParity[row+j*vStep][col+j*hStep]).OnlyEnforceIf(varBitmap[i])
			self.model.Add(self.cellParity[row][col] != self.cellParity[row+(i-1)*vStep][col+(i-1)*hStep]).OnlyEnforceIf(varBitmap[i])
			
def setSumSandwich(self,row1,col1,rc,values,neg=False):
	if type(values) is int:
		values  = [values]
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)

	for v in values:
		self.model.Add(self.cellValues[row][col] != v)
		self.model.Add(self.cellValues[row+(self.boardWidth-1)*vStep][col+(self.boardWidth-1)*hStep] != v)
		varBitmap = self._varBitmap('SumSandwich{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth-2)
		for i in range(1,self.boardWidth-1):
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == v).OnlyEnforceIf(varBitmap[i-1])
			self.model.Add(self.cellValues[row+(i-1)*vStep][col+(i-1)*hStep] + self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep] == v).OnlyEnforceIf(varBitmap[i-1])
			
	if neg is True:
		for v in self.digits:
			if v not in values:
				varBitmap = self._varBitmap('SumSandwich{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
				for i in range(self.boardWidth):
					self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == v).OnlyEnforceIf(varBitmap[i])
					if i > 0 and i < self.boardWidth-1:
						self.model.Add(self.cellValues[row+(i-1)*vStep][col+(i-1)*hStep] + self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep] != v).OnlyEnforceIf(varBitmap[i])
						
def setAscendingStarter(self,row1,col1,rc,value):
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	varBitmap = self._varBitmap('AscendingStarterRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
	for i in range(self.boardWidth):
		for j in range(i):
			self.model.Add(self.cellValues[row+j*vStep][col+j*hStep] < self.cellValues[row+(j+1)*vStep][col+(j+1)*hStep]).OnlyEnforceIf(varBitmap[i])
		if i < self.boardWidth-1:
			self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] > self.cellValues[row+(i+1)*vStep][col+(i+1)*hStep]).OnlyEnforceIf(varBitmap[i])
		self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(i+1)) == value).OnlyEnforceIf(varBitmap[i])

def setFirstSeenParity(self,row1,col1,rc,value):
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	if self.isParity is False:
		self._setParity()
	varBitmap = self._varBitmap('FirstSeenParityRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
	clueParity = value % 2
	for i in range(self.boardWidth):
		for j in range(i):
			self.model.Add(self.cellParity[row+j*vStep][col+j*hStep] != clueParity).OnlyEnforceIf(varBitmap[i])
		self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == value).OnlyEnforceIf(varBitmap[i])
		
def setFirstSeenEntropy(self,row1,col1,rc,value):
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	if self.isEntropy is False:
		self._setEntropy()
	varBitmap = self._varBitmap('FirstSeenEntropyRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
	clueEntropy = (value-1) // 3
	for i in range(self.boardWidth):
		for j in range(i):
			self.model.Add(self.cellEntropy[row+j*vStep][col+j*hStep] != clueEntropy).OnlyEnforceIf(varBitmap[i])
		self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == value).OnlyEnforceIf(varBitmap[i])

def setFirstSeenModular(self,row1,col1,rc,value):
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	if self.isModular is False:
		self._setModular()
	varBitmap = self._varBitmap('FirstSeenModularRow{:d}Col{:d}RC{:d}'.format(row,col,rc),self.boardWidth)
	clueModular = value - 3*((value-1) //3)
	for i in range(self.boardWidth):
		for j in range(i):
			self.model.Add(self.cellModular[row+j*vStep][col+j*hStep] != clueModular).OnlyEnforceIf(varBitmap[i])
		self.model.Add(self.cellValues[row+i*vStep][col+i*hStep] == value).OnlyEnforceIf(varBitmap[i])

def setPointingDifferents(self,row1,col1,row2,col2,value):
	hStep = col2 - col1
	vStep = row2 - row1
	# Note: we're keeping cells one-based, since we're passing to another function
	cells = list({(row1+vStep*k,col1+hStep*k) for k in range(self.boardWidth)} & {(i,j) for i in range(1,self.boardWidth+1) for j in range(1,self.boardWidth+1)})
	self.setDigitCountCage(cells,value)
	
def setBust(self,row1,col1,rc,value,targetSum=21):
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(value-1)) <= targetSum)
	self.model.Add(sum(self.cellValues[row+j*vStep][col+j*hStep] for j in range(value)) > targetSum)