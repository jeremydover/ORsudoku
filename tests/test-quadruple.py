import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Quad-Wrangle
	# Author: jeremydover
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000HSL
	# Constraints tested: setQuadrupleArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setQuadrupleArray([1112,1234,2156,2278,3178,3223,4119,4227,1389,2337,2468,1419])
		p.setQuadrupleArray([7625,7712,7834,8618,8789,8867])
		p.setQuadrupleArray([7568,8579])
		p.setQuadrupleArray([6759,6811,5723,366,634])
		
		self.assertEqual(p.findSolution(test=True),'243915786158762349679384152832149675917653428564827931796238514481576293325491867','Failed Quad-Wrangle')
		
if __name__ == '__main__':
    unittest.main()