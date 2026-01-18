import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (441) - Hot Potato
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000P0D
	# Constraints tested: setCage, setDigitComparison
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCage([11,21,31],11)
		p.setCage([22,32,42,33],18)
		p.setDigitComparison([11,21,31],[22,32,42,33],p.GE,1)
		p.setCage([34,35],8)
		p.setDigitComparison([34,35],[22,32,42,33],p.GE,1)
		p.setDigitComparison([34,35],[25,26,27],p.GE,1)
		p.setDigitComparison([25,26,27],[17,18,19],p.GE,1)
		p.setCage([29,39,49],12)
		p.setDigitComparison([17,18,19],[29,39,49],p.GE,1)
		p.setCage([38,48],13)
		p.setDigitComparison([38,48],[29,39,49],p.GE,1)
		p.setCage([37,47],7)
		p.setDigitComparison([38,48],[37,47],p.GE,1)
		p.setDigitComparison([25,26,27],[37,47],p.GE,1)
		p.setDigitComparison([34,35],[45,55,65],p.GE,1)
		p.setCage([75,76],8)
		p.setDigitComparison([75,76],[45,55,65],p.GE,1)
		p.setCage([68,77,78,88],23)
		p.setDigitComparison([75,76],[68,77,78,88],p.GE,1)
		p.setCage([79,89,99],23)
		p.setDigitComparison([79,89,99],[68,77,78,88],p.GE,1)
		p.setCage([83,84,85],15)
		p.setDigitComparison([75,76],[83,84,85],p.GE,1)
		p.setCage([63,73],12)
		p.setDigitComparison([63,73],[83,84,85],p.GE,1)
		p.setCage([62,72],15)
		p.setDigitComparison([63,73],[62,72],p.GE,1)
		p.setCage([61,71,81],15)
		p.setDigitComparison([61,71,81],[62,72],p.GE,1)
		p.setDigitComparison([61,71,81],[91,92,93],p.GE,1)
		p.setDigitComparison([83,84,85],[91,92,93],p.GE,1)
		
		self.assertEqual(p.countSolutions(test=True),'1:865217934137496582249358167421985673693721845578634291384162759716549328952873416','Failed Sudoku Variants Series (441) - Hot Potato')
		
if __name__ == '__main__':
    unittest.main()