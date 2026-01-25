import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (425) - Up to N
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000NI1
	# Constraints tested: setOpenfacedSandwichSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setOpenfacedSandwichSum(1,1,p.Col,19,1)
		p.setOpenfacedSandwichSum(1,2,p.Col,12,2)
		p.setOpenfacedSandwichSum(1,3,p.Col,5,3)
		p.setOpenfacedSandwichSum(1,4,p.Col,8,4)
		p.setOpenfacedSandwichSum(1,6,p.Col,14,6)
		p.setOpenfacedSandwichSum(1,7,p.Col,21,7)
		p.setOpenfacedSandwichSum(1,8,p.Col,12,8)
		p.setOpenfacedSandwichSum(1,9,p.Col,32,9)
		p.setOpenfacedSandwichSum(2,1,p.Row,10,2)
		p.setOpenfacedSandwichSum(3,1,p.Row,22,3)
		p.setOpenfacedSandwichSum(4,1,p.Row,13,4)
		p.setOpenfacedSandwichSum(6,1,p.Row,14,6)
		p.setOpenfacedSandwichSum(7,1,p.Row,8,7)
		p.setOpenfacedSandwichSum(8,1,p.Row,27,8)
		p.setOpenfacedSandwichSum(9,1,p.Row,29,9)
		
		self.assertEqual(p.countSolutions(test=True),'1:845691327613275498279438516327146985184953762596827134431782659962514873758369241','Failed Sudoku Variants Series (425) - Up to N')
		
if __name__ == '__main__':
    unittest.main()