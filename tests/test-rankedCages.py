import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (052) - Rank Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00023W
	# Constraints tested: setRankedCage, set GivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRankedCage([15,16,25,26,27],[(3,3),(5,1)])
		p.setRankedCage([23,33,34,43,44],[(3,4)])
		p.setRankedCage([32,41,42,51,52],[(2,2),(5,1)])
		p.setRankedCage([36,37,38,46,47],[(1,2),(2,1)])
		p.setRankedCage([58,59,68,69,78],[(1,5),(4,3)])
		p.setRankedCage([63,64,72,73,74],[(4,1),(5,4)])
		p.setRankedCage([66,67,76,77,87],[(3,4)])
		p.setRankedCage([83,84,85,94,95],[(1,4),(3,1)])
		p.setGivenArray([135,171,221,289,318,393,714,799,825,884,938,972])
		
		self.assertEqual(p.countSolutions(test=True),'1:745389162613275498892416573376148925524693781189752634461827359257931846938564217','Failed Sudoku Variants Series (052) - Rank Sudoku')
		
if __name__ == '__main__':
    unittest.main()