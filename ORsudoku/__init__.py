from __future__ import print_function
from __future__ import print_function
import sys
import math
import colorama
from ortools.sat.python import cp_model
from array import *
from colorama import Fore,Back,init
init()

class sudoku:
	"""A class used to create a square Sudoku puzzle with variable size,
	   though 3x3 is the default and best (only?) tested use case.
	   
	   Constants
	   =========
		Row/Col - can specify a row/column to indicate whether a clue,
					typically given outside the grid, applies to a row or
					column. Usually only one choice, but needed for (literally)
					the corner cases.
				 
		V/X    - specifies type of XV or XVXV Sudoku clue is used
		
		White/Black - same as XV, but for Kropkis
		
		Horz/Vert - clues that go on edges are usually specified with the
		            grid of the top/left most cell, and then an H or V to
					determine whether the clue is on the right (H) or bottom (V)
					edge
					
		Location Specifications
		=======================
		Cells are specified by coordinates, with (0,0) at top left, (8,8) at bottom right
		First coordinate is the row, so a change causes vertial motion.
		
		Quads are specified analogously, on a (0,0) to (7,7) basis.
		
		Lines are specified as lists of cells. Order within the list usually matters, unless
		it does not matter for the underlying constraint.
		
		There are a whole fistful of methods, so I'm going to have to figure out a better way
		to document
	"""
		
	Row = 0		#Constant to pass to indicate row/column
	Col = 1		#Constant to pass to indicate row/column
	
	V = 0		#Constant to distinguish XV sudoku clues
	X = 1		#Constant to distinguish XV sudoku clues
	
	White = 0	#Constant to distinguish Kropki clues
	Black = 1	#Constant to distinguish Kropki clues
	Gray = 2	#Constant to distinguish Kropki clues
	
	Horz = 0	#Constant to determine clues going horizontally/vertically
	Vert = 1	#Constant to determine clues going horizontally/vertically
	
	Min = 0		#Constant to determine whether min/max clues are mins or maxs
	Max = 1		#Constant to determine whether min/max clues are mins or maxs
	
	Even = 0	# Constant to determine whether parity constraint is even or odd
	Odd = 1		# Constant to determine whether parity constraint is even or odd
	
	Top = 0		# Constant to determine direction arrow on 2x2 points...note code assumes this value is the same as Left
	Bottom = 1	# Constant to determine direction arrow on 2x2 points
	Left = 2	# Constant to determine direction arrow on 2x2 points
	Right = 3	# Constant to determine direction arrow on 2x2 points
	Up = 0		# Constant for Rossini clues
	Down = 1	# Constant for Rossini clues
	
	Corner = 0	# Constant to determine clue type for corner/edge clues
	Edge = 1	# Constant to determine clue type for corner/edge clues
	
	NE = 3      # Constant to assert a not equal comparison
	GE = 2 		# Constant to assert a greater than or equal to comparison
	EQ = 1		# Constant to assert an equal to comparison
	LE = 0		# Constant to assert a less than or equal to comparison
	
	Low = 0		# Constant to assert a value is "low"
	Middle = 1  # Constant to assert a value is "middle"
	High = 2	# Constant to assert a value is "high"
	
	Pos = 0		# Constant to assert a condition is "positive"
	Neg = 1     # Constant to assert a condition is "negative"
	
	def mySuper(self):
		return super()

	def __init__(self,boardSizeRoot,irregular=None,digitSet=None,model=None):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot
		
		self._constraintInitialized = []
		self._constraintNegative = []
		self._propertyInitialized = []
		
		if digitSet is None:
			self.digits = {x for x in range(1,self.boardWidth+1)}
		else:
			self.digits = digitSet
		self.maxDigit = max(self.digits)
		self.minDigit = min(self.digits)
		self.digitRange = self.maxDigit - self.minDigit

		if model is None:
			self.model = cp_model.CpModel()
		else:
			self.model = model
		self.cellValues = []
		self.allVars = []
		self.candTests = [[[None for k in range(len(self.digits))] for j in range(self.boardWidth)] for i in range(self.boardWidth)]
		self.candToExclude=[]
		
		# Create the variables containing the cell values
		for rowIndex in range(self.boardWidth):
			tempArray = []
			for colIndex in range(self.boardWidth):
				tempCell = self.model.NewIntVar(self.minDigit,self.maxDigit,'cellValue{:d}{:d}'.format(rowIndex,colIndex))
				if (self.maxDigit - self.minDigit) >= self.boardWidth:	#Digit set is not continguous, so force values
					self.model.AddAllowedAssignments([tempCell],[(x,) for x in digitSet])
				tempArray.append(tempCell)
				self.allVars.append(tempCell)
			self.cellValues.insert(rowIndex,tempArray)
			
		# Create rules to ensure rows and columns have no repeats
		for rcIndex in range(self.boardWidth):
			self.model.AddAllDifferent([self.cellValues[rcIndex][crIndex] for crIndex in range(self.boardWidth)]) 	# Rows
			self.model.AddAllDifferent([self.cellValues[crIndex][rcIndex] for crIndex in range(self.boardWidth)]) 	# Columns

		# Now deal with regions. Default to boxes...leaving stub for irregular Sudoku for now
		self.regions = []
		if irregular is None:
			self.__setBoxes()
			
	def __setBoxes(self):
		# Create rules to ensure boxes have no repeats
		for rowBox in range(self.boardSizeRoot):
			for colBox in range(self.boardSizeRoot):
				tempCellArray = []
				tempCellIndexArray = []
				for rowIndex in range(self.boardSizeRoot):
					for colIndex in range(self.boardSizeRoot):
						tempCellArray.append(self.cellValues[self.boardSizeRoot*rowBox+rowIndex][self.boardSizeRoot*colBox+colIndex])
						tempCellIndexArray.append((self.boardSizeRoot*rowBox+rowIndex,self.boardSizeRoot*colBox+colIndex))
				self.model.AddAllDifferent(tempCellArray)					# Squares
				self.regions.append(tempCellIndexArray)

	def setRegion(self,inlist):
		# Allow setting of irregular regions
		inlist = self._procCellList(inlist)
		self.regions.append(inlist)
		self.model.AddAllDifferent([self.cellValues[x[0]][x[1]] for x in self.regions[-1]])
		
	def setRegions(self,inlist):
		# Allow setting of multiple regions
		for x in inlist: self.setRegion(x)
		
	def getRegion(self,row,col):
		return [i for i in range(len(self.regions)) if (row,col) in self.regions[i]][0]

	def _initializeParity(self):
		if 'Parity' not in self._propertyInitialized:
			self._setParity()
	
	def _setParity(self):
		# Set up variables to track parity constraints
		divVars = []
		self.cellParity = []
		
		maxDiff = self.maxDigit-self.minDigit
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				div = self.model.NewIntVar(0,2*maxDiff,'ParityDiv')
				mod = self.model.NewIntVar(0,1,'parityValue{:d}{:d}'.format(i,j))
				t.append(mod)
				self.model.Add(2*div <= self.cellValues[i][j])
				self.model.Add(2*div+2 > self.cellValues[i][j])
				self.model.Add(mod == self.cellValues[i][j]-2*div)
			self.cellParity.insert(i,t)
		
		self._propertyInitialized.append('Parity')
		
	def _initializeEntropy(self):
		if 'Entropy' not in self._propertyInitialized:
			self._setEntropy()

	def _setEntropy(self):
		# Set up variables to track entropy and modular constraints
		self.cellEntropy = []
		
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(self.minDigit // 3 - 1,self.maxDigit // 3,'entropyValue{:d}{:d}'.format(i,j))
				t.append(c)
				self.model.Add(3*c+1 <= self.cellValues[i][j])
				self.model.Add(3*c+4 > self.cellValues[i][j])
			self.cellEntropy.insert(i,t)
		
		self._propertyInitialized.append('Entropy')

	def _initializeModular(self):
		if 'Modular' not in self._propertyInitialized:
			self._setModular()

	def _setModular(self):
		# Set up variables to track modular constraints
		if 'Entropy' not in self._propertyInitialized:
			self._setEntropy()
		
		self.cellModular = []
		
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(1,3,'modularValue{:d}{:d}'.format(i,j))
				t.append(c)
				self.model.Add(c == self.cellValues[i][j] - 3*self.cellEntropy[i][j])
			self.cellModular.insert(i,t)
		
		self._propertyInitialized.append('Modular')
		
	def _setFullRank(self):
		if self.boardWidth != 9 or self.minDigit < 0 or self.maxDigit > 9:
			print("Full rank constraints only supported for digits {0..9} on 9x9 boards or smaller.")
			sys.exit()
			
		# Set up variables to track full rank constraints
		self.rcRank = [self.model.NewIntVar(1,4*self.boardWidth,'fullRankRank') for i in range(4*self.boardWidth)]
		self.rcSum = [self.model.NewIntVar(0,10**self.boardWidth,'fullRankSum') for i in range(4*self.boardWidth)]
		# Set up tie between rank sums and cell values
		for k in range(2):	# Top/left or bottom/right
			for j in range(2):	# Row or column
				for i in range(self.boardWidth):
					# Note: these sums seems backwards because the closest digit to the clue is the MOST significant
					sumRow = i if j == sudoku.Row else (self.boardWidth-1 if k == 0 else 0)
					sumCol = i if j == sudoku.Col else (self.boardWidth-1 if k == 0 else 0)
					hStep = 0 if j == sudoku.Col else (-1 if k == 0 else 1) 
					vStep = 0 if j == sudoku.Row else (-1 if k == 0 else 1)
					#print (sum(self.cellValue[sumRow+m*vStep][sumCol+m*hStep]*10**m for m in range(self.boardWidth)))
					self.model.Add(self.rcSum[4*i+2*j+k] == sum(self.cellValues[sumRow+m*vStep][sumCol+m*hStep]*10**m for m in range(self.boardWidth)))
		
		# Set up Booleans to force rank ordering
		for i in range(4*self.boardWidth):
			for j in range(i+1,4*self.boardWidth):
				c = self.model.NewBoolVar('rankOrder{:d}{:d}'.format(i,j))
				self.model.Add(self.rcSum[i] > self.rcSum[j]).OnlyEnforceIf(c)
				self.model.Add(self.rcRank[i] > self.rcRank[j]).OnlyEnforceIf(c)
				self.model.Add(self.rcSum[i] < self.rcSum[j]).OnlyEnforceIf(c.Not())
				self.model.Add(self.rcRank[i] < self.rcRank[j]).OnlyEnforceIf(c.Not())
				
		self._propertyInitialized.append('FullRank')
		
	def _initializePrimality(self):
		if 'Primality' not in self._propertyInitialized:
			self._setPrimality()

	def configurePrimality(self,whatIsOne='Neither'):
		match whatIsOne:
			case 'Prime':
				one = 0
			case 'NotPrime':
				one = 2
			case 'Neither':
				one = 1
		self._setPrimality(one)
	
	def _setPrimality(self,whatIsOne=1):
		if self.boardWidth != 9 or self.minDigit < 0 or self.maxDigit > 9:
			print("Primality constraints only supported for digits {0..9} on 9x9 boards or smaller.")
			sys.exit()

		# Set up variables to track primality constraints
		self.cellPrimality = []
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				varBitmap = self._varBitmap('PrimalityRow{:d}Col{:d}'.format(i,j),self.boardWidth)
				c = self.model.NewIntVar(0,2,'primalityValue{:d}{:d}'.format(i,j))
				self.model.Add(self.cellValues[i][j] == 1).OnlyEnforceIf(varBitmap[0])
				self.model.Add(c == whatIsOne).OnlyEnforceIf(varBitmap[0])
				self.model.Add(self.cellValues[i][j] == 2).OnlyEnforceIf(varBitmap[1])
				self.model.Add(c == 0).OnlyEnforceIf(varBitmap[1])
				self.model.Add(self.cellValues[i][j] == 3).OnlyEnforceIf(varBitmap[2])
				self.model.Add(c == 0).OnlyEnforceIf(varBitmap[2])
				self.model.Add(self.cellValues[i][j] == 4).OnlyEnforceIf(varBitmap[3])
				self.model.Add(c == 2).OnlyEnforceIf(varBitmap[3])
				self.model.Add(self.cellValues[i][j] == 5).OnlyEnforceIf(varBitmap[4])
				self.model.Add(c == 0).OnlyEnforceIf(varBitmap[4])
				self.model.Add(self.cellValues[i][j] == 6).OnlyEnforceIf(varBitmap[5])
				self.model.Add(c == 2).OnlyEnforceIf(varBitmap[5])
				self.model.Add(self.cellValues[i][j] == 7).OnlyEnforceIf(varBitmap[6])
				self.model.Add(c == 0).OnlyEnforceIf(varBitmap[6])
				self.model.Add(self.cellValues[i][j] == 8).OnlyEnforceIf(varBitmap[7])
				self.model.Add(c == 2).OnlyEnforceIf(varBitmap[7])
				self.model.Add(self.cellValues[i][j] == 9).OnlyEnforceIf(varBitmap[8])
				self.model.Add(c == 2).OnlyEnforceIf(varBitmap[8])
				t.append(c)
			self.cellPrimality.insert(i,t)
		self._propertyInitialized.append('Primality')
		
	def getCellVar(self,i,j):
		# Returns the model variable associated with a cell value. Useful when tying several puzzles together, e.g. Samurai
		return self.cellValues[i][j]
		
	def assertNoRoping(self,rc):
		if rc == self.Row:
			rows = [[(3*j,i) for i in range(3)] for j in range(3)]
		else:
			rows = [[(i,3*j) for i in range(3)] for j in range(3)]

		minVars = [self.model.NewIntVar(self.minDigit,self.maxDigit,'roping') for j in range(3)]
		for i in range(3):
			self.model.AddMinEquality(minVars[i],[self.cellValues[x[0]][x[1]] for x in rows[i]])
		maxVars = [self.model.NewIntVar(self.minDigit,self.maxDigit,'roping') for j in range(3)]
		for i in range(3):
			self.model.AddMaxEquality(maxVars[i],[self.cellValues[x[0]][x[1]] for x in rows[i]])
		sumVars = [self.model.NewIntVar(3*self.minDigit,3*self.maxDigit,'roping') for j in range(3)]
		for i in range(3):
			self.model.Add(sumVars[i] == sum([self.cellValues[x[0]][x[1]] for x in rows[i]]))
		
		hStep = 0 if rc == self.Col else 1
		vStep = 0 if rc == self.Row else 1
		
		for i in range(3):
			for j in range(1,3):
				myMinVar = self.model.NewIntVar(self.minDigit,self.maxDigit,'roping')
				myMaxVar = self.model.NewIntVar(self.minDigit,self.maxDigit,'roping')
				mySumVar = self.model.NewIntVar(3*self.minDigit,3*self.maxDigit,'roping')
				myTestRow = [(x[0]+j*hStep+3*vStep,x[1]+j*vStep+3*hStep) for x in rows[i]]

				self.model.AddMinEquality(myMinVar,[self.cellValues[x[0]][x[1]] for x in myTestRow])
				self.model.AddMaxEquality(myMaxVar,[self.cellValues[x[0]][x[1]] for x in myTestRow])
				self.model.Add(mySumVar == sum([self.cellValues[x[0]][x[1]] for x in myTestRow]))
				
				compVars = [self.model.NewBoolVar('roping') for k in range(3)]
				self.model.Add(minVars[i] == myMinVar).OnlyEnforceIf(compVars[0].Not())
				self.model.Add(minVars[i] != myMinVar).OnlyEnforceIf(compVars[0])
				self.model.Add(maxVars[i] == myMaxVar).OnlyEnforceIf(compVars[1].Not())
				self.model.Add(maxVars[i] != myMaxVar).OnlyEnforceIf(compVars[1])
				self.model.Add(sumVars[i] == mySumVar).OnlyEnforceIf(compVars[2].Not())
				self.model.Add(sumVars[i] != mySumVar).OnlyEnforceIf(compVars[2])
				self.model.AddBoolOr(compVars)
				
	from ._globalConstraints import setXSudokuMain,setXSudokuOff,setBentDiagonals,setAntiDiagonalMain,setAntiDiagonalOff,setMagnitudeMirrorMain,setMagnitudeMirrorOff,setMagnitudeAntiMirrorMain,setMagnitudeAntiMirrorOff,setParityMirrorMain,setParityMirrorOff,setEntropyMirrorMain,setEntropyMirrorOff,setEntropyAntiMirrorMain,setEntropyAntiMirrorOff,setPrimalityMirrorMain,setPrimalityMirrorOff,setPrimalityAntiMirrorMain,setPrimalityAntiMirrorOff,setAntiKing,setAntiKnight,setKnightMare,setGeneralizedKnightMare,setDisjointGroups,setNonConsecutive,setWindoku,_setIndexCell,_setNonIndexCell,setIndexRow,setIndexColumn,setGlobalWhispers,setCloseNeighbors,setCloseNeighbours,setGlobalNeighborSum,setGlobalNeighbourSum,setGlobalEntropy,setGlobalModular,setQuadro,setUnicornDigit,setRepellingDigit,setAntiQueenDigit,setGSP,setRotationalPairs,setNoThreeInARowParity,setIsotopic,setNoConsecutiveSum,setNoSeven,setCountingCircles,setOffsetDigit,setFlatMates,setDutchFlatMates
	
	from ._singleCell import setGiven,setGivenArray,setMinMaxCell,setMinCell,setMaxCell,setMinMaxArray,setMaxMinArray,setMinArray,setMaxArray,setEvenOdd,setOddEven,setEven,setOdd,setEvenArray,setOddArray,setEvenOddArray,setOddEvenArray,setNeighborSum,setNeighbourSum,setNeighborSumArray,setNeighbourSumArray,setFriendly,setFriendlyArray,setUnfriendly,setUnfriendlyArray,setFriendlyNegative,_applyFriendlyNegative,setScary,setPencilmarks,setPencilmarksArray,setSearchNine,setLogicBomb,assertNumberOfLogicBombs,setCupid,setNearestNeighbor,setNearestNeighbour,setDifferentNeighbors,setDifferentNeighbours,setSlingshot,_initializeNeighborSet,_setNeighborSetBase,setPosNeighborSet,setPosNeighbourSet,setNegNeighborSet,setNegNeighbourSet,setPosNeighborSetArray,setPosNeighbourSetArray,setNegNeighborSetArray,setNegNeighbourSetArray,setNeighborSetArray,setNeighbourSetArray,setNeighborSetProperty,setNeighbourSetProperty,setNeighborSetNegative,setNeighbourSetNegative,_applyNeighborSetNegative,setRemoteClone
	
	from ._multiCell import setFortress,_initializeKropkiWhite,_initializeKropkiBlack,setKropkiWhite,setKropkiBlack,setKropkiGray,setKropkiWhiteArray,setKropkiBlackArray,setKropkiGrayArray,setKropkiArray,setKropkiWhiteNegative,setKropkiBlackNegative,setKropkiNegative,setAntiKropkiWhite,setAntiKropkiBlack,setAntiKropki,setAntiKropkiWhiteArray,setAntiKropkiBlackArray,setAntiKropkiArray,_applyKropkiWhiteNegative,_applyKropkiBlackNegative,setKropkiDifference,setKropkiRatio,setGammaEpsilon,_initializeRemoteKropkiWhite,_initializeRemoteKropkiBlack,_setRemoteKropkiBase,setRemoteKropkiWhite,setRemoteKropkiBlack,setRemoteKropkiGray,setRemoteKropkiWhiteArray,setRemoteKropkiBlackArray,setRemoteKropkiGrayArray,setRemoteKropkiArray,setRemoteKropkiDifference,setRemoteKropkiRatio,_initializeRomanSum,setRomanSum,setXVV,setXVX,setRomanSumArray,setXVVArray,setXVXArray,setXVArray,setAntiRomanSum,setAntiRomanSums,setAntiXVV,setAntiXVX,setAntiXV,setAntiRomanSumArray,setAntiRomanSumsArray,setAntiXVVArray,setAntiXVXArray,setAntiXVArray,setRomanSumNegative,setXVVNegative,setXVXNegative,setXVNegative,_applyRomanSumNegative,setXVXVV,setXVXVX,setXVXVVArray,setXVXVXArray,setXVXVArray,setAntiXVXV,setAntiXVXVArray,setXVXVNegative,_applyXVXVNegative,setXYDifference,setXYDifferenceArray,setAntiXYDifference,setAntiXYDifferenceArray,setXYDifferenceNegative,_applyXYDifferenceNegative,setEitherOr,setEitherOrArray,setCloneRegion,setDominantCloneRegion,setShakenCloneRegion,setHiddenClones,setCage,setMaxMinSumCage,setRepeatingCage,setMedianCage,setBlockCage,setMOTECage,setMETOCage,setUniparityCage,setEquiparityCage,setAllOddOrEven,setPuncturedCage,setPsychoKillerCage,setKnappDanebenCage,setCapsule,setDavidAndGoliath,setDigitCountCage,setVault,setZone,setLookAndSayCage,setPsychoLookAndSayCage,setOrderSumCages,setMagicSquare,setEntropkiWhite,setEntropkiBlack,setEntropkiWhiteArray,setEntropkiBlackArray,setEntropkiArray,setParityDotWhite,setParityDotBlack,setParityDotWhiteArray,setParityDotBlackArray,setParityDotArray,setGenetic,setGeneticArray,setParitySnake,setConsecutiveChainRegion,setAntiQueenCell,setTripleTab,setEqualSumCages
	
	from ._externalClues import setLittleKiller,setXSumBase,setXSum,setReverseXSum,setDoubleXSum,setXAverageBase,setXAverage,setReverseXAverage,setXKropki,setNumberedRoomBase,setNumberedRoom,setReverseNumberedRoom,setSandwichSum,setOpenfacedSandwichSum,setShortSandwichSum,setConditionalSandwichSum,setBeforeNine,setBattlefield,setPositionSum,_setDigitsInBlock,setOutside,setOutsideDiagonal,setOutsideLength,setCornerEdge,setRossini,setRossiniLength,setRossiniNegative,_applyRossiniNegative,setMaxAscendingRun,setMaxAscending,setSkyscraper,setSkyscraperSum,setNextToNine,setNextToNineSum,setMaximumRun,setMaximumTriplet,setDescriptivePair,setMinimax,setMaximin,setFullRank,setParityParty,setSumSandwich,setAscendingStarter,setFirstSeenParity,setFirstSeenEntropy,setFirstSeenModular,setPointingDifferents,setBust,setHangingSum,setHangingCount,setHangingAverage,setXOutside
	
	from ._quadConstraints import setQuadruple,setQuadrupleArray,setQuadSum,setQuadSumArray,setMaxMinQuadSum,setMaxMinQuadSumArray,setBattenburg,setBattenburgArray,setBattenburgNegative,setAntiBattenburg,setAntiBattenburgArray,_applyBattenburgNegative,setEntropyQuad,setEntropyQuadArray,setEntropyQuadNegative,setAntiEntropyQuad,setAntiEntropyQuadArray,_applyEntropyQuadNegative,setModularQuad,setModularQuadArray,setModularQuadNegative,setAntiModularQuad,setAntiModularQuadArray,_applyModularQuadNegative,_initializeParityQuad,setParityQuad,setParityQuadArray,setParityQuadNegative,setAntiParityQuad,setAntiParityQuadArray,_applyParityQuadNegative,setParityQuadExclusions,_initializeEntropyBattenburg,setEntropyBattenburg,setEntropyBattenburgArray,setAntiEntropyBattenburg,setAntiEntropyBattenburgArray,setEntropyBattenburgNegative,_applyEntropyBattenburgNegative,setQuadMaxArrow,setQuadMaxArrowArray,setQuadMaxValue,setQuadMaxValueArray,setQuadMaxParityValue,setConsecutiveQuad,setConsecutiveQuadWhite,setConsecutiveQuadWhiteArray,setConsecutiveQuadBlack,setConsecutiveQuadBlackArray,setConsecutiveQuadArray,setAntiConsecutiveQuad,setAntiConsecutiveQuadArray,setConsecutiveQuadNegative,_applyConsecutiveQuadNegative,setDiagonalConsecutivePairs,setDiagonalConsecutivePairsArray
	
	from ._lineConstraints import setArrow,setHeavyArrow,setDoubleArrow,setPointingArrow,setMultiDigitSumArrow,setMissingArrow,setRepeatingArrow,setThermo,setSlowThermo,setFastThermo,setOddEvenThermo,setSlowOddEvenThermo,setMissingThermo,setBrokenThermo,setDoubleThermo,setRemovedBulbThermo,setCountTheOddsLine,setKeypadKnightLine,setKeypadKingLine,setPalindromeLine,setParindromeLine,setWeakPalindromeLine,setParityLine,setRenbanLine,setRenrenbanbanLine,setNotRenbanLine,setRunOnRenbanLine,setMinWhispersLine,setMaxWhispersLine,setGermanWhispersLine,setDutchWhispersLine,setChineseWhispersLine,setMinExtendedWhispersLine,setMaxExtendedWhispersLine,setRunOnNabnerLine,setEntropicWhispersLine,setEntropicLine,setModularLine,setBetweenLine,setLockoutLine,setRegionSumLine,setRegionSegmentSumLine,setRegionometer,setDoublingLine,setShiftLine,setUpAndDownLine,setAverageLine,setNabnerLine,setParityCountLine,set10Line,setClockLine,setMagicLine,setConsecutiveLine,setZipperLine,setLineSumLine,setUniquePairsLines,setCellIndexLines,setSplitPeaLine,setSequenceLine,setIndexLine,setLotLine,setConditionalSumLine
	
	from ._solving import applyNegativeConstraints,findSolution,preparePrintVariables,countSolutions,printCurrentSolution,testStringSolution,listCandidates,addExcludedDigit,addExcludedDigitArray,listCellCandidates
	
	from ._utilities import _varBitmap,_procCell,_procCellList,getOrthogonalNeighbors,_selectCellsOnLine,_selectCellsInRowCol,_terminateCellsOnLine,_terminateCellsInRowCol,_evaluateHangingClues