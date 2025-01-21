import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (382) - Parity Lines Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000B15
	# Constraints tested: setParityCountLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setParityCountLine([12,21,31,41,42,32,23,13])
		p.setParityCountLine([33,34,24,14,15,16,25,35,36,47])
		p.setParityCountLine([17,26,27,18])
		p.setParityCountLine([37,28,19,29,39,49,38])
		p.setParityCountLine([43,44,54,64,65,55,56,66,67,58,68])
		p.setParityCountLine([45,46,57,48])
		p.setParityCountLine([59,69,79,89,99])
		p.setParityCountLine([62,61,51,52,53,63,74,75,76,85])
		p.setParityCountLine([72,73,83,84])
		p.setParityCountLine([91,81,71,82,93])
		p.setParityCountLine([95,86,77,87,97,96])
	
		self.assertEqual(p.countSolutions(test=True),'1:726594318158236947493178256865419732237685491941723865619842573584367129372951684','Failed Sudoku Variants Series (382) - Parity Lines Sudoku')
		
if __name__ == '__main__':
    unittest.main()