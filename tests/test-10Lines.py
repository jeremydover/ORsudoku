import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: 10 Lines
	# Author: zetamath
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009MN
	# Constraints tested: set10Line
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.set10Line([13,12,11,21,31])
		p.set10Line([14,23,22,32,33,34])
		p.set10Line([15,16,26,36])
		p.set10Line([17,27,37,38,39])
		p.set10Line([44,35,46,57])
		p.set10Line([45,56,65,54,45])
		p.set10Line([63,62,61,71])
		p.set10Line([66,75,84,93])
		p.set10Line([67,68,79,78,87])
		p.set10Line([74,73,72,82])
		p.set10Line([76,86,96,95])
		
		self.assertEqual(p.countSolutions(test=True),'1:582437619136592478479168532768241953925683147341975286297354861814726395653819724','Failed 10 Lines')
		
if __name__ == '__main__':
    unittest.main()