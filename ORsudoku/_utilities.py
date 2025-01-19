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