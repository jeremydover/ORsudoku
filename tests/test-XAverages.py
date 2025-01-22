import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (397) - X-Sums - average
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000CBC
	# Constraints tested: setXAverage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setXAverage(1,1,p.Col,7)
		p.setXAverage(1,3,p.Col,4)
		p.setXAverage(1,5,p.Col,3)
		p.setXAverage(1,6,p.Col,7)
		p.setXAverage(3,9,p.Row,4)
		p.setXAverage(7,9,p.Row,5)
		p.setXAverage(9,9,p.Col,2)
		p.setXAverage(9,7,p.Col,6)
		p.setXAverage(9,5,p.Col,3)
		p.setXAverage(9,4,p.Col,5)
		p.setXAverage(7,1,p.Row,4)
		p.setXAverage(5,1,p.Row,5)
		p.setXAverage(3,1,p.Row,6)
			
		self.assertEqual(p.countSolutions(test=True),'1:527634819943218756681957324715369248896472135432185967354791682269843571178526493','Failed Sudoku Variants Series (397) - X-Sums - average')
		
if __name__ == '__main__':
    unittest.main()