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
	
	Big = 2		# Constant to assert a "big" digit size
	Neither = 1 # Constant to assert an "in-between" digit size, i.e., 5
	Small = 0 	# Constant to assert a "small" digit size
	
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
		
	from ._globalConstraints import setXSudokuMain,setXSudokuOff,setBentDiagonals,setAntiDiagonalMain,setAntiDiagonalOff,setMagnitudeMirrorMain,setMagnitudeMirrorOff,setMagnitudeAntiMirrorMain,setMagnitudeAntiMirrorOff,setParityMirrorMain,setParityMirrorOff,setEntropyMirrorMain,setEntropyMirrorOff,setEntropyAntiMirrorMain,setEntropyAntiMirrorOff,setPrimalityMirrorMain,setPrimalityMirrorOff,setPrimalityAntiMirrorMain,setPrimalityAntiMirrorOff,setAntiKing,setAntiKnight,setKnightMare,setGeneralizedKnightMare,setDisjointGroups,setNonConsecutive,setWindoku,_setIndexCell,_setNonIndexCell,setIndexRow,setIndexColumn,setGlobalWhispers,setCloseNeighbors,setCloseNeighbours,setGlobalNeighborSum,setGlobalNeighbourSum,setGlobalEntropy,setGlobalModular,setQuadro,setUnicornDigit,setRepellingDigit,setAntiQueenDigit,setGSP,setRotationalPairs,setNoThreeInARowParity,setIsotopic,setNoConsecutiveSum,setNoSeven,setCountingCircles,setOffsetDigit,setFlatMates,setDutchFlatMates,setPool,setBattleships,setDismode,setDisparity,setDisentropy,setDismodular,setTopDownCondition,setLeftRightCondition,setOrthogonalCondition,setTopHeavy
	
	from ._singleCell import setGiven,setGivenArray,setMinMaxCell,setMinCell,setMaxCell,setMinMaxArray,setMaxMinArray,setMinArray,setMaxArray,setEvenOdd,setOddEven,setEven,setOdd,setEvenArray,setOddArray,setEvenOddArray,setOddEvenArray,setNeighborSum,setNeighbourSum,setNeighborSumArray,setNeighbourSumArray,setFriendly,setFriendlyArray,setUnfriendly,setUnfriendlyArray,setFriendlyNegative,_applyFriendlyNegative,setScary,setPencilmarks,setPencilmarksArray,setSearchNine,setLogicBomb,assertNumberOfLogicBombs,setCupid,setNearestNeighbor,setNearestNeighbour,setDifferentNeighbors,setDifferentNeighbours,setSlingshot,_initializeNeighborSet,_setNeighborSetBase,setPosNeighborSet,setPosNeighbourSet,setNegNeighborSet,setNegNeighbourSet,setPosNeighborSetArray,setPosNeighbourSetArray,setNegNeighborSetArray,setNegNeighbourSetArray,setNeighborSetArray,setNeighbourSetArray,setNeighborSetProperty,setNeighbourSetProperty,setNeighborSetNegative,setNeighbourSetNegative,_applyNeighborSetNegative,setRemoteClone,setRepeatedNeighbors,setRepeatedNeighbours,setRepeatedNeighborsArray,setRepeatedNeighboursArray,setDistinctNeighbors,setDistinctNeighbours,setDistinctNeighborsArray,setDistinctNeighboursArray,setRepeatedNeighborsNegative,setRepeatedNeighboursNegative,_applyRepeatedNeighborsNegative,setConditionalCountCross,_initializeSweeper,_setSweeperCellBase,setSweeper,setAntiSweeper,setSweeperNegative,_applySweeperNegative,setIndexedPairSum,setNMates
	
	from ._multiCell import setFortress,_initializeKropkiWhite,_initializeKropkiBlack,_modelKropkiWhiteRelationship,_modelKropkiBlackRelationship,setKropkiWhite,setKropkiBlack,setKropkiGray,setKropkiWhiteArray,setKropkiBlackArray,setKropkiGrayArray,setKropkiArray,setKropkiWhiteNegative,setKropkiBlackNegative,setKropkiNegative,setAntiKropkiWhite,setAntiKropkiBlack,setAntiKropki,setAntiKropkiWhiteArray,setAntiKropkiBlackArray,setAntiKropkiArray,_applyKropkiWhiteNegative,_applyKropkiBlackNegative,setKropkiDifference,setKropkiRatio,setGammaEpsilon,setKroopki,setKroopkiArray,_initializeRemoteKropkiWhite,_initializeRemoteKropkiBlack,_setRemoteKropkiBase,setRemoteKropkiWhite,setRemoteKropkiBlack,setRemoteKropkiGray,setRemoteKropkiWhiteArray,setRemoteKropkiBlackArray,setRemoteKropkiGrayArray,setRemoteKropkiArray,setRemoteKropkiDifference,setRemoteKropkiRatio,_initializeRomanSum,setRomanSum,setXVV,setXVX,setRomanSumArray,setXVVArray,setXVXArray,setXVArray,setAntiRomanSum,setAntiRomanSums,setAntiXVV,setAntiXVX,setAntiXV,setAntiRomanSumArray,setAntiRomanSumsArray,setAntiXVVArray,setAntiXVXArray,setAntiXVArray,setRomanSumNegative,setXVVNegative,setXVXNegative,setXVNegative,_applyRomanSumNegative,setXVXVV,setXVXVX,setXVXVVArray,setXVXVXArray,setXVXVArray,setAntiXVXV,setAntiXVXVArray,setXVXVNegative,_applyXVXVNegative,setXYDifference,setXYDifferenceArray,setAntiXYDifference,setAntiXYDifferenceArray,setXYDifferenceNegative,_applyXYDifferenceNegative,setEitherOr,setEitherOrArray,setCloneRegion,setDominantCloneRegion,setShakenCloneRegion,setDigitComparison,setHiddenClones,setCage,setMaxMinSumCage,setRepeatingCage,setMedianCage,setBlockCage,setMOTECage,setMETOCage,setUniparityCage,setEquiparityCage,setAllOddOrEven,setPuncturedCage,setPsychoKillerCage,setKnappDanebenCage,setEqualSumCages,setRankedCage,setCapsule,setDavidAndGoliath,setDigitCountCage,setVault,setZone,setLookAndSayCage,setPsychoLookAndSayCage,setOrderSumCages,setMagicSquare,setEntropkiWhite,setEntropkiBlack,setEntropkiWhiteArray,setEntropkiBlackArray,setEntropkiArray,setParityDotWhite,setParityDotBlack,setParityDotWhiteArray,setParityDotBlackArray,setParityDotArray,setGenetic,setGeneticArray,setParitySnake,setConsecutiveChainRegion,setAntiQueenCell,setTripleTab,setSlotMachine
	
	from ._externalClues import setLittleKiller,setXSumBase,setXSum,setReverseXSum,setDoubleXSum,setXAverageBase,setXAverage,setReverseXAverage,setXKropki,setNumberedRoomBase,setNumberedRoom,setReverseNumberedRoom,setSandwichSum,setOpenfacedSandwichSum,setShortSandwichSum,setConditionalSandwichSum,setBeforeNine,setBattlefield,setPositionSum,_setDigitsInBlock,setOutside,setOutsideDiagonal,setOutsideLength,setCornerEdge,setRossini,setRossiniLength,setRossiniNegative,_applyRossiniNegative,setMaxAscendingRun,setMaxAscending,setSkyscraper,setSkyscraperSum,setNextToNine,setNextToNineSum,setMaximumRun,setMaximumTriplet,setDescriptivePair,setMinimax,setMaximin,setFullRank,setParityParty,setSumSandwich,setAscendingStarter,setFirstSeenParity,setFirstSeenEntropy,setFirstSeenModular,setPointingDifferents,setBust,setHangingSum,setHangingCount,setHangingAverage,setHangingInstance,setXOutside,setInOrder,setRayCount,setRaySum,setPotpourriNSums,setXDistance,setRCRegionSum,setRussianDollSum
	
	from ._quadConstraints import setQuadruple,setQuadrupleArray,setExclusionQuad,setExclusionQuadArray,setQuadSum,setQuadSumArray,setMaxMinQuadSum,setMaxMinQuadSumArray,setBattenburg,setBattenburgArray,setBattenburgNegative,setAntiBattenburg,setAntiBattenburgArray,_applyBattenburgNegative,setEntropyQuad,setEntropyQuadArray,setEntropyQuadNegative,setAntiEntropyQuad,setAntiEntropyQuadArray,_applyEntropyQuadNegative,setModularQuad,setModularQuadArray,setModularQuadNegative,setAntiModularQuad,setAntiModularQuadArray,_applyModularQuadNegative,_initializeParityQuad,setParityQuad,setParityQuadArray,setParityQuadNegative,setAntiParityQuad,setAntiParityQuadArray,_applyParityQuadNegative,setParityQuadExclusions,_initializeEntropyBattenburg,setEntropyBattenburg,setEntropyBattenburgArray,setAntiEntropyBattenburg,setAntiEntropyBattenburgArray,setEntropyBattenburgNegative,_applyEntropyBattenburgNegative,setQuadMaxArrow,setQuadMaxArrowArray,setQuadValueBase,setQuadMaxValue,setQuadMaxValueArray,setQuadMinValue,setQuadMinValueArray,setQuadParityValueBase,setQuadMaxParityValue,setQuadMinParityValue,setQuadParityBase,setQuadMaxParity,setQuadMinParity,setQuadMaxParityArray,setQuadMinParityArray,setConsecutiveQuad,setConsecutiveQuadWhite,setConsecutiveQuadWhiteArray,setConsecutiveQuadBlack,setConsecutiveQuadBlackArray,setConsecutiveQuadArray,setAntiConsecutiveQuad,setAntiConsecutiveQuadArray,setConsecutiveQuadNegative,_applyConsecutiveQuadNegative,setDiagonalConsecutivePairs,setDiagonalConsecutivePairsArray,_initializeClockQuadWhite,_initializeClockQuadBlack,setClockQuadWhite,setClockQuadBlack,setClockQuadGray,setClockQuadWhiteArray,setClockQuadBlackArray,setClockQuadGrayArray,setClockQuadArray,setClockQuadWhiteNegative,setClockQuadBlackNegative,setClockQuadNegative,setAntiClockQuadWhite,setAntiClockQuadBlack,setAntiClockQuad,setAntiClockQuadWhiteArray,setAntiClockQuadBlackArray,setAntiClockQuadArray,_applyClockQuadWhiteNegative,_applyClockQuadBlackNegative
	
	from ._lineConstraints import setArrow,setHeavyArrow,setDoubleArrow,setPointingArrow,setMultiDigitSumArrow,setMissingArrow,setMultiDigitSumMissingArrow,setRepeatingArrow,setThermo,setSlowThermo,setFastThermo,setOddEvenThermo,setSlowOddEvenThermo,setMissingThermo,setBrokenThermo,setDoubleThermo,setRemovedBulbThermo,setCountTheOddsLine,setKeypadKnightLine,setKeypadKingLine,setPalindromeLine,setParindromeLine,setWeakPalindromeLine,setParityLine,setRenbanLine,setRenrenbanbanLine,setNotRenbanLine,setRunOnRenbanLine,setMinWhispersLine,setMaxWhispersLine,setGermanWhispersLine,setDutchWhispersLine,setChineseWhispersLine,setMinExtendedWhispersLine,setMaxExtendedWhispersLine,setRunOnNabnerLine,setEntropicWhispersLine,setEntropicLine,setModularLine,setBetweenLine,setLockoutLine,setRegionSumLine,setRegionSegmentSumLine,setRegionometer,setDoublingLine,setShiftLine,setUpAndDownLine,setAverageLine,setNabnerLine,setParityCountLine,set10Line,setClockLine,setMagicLine,setConsecutiveLine,setZipperLine,setLineSumLine,setUniquePairsLines,setCellIndexLines,setSplitPeaLine,setSequenceLine,setIndexLine,setLotLine,setConditionalSumLine,setConditionalCountLine,setConditionalInstanceLine,_setConditionalSegment,setConditionalCountSegment,setConditionalSumSegment
	
	from ._solving import applyNegativeConstraints,findSolution,preparePrintVariables,countSolutions,printCurrentSolution,testStringSolution,listCandidates,addExcludedDigit,addExcludedDigitArray,listCellCandidates
	
	from ._utilities import _varBitmap,_procCell,_procCellList,getOrthogonalNeighbors,getRegion,_initializeDigitTracking,_setDigitTracking,_initializeDigitTrackingCell,_initializeParity,_setParity,_initializeEntropy,_setEntropy,_initializeModular,_setModular,_setFullRank,_initializePrimality,configurePrimality,_setPrimality,_initializeDigitSize,configureDigitSize,_setDigitSize,getCellVar,assertNoRoping,_selectCellsMatchDigitSet,_selectCellsOnLine,_selectCellsInRowCol,_terminateCellsOnLine,_terminateCellsInRowCol,_evaluateHangingClues