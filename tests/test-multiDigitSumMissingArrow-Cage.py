import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (369) - Killer - Hidden Arrows Sudoku
	# Author: Richard
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009T8
	# Constraints tested: setMultiDigitSumMissingArrow, setCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		for x in [([12,11,21],16),([16,26,27,37,38,48],32),([23,22,32],18),([24,34,33,43,42],28),([35,45,44,54,53],29),([46,56,66,65,64],23),([61,62,72,73,83,84],30),([67,77,76],8)]:
			p.setCage(x[0],x[1])
			p.setMultiDigitSumMissingArrow(x[0])
		
		self.assertEqual(p.countSolutions(test=True),'1:384517296579246813126389457698473521731925648245168379963754182417832965852691734','Failed Sudoku Variants Series (369) - Killer - Hidden Arrows Sudoku')
		
if __name__ == '__main__':
    unittest.main()