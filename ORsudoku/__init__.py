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
	
	GE = 2 		# Constant to assert a greater than or equal to comparison
	EQ = 1		# Constant to assert an equal to comparison
	LE = 0		# Constant to assert an equal to comparison
	
	def mySuper(self):
		return super()

	def __init__(self,boardSizeRoot,irregular=None,digitSet=None,model=None):
		self.boardSizeRoot = boardSizeRoot
		self.boardWidth = boardSizeRoot*boardSizeRoot

		self.isBattenburgInitialized = False
		self.isBattenburgNegative = False
		
		self.isKropkiInitialized = False
		self.isKropkiNegative = False
		self.kropkiDiff = 1
		self.kropkiRatio = 2
		
		self.isFriendlyInitialized = False
		self.isFriendlyNegative = False
		
		self.isRossiniInitialized = False
		self.isRossiniNegative = False
		self.rossiniLength = -1
		self.outsideLength = -1
		
		self.isXVInitialized = False
		self.isXVNegative = False
		
		self.isXVXVInitialized = False
		self.isXVXVNegative = False
		
		self.isXYDifferenceInitialized = False
		self.isXYDifferenceNegative = False
		
		self.isEntropyQuadInitialized = False
		self.isEntropyQuadNegative = False
		
		self.isModularQuadInitialized = False
		self.isModularQuadNegative = False
		
		self.isEntropyBattenburgInitialized = False
		self.isEntropyBattenburgNegative = False
		
		self.isConsecutiveQuadInitialized = False
		self.isConsecutiveQuadNegative = False
		
		self.isParityQuadInitialized = False
		self.isParityQuadNegative = False
		self.parityQuadExcluded = [0,4]
		
		self.isParity = False
		self.isEntropy = False
		self.isModular = False
		self.isFullRank = False
		self.isPrimality = False
		
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
				self.allVars.append(mod)
				self.model.Add(2*div <= self.cellValues[i][j])
				self.model.Add(2*div+2 > self.cellValues[i][j])
				self.model.Add(mod == self.cellValues[i][j]-2*div)
			self.cellParity.insert(i,t)
		
		self.isParity = True
		
	def _setEntropy(self):
		# Set up variables to track entropy and modular constraints
		self.cellEntropy = []
		
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(self.minDigit // 3 - 1,self.maxDigit // 3,'entropyValue{:d}{:d}'.format(i,j))
				t.append(c)
				self.allVars.append(c)
				self.model.Add(3*c+1 <= self.cellValues[i][j])
				self.model.Add(3*c+4 > self.cellValues[i][j])
			self.cellEntropy.insert(i,t)
		
		self.isEntropy = True

	def _setModular(self):
		# Set up variables to track modular constraints
		if self.isEntropy is False:
			self._setEntropy()
		
		self.cellModular = []
		
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				c = self.model.NewIntVar(1,3,'modularValue{:d}{:d}'.format(i,j))
				t.append(c)
				self.allVars.append(c)
				self.model.Add(c == self.cellValues[i][j] - 3*self.cellEntropy[i][j])
			self.cellModular.insert(i,t)
		
		self.isModular = True
		
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
				
		self.isFullRank = True
		
	def _setPrimality(self):
		if self.boardWidth != 9 or self.minDigit < 0 or self.maxDigit > 9:
			print("Primality constraints only supported for digits {0..9} on 9x9 boards or smaller.")
			sys.exit()

		# Set up variables to track primality constraints
		self.cellPrimality = []
		for i in range(self.boardWidth):
			t = []
			for j in range(self.boardWidth):
				varBitmap = self.__varBitmap('PrimalityRow{:d}Col{:d}'.format(i,j),self.boardWidth)
				c = self.model.NewIntVar(0,2,'primalityValue{:d}{:d}'.format(i,j))
				self.model.Add(self.cellValues[i][j] == 1).OnlyEnforceIf(varBitmap[0])
				self.model.Add(c == 1).OnlyEnforceIf(varBitmap[0])
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
		self.isPrimality = True
		
	def getCellVar(self,i,j):
		# Returns the model variable associated with a cell value. Useful when tying several puzzles together, e.g. Samurai
		return self.cellValues[i][j]
		
	from ._globalConstraints import setXSudokuMain,setXSudokuOff,setBentDiagonals,setAntiDiagonalMain,setAntiDiagonalOff,setMagnitudeMirrorMain,setMagnitudeMirrorOff,setMagnitudeAntiMirrorMain,setMagnitudeAntiMirrorOff,setParityMirrorMain,setParityMirrorOff,setEntropyMirrorMain,setEntropyMirrorOff,setEntropyAntiMirrorMain,setEntropyAntiMirrorOff,setPrimalityMirrorMain,setPrimalityMirrorOff,setPrimalityAntiMirrorMain,setPrimalityAntiMirrorOff,setAntiKing,setAntiKnight,setKnightMare,setGeneralizedKnightMare,setDisjointGroups,setNonConsecutive,setWindoku,_setIndexCell,_setNonIndexCell,setIndexRow,setIndexColumn,setGlobalWhispers,setCloseNeighbors,setCloseNeighbours,setGlobalNeighborSum,setGlobalNeighbourSum,setGlobalEntropy,setGlobalModular,setQuadro,setUnicornDigit,setRepellingDigit,setAntiQueenDigit,setGSP,setRotationalPairs,setNoThreeInARowParity,setIsotopic,setNoConsecutiveSum,setNoSeven,setCountingCircles
	
	from ._singleCell import setGiven,setGivenArray,setMinMaxCell,setMinCell,setMaxCell,setMinMaxArray,setMinArray,setMaxArray,setEvenOdd,setOddEven,setEven,setOdd,setEvenArray,setOddArray,setEvenOddArray,setOddEvenArray,setNeighborSum,setNeighbourSum,setNeighborSumArray,setNeighbourSumArray,setFriendly,setFriendlyArray,setUnfriendly,setUnfriendlyArray,setFriendlyNegative,_applyFriendlyNegative,setScary,setPencilmarks,setPencilmarksArray,setSearchNine,setLogicBomb,assertNumberOfLogicBombs,setCupid,setNearestNeighbor,setNearestNeighbour,setDifferentNeighbors,setDifferentNeighbours,setSlingshot
	
	setOddEvenArray = setEvenOddArray
	
	
	from ._multiCell import setFortress,setKropkiWhite,setKropkiBlack,setKropkiGray,setKropkiWhiteArray,setKropkiBlackArray,setKropkiGrayArray,setKropkiArray,setKropkiNegative,setAntiKropki,setAntiKropkiArray,_applyKropkiNegative,setKropkiDifference,setKropkiRatio,setGammaEpsilon,setXVV,setXVX,setXVVArray,setXVXArray,setXVArray,setAntiXV,setAntiXVArray,setXVNegative,_applyXVNegative,setXVXVV,setXVXVX,setXVXVVArray,setXVXVXArray,setXVXVArray,setAntiXVXV,setAntiXVXVArray,setXVXVNegative,_applyXVXVNegative,setXYDifference,setXYDifferenceArray,setAntiXYDifference,setAntiXYDifferenceArray,setXYDifferenceNegative,_applyXYDifferenceNegative,setEitherOr,setEitherOrArray,setCloneRegion,setDominantCloneRegion,setShakenCloneRegion,setCage,setRepeatingCage,setMedianCage,setBlockCage,setMOTECage,setMETOCage,setUniparityCage,setEquiparityCage,setAllOddOrEven,setPuncturedCage,setPsychoKillerCage,setKnappDanebenCage,setCapsule,setDavidAndGoliath,setDigitCountCage,setVault,setZone,setLookAndSayCage,setPsychoLookAndSayCage,setOrderSumCages,setMagicSquare,setEntropkiWhite,setEntropkiBlack,setEntropkiWhiteArray,setEntropkiBlackArray,setEntropkiArray,setParityDotWhite,setParityDotBlack,setParityDotWhiteArray,setParityDotBlackArray,setParityDotArray,setGenetic,setGeneticArray,setParitySnake,setConsecutiveChainRegion,setAntiQueenCell,setTripleTab,setEqualSumCages
	
	from ._externalClues import setLittleKiller,setXSumBase,setXSum,setReverseXSum,setDoubleXSum,setXKropki,setNumberedRoomBase,setNumberedRoom,setReverseNumberedRoom,setSandwichSum,setOpenfacedSandwichSum,setBeforeNine,setBattlefield,setPositionSum,_setDigitsInBlock,setOutside,setOutsideDiagonal,setOutsideLength,setCornerEdge,setRossini,setRossiniLength,setRossiniNegative,_applyRossiniNegative,setMaxAscending,setSkyscraper,setSkyscraperSum,setNextToNine,setMaximumRun,setMaximumTriplet,setDescriptivePair,setMinimax,setMaximin,setFullRank,setParityParty,setSumSandwich,setAscendingStarter,setFirstSeenParity,setFirstSeenEntropy,setFirstSeenModular,setPointingDifferents,setBust
	
	from ._quadConstraints import setQuadruple,setQuadrupleArray,setQuadSum,setQuadSumArray,setBattenburg,setBattenburgArray,setBattenburgNegative,setAntiBattenburg,setAntiBattenburgArray,_applyBattenburgNegative,setEntropyQuad,setEntropyQuadArray,setEntropyQuadNegative,setAntiEntropyQuad,setAntiEntropyQuadArray,_applyEntropyQuadNegative,setModularQuad,setModularQuadArray,setModularQuadNegative,setAntiModularQuad,setAntiModularQuadArray,_applyModularQuadNegative,setParityQuad,setParityQuadArray,setParityQuadNegative,setAntiParityQuad,setAntiParityQuadArray,_applyParityQuadNegative,setParityQuadExclusions,setEntropyBattenburg,setEntropyBattenburgArray,setAntiEntropyBattenburg,setAntiEntropyBattenburgArray,setEntropyBattenburgNegative,_applyEntropyBattenburgNegative,setQuadMaxArrow,setQuadMaxArrowArray,setQuadMaxValue,setQuadMaxValueArray,setQuadMaxParityValue,setConsecutiveQuad,setConsecutiveQuadWhite,setConsecutiveQuadWhiteArray,setConsecutiveQuadBlack,setConsecutiveQuadBlackArray,setConsecutiveQuadArray,setAntiConsecutiveQuad,setAntiConsecutiveQuadArray,setConsecutiveQuadNegative,_applyConsecutiveQuadNegative,setDiagonalConsecutivePairs,setDiagonalConsecutivePairsArray
	
	from ._lineConstraints import setArrow,setHeavyArrow,setDoubleArrow,setPointingArrow,setMultiDigitSumArrow,setMissingArrow,setRepeatingArrow,setThermo,setSlowThermo,setFastThermo,setOddEvenThermo,setSlowOddEvenThermo,setMissingThermo,setvariableLengthThermo,setCountTheOddsLine,setKeypadKnightLine,setKeypadKingLine,setPalindromeLine,setParindromeLine,setWeakPalindromeLine,setParityLine,setRenbanLine,setRenrenbanbanLine,setNotRenbanLine,setRunOnRenbanLine,setMinWhispersLine,setMaxWhispersLine,setGermanWhispersLine,setDutchWhispersLine,setChineseWhispersLine,setMinExtendedWhispersLine,setMaxExtendedWhispersLine,setRunOnNabnerLine,setEntropicWhispersLine,setEntropicLine,setModularLine,setBetweenLine,setLockoutLine,setRegionSumLine,setRegionSegmentSumLine,setRegionometer,setDoublingLine,setShiftLine,setUpAndDownLine,setAverageLine,setNabnerLine,setParityCountLine,set10Line,setClockLine,setMagicLine,setConsecutiveLine,setZipperLine,setLineSumLine,setUniquePairsLines,setCellIndexLines,setSplitPeaLine,setSequenceLine
	
	from ._solving import applyNegativeConstraints,findSolution,preparePrintVariables,countSolutions,printCurrentSolution,testStringSolution,listCandidates,addExcludedDigit,addExcludedDigitArray,listCellCandidates
	
	from ._utilities import _varBitmap,_procCell,_procCellList,getOrthogonalNeighbors
