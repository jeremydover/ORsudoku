import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (361) - Sum Sum Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00098T
	# Constraints tested: setEqualSumCages, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		for n in range(1,10):
			p.setEqualSumCages([[(n,1),(n,2)],[(8,n),(9,n)]])
		p.setGivenArray([121,165,239,283,343,377,457,492,564,642,678,738,782,899])
			
		self.assertEqual(p.countSolutions(test=True),'1:713945268859726134426381795941678352285134976637259841198463527362517489574892613','Failed Sudoku Variants Series (361) - Sum Sum Sudoku')
		
if __name__ == '__main__':
    unittest.main()