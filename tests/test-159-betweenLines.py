import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Fishie
	# Author: zetamath
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0007IX
	# Constraints tested: setIndexing, setBetweenLines
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setIndexColumn(1)
		p.setIndexColumn(5)
		p.setIndexColumn(9)
		p.setBetweenLine([13,23,33,43])
		p.setBetweenLine([31,41,51,61,62,53])
		p.setBetweenLine([38,49,59,69,78])
		p.setBetweenLine([54,45,36,47,58])
		p.setBetweenLine([54,65,76,67,58])
		p.setBetweenLine([74,84,94,93])
		
		self.assertEqual(p.findSolution(test=True),'684271539215936874937854621859627413462183957371549286546312798723498165198765342','Failed Fishie')
		
if __name__ == '__main__':
    unittest.main()