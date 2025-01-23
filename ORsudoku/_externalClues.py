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
	if 'FullRank' not in self._propertyInitialized:
		self._setFullRank()
		
	# Convert from 1-base to 0-base
	row = row1 - 1
	col = col1 - 1
	i = row if rc==self.Row else col
	j = rc
	k = (0 if col == 0 else 1) if rc==self.Row else (0 if row == 0 else 1)
	self.model.Add(self.rcRank[4*i+2*j+k] == value)

def setParityParty(self,row1,col1,rc,value):
	if 'Parity' not in self._propertyInitialized:
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
	if 'Parity' not in self._propertyInitialized:
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
	if 'Entropy' not in self._propertyInitialized:
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
	if 'Modular' not in self._propertyInitialized:
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
	
def setHangingSum(self,row1,col1,rc,value,selectSummands,selectTerminator,terminateOnFirst=True,includeTerminator=True):
	# OK, this one is going to need some comments, because I'm hoping it will cover a LOT of ground. Basically
	# this is going to be a general function to cover a number of different constraints that start at the grid
	# boundary and continue in, selecting digits based on some criteria, and terminating at a cell, determined
	# by some other criteria. Well, that's helpful. Thanks, Jeremy.
	
	# OK, what is selectSummands? It is a descriptor (TBD) of how to pick which cells to include in the sum
	# Same thing for selectTerminator, except it determines the termination condition
	# includeTerminator is a Boolean which picks whether or not to include the terminating cell
	
	row = row1 - 1
	col = col1 - 1
	hStep = 0 if rc == self.Col else (1 if col == 0 else -1)
	vStep = 0 if rc == self.Row else (1 if row == 0 else -1)
	
	# Since we don't know how this is going to terminate, or what is going to be picked, I think the best way to
	# go is to just create partial sums for each cell, basically "if the sum stopped at cell 5, what would the total be?"
	partialSum = [self.model.NewIntVar(min(0,self.boardWidth*self.minDigit),self.boardWidth*self.maxDigit,'HangingSumPartialSum{:d}'.format(i)) for i in range(self.boardWidth)]
	
	# Now I'm going to create selection Booleans to evaluate each cell against the selectSummand criteria. 
	# Notice how I'm clever enough to avoid defining selectSummands as long as I can. #genius
	selectionCells = [self.model.NewBoolVar('HangingSumCondition{:d}'.format(i)) for i in range(self.boardWidth)]
	
	self.allVars = self.allVars + partialSum
	
	# Tie the variables together
	self.model.Add(partialSum[0] == self.cellValues[row][col]).OnlyEnforceIf(selectionCells[0])
	self.model.Add(partialSum[0] == 0).OnlyEnforceIf(selectionCells[0].Not())
	for i in range(1,self.boardWidth):
		self.model.Add(partialSum[i] == partialSum[i-1] + self.cellValues[row+i*vStep][col+i*hStep]).OnlyEnforceIf(selectionCells[i])
		self.model.Add(partialSum[i] == partialSum[i-1]).OnlyEnforceIf(selectionCells[i].Not())
	
	# OK, document as I go! selectSummands is an array of criteria, all of which must be true for a cell to be
	# selected for a sum. Each array element is itself a tuple of at least two items: property, value.
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
	for criterion in selectSummands:
		criterionBools = [self.model.NewBoolVar('Criterion{:d}{:d}'.format(criterionNumber,i)) for i in range(self.boardWidth)]
		match criterion[0]:
			case 'Index':
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
			
			case 'IndexSkip':
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
				for i in range(self.boardWidth):
					self.model.Add(self.cellParity[row+i*vStep][col+i*hStep] == criterion[1]).OnlyEnforceIf(criterionBools[i])
					self.model.Add(self.cellParity[row+i*vStep][col+i*hStep] != criterion[1]).OnlyEnforceIf(criterionBools[i].Not())

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
						
		criteriaBools.insert(criterionNumber,criterionBools)
		criterionNumber = criterionNumber + 1
	
	# Ensure selectionCells[i] is True if and only if each of the underlying criteria is
	for i in range(self.boardWidth):
		self.model.AddBoolAnd([criteriaBools[j][i] for j in range(len(criteriaBools))]).OnlyEnforceIf(selectionCells[i])
		self.model.AddBoolOr([criteriaBools[j][i].Not() for j in range(len(criteriaBools))]).OnlyEnforceIf(selectionCells[i].Not())
		
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
			

		terminatorBools.insert(terminatorNumber,termBools)
		terminatorNumber = terminatorNumber + 1
	
	# A couple of parameters to cover here: 
	# terminateOnFirst: generically, termination is an "or" condition. If multiple terminators are given, any will serve as
	#   an indication to terminate. terminateOnFrist is the default behavior, which is to terminate on the first condition
	#   the can be met, in the line of cells. However, we can also terminate at any of them, making this a variable choice.
	#
	# includeTerminator: decides if the cell which indicates the termination of the sum should be included in the sum, default yes

	
	# For each terminator cell, need only one of the criteria below it to be true, so it could terminate here.
	for i in range(self.boardWidth):
		self.model.AddBoolOr([terminatorBools[j][i] for j in range(len(terminatorBools))]).OnlyEnforceIf(terminatorCells[i])
		self.model.AddBoolAnd([terminatorBools[j][i].Not() for j in range(len(terminatorBools))]).OnlyEnforceIf(terminatorCells[i].Not())
	
	if terminateOnFirst:
		if includeTerminator:
			self.model.Add(partialSum[0] == value).OnlyEnforceIf(terminatorCells[0])
		else:
			if value == 0:
				pass
			else:
				self.model.AddBoolAnd(terminatorCells[0].Not()).OnlyEnforceIf(terminatorCells[0])
		for i in range(1,self.boardWidth):
			if includeTerminator:
				self.model.Add(partialSum[i] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
			else:
				self.model.Add(partialSum[i-1] == value).OnlyEnforceIf([terminatorCells[i]] + [terminatorCells[j].Not() for j in range(i)])
	else:
		# OK, what the heck is going on here? I want to allow for the possibility that any place that provides a possible 
		# termination point could be chosen. Hence the varBitmap to pick. However. I want to ensure the solution is unique, so
		# I want to make sure to pick the *first* location which meets the condition. I actually don't care which, just need to
		# be canonical. The for j loop below ensures that if there is an earlier terminator that *could* be chosen, this
		# one cannot be.
		varBitmap = self._varBitmap('terminationPicker',self.boardWidth)
		self.allVars = self.allVars + varBitmap[0]
		for i in range(self.boardWidth):
			self.model.Add(partialSum[i] == value).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i]])
			self.model.AddBoolAnd(terminatorCells[i]).OnlyEnforceIf(varBitmap[i] + [terminatorCells[i].Not()])
			  # ensures this varBitmap cannot be chosen if terminatorCells is not set
			for j in range(i):
				c = self.model.NewBoolVar('solutionPickerSwitch')
				self.allVars = self.allVars + [c]
				self.model.Add(partialSum[j] != value).OnlyEnforceIf(varBitmap[i] + [c])
				self.model.AddBoolAnd(terminatorCells[j].Not()).OnlyEnforceIf(varBitmap[i] + [c.Not()])
				self.model.AddBoolAnd(c.Not()).OnlyEnforceIf(varBitmap[i] + [terminatorCells[j].Not()])
				for k in range(self.boardWidth):
					if k != i:
						self.model.AddBoolAnd(c).OnlyEnforceIf(varBitmap[k])