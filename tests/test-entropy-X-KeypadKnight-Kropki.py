import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Knights of the Xentropy Table
	# Author: jeremydover
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009DH
	# Constraints tested: setXSudokuMain, setXSudokuOff, setKeypadKnightLine, setKropkiBlack
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setXSudokuMain()
		p.setXSudokuOff()
		p.setGlobalEntropy()
		p.setKeypadKnightLine([11,22,33])
		p.setKeypadKnightLine([77,88,99])
		p.setKeypadKnightLine([51,52,53,43,44,54,64,74,75,85,84,94])
		p.setKeypadKnightLine([44,45,46,56,66,65,64])
		p.setKeypadKnightLine([16,26,25,35,36,46])
		p.setKeypadKnightLine([66,67,57,58,59])
		p.setKropkiBlack(311)
		
		self.assertEqual(p.countSolutions(test=True),'1:925841673148376925673529148357294816816753492492618357269185734581437269734962581','Failed Knights of the Xentropy Table')
		
if __name__ == '__main__':
    unittest.main()