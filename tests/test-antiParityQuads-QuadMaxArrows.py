import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (171) - Parity QuadMax Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002KB
	# Constraints tested: setParityCountLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setAntiParityQuadArray([13,26,31,33,55,62,77])
		p.setQuadMaxArrowArray([1301,2601,3100,3301,5510,6200,7700])
		p.setGivenArray([121,156,178,212,287,399,513,693,711,825,938,965,996])
	
		self.assertEqual(p.countSolutions(test=True),'1:417963825293584671865712439621348597379651284584297163146839752952476318738125946','Failed Sudoku Variants Series (171) - Parity QuadMax Sudoku')
		
if __name__ == '__main__':
    unittest.main()