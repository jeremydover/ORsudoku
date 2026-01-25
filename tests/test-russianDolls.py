import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (451) - Russian Doll Sums
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000Q85
	# Constraints tested: setRussianDollSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRussianDollSum(1,1,p.Row,[5,16])
		p.setRussianDollSum(3,1,p.Row,[11,11])
		p.setRussianDollSum(5,1,p.Row,[10,12])
		p.setRussianDollSum(7,1,p.Row,[10,12])
		p.setRussianDollSum(8,1,p.Row,6)
		p.setRussianDollSum(9,1,p.Row,5)
		p.setRussianDollSum(1,1,p.Col,3)
		p.setRussianDollSum(1,2,p.Col,5)
		p.setRussianDollSum(1,8,p.Col,8)
		p.setRussianDollSum(1,9,p.Col,[13,9])
		
		self.assertEqual(p.countSolutions(test=True),'1:451378269672954318983216475597631824264897531318542697126489753839725146745163982','Failed Sudoku Variants Series (451) - Russian Doll Sums')
		
if __name__ == '__main__':
    unittest.main()