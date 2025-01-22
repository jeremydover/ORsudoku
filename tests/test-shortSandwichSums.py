import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (381) - Short Sandwiches Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000AYG
	# Constraints tested: setShortSandwichSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setShortSandwichSum(1,1,p.Col,10)
		p.setShortSandwichSum(1,2,p.Col,0)
		p.setShortSandwichSum(1,6,p.Col,3)
		p.setShortSandwichSum(1,9,p.Col,14)
		
		p.setShortSandwichSum(3,9,p.Row,25)
		p.setShortSandwichSum(6,9,p.Row,19)
		p.setShortSandwichSum(7,9,p.Row,8)
		p.setShortSandwichSum(8,9,p.Row,12)
		
		p.setShortSandwichSum(9,1,p.Col,20)
		p.setShortSandwichSum(9,4,p.Col,10)
		p.setShortSandwichSum(9,8,p.Col,0)
		p.setShortSandwichSum(9,9,p.Col,2)
		
		p.setShortSandwichSum(3,1,p.Row,17)
		p.setShortSandwichSum(4,1,p.Row,10)
		p.setShortSandwichSum(7,1,p.Row,19)
			
		self.assertEqual(p.countSolutions(test=True),'1:684591327279463815153278649392814576745632198861957432538749261916325784427186953','Failed Sudoku Variants Series (381) - Short Sandwiches Sudoku')
		
if __name__ == '__main__':
    unittest.main()