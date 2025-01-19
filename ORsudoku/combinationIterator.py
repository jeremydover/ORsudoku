class CombinationIterator():
	def __init__(self,n,k):
		self.n = n
		self.k = k
		self.Code = [j for j in range(k)] + [n+1]
				
	def getNext(self):
		if self.Code is None:
			return None
		else:
			current = self.Code[:-1:]
		flag = False
		for i in range(self.k):
			if (self.Code[i] + 1 < self.Code[i+1]):
				flag = True
				self.Code[i] = self.Code[i] + 1
				for j in range(i):
					self.Code[j] = j
				break
		if flag is False: self.Code = None					
		return current