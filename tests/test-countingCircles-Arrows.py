import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Circular Reasoning
	# Author: marty_sears
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000F0A
	# Constraints tested: setCountingCircles, setArrow
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCountingCircles([11,13,16,17,19,21,22,25,31,33,34,35,36,37,39,43,44,45,47,49,51,52,53,54,55,56,57,58,63,65,67,75,81,83,85,86,87,88,89,91,93,95,97])
		p.setArrow([16,15,14,24,23])
		p.setArrow([52,42,32])
		p.setArrow([87,77,78])
		p.setArrow([88,98,99])
		
		self.assertEqual(p.countSolutions(test=True),'1:635127849891364275724859316167942538583716492249583761372695184416238957958471623','Failed Circular Reasoning')
		
if __name__ == '__main__':
    unittest.main()