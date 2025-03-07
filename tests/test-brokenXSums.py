import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (367) - Broken X-Sums Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009P6
	# Constraints tested: setXSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setXSum(1,1,p.Col,10,broken=True)
		p.setXSum(1,6,p.Col,4,broken=True)
		p.setXSum(1,7,p.Col,28,broken=True)
		
		p.setXSum(3,9,p.Row,32,broken=True)
		p.setXSum(6,9,p.Row,18,broken=True)
		p.setXSum(7,9,p.Row,10,broken=True)
		p.setXSum(9,9,p.Row,28,broken=True)
		
		p.setXSum(9,3,p.Col,27,broken=True)
		p.setXSum(9,4,p.Col,30,broken=True)
		p.setXSum(9,9,p.Col,7,broken=True)
		
		p.setXSum(1,1,p.Row,14,broken=True)
		p.setXSum(3,1,p.Row,14,broken=True)
		p.setXSum(4,1,p.Row,34,broken=True)
		p.setXSum(7,1,p.Row,18,broken=True)
			
		self.assertEqual(p.countSolutions(test=True),'1:352461789786293415491875236865132947934756128217984563528347691649518372173629854','Failed Sudoku Variants Series (367) - Broken X-Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()