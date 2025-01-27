import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (326) - Odd-Even Sandwich Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0006QP
	# Constraints tested: setConditionalSandwichSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setConditionalSandwichSum(1,1,p.Col,7,[2,8],[('Parity',p.EQ,p.Odd)])
		p.setConditionalSandwichSum(1,2,p.Col,18,[2,8],[('Parity',p.EQ,p.Odd)])
		p.setConditionalSandwichSum(1,5,p.Col,11,[2,8],[('Parity',p.EQ,p.Odd)])
		p.setConditionalSandwichSum(1,6,p.Col,9,[2,8],[('Parity',p.EQ,p.Odd)])
		p.setConditionalSandwichSum(1,8,p.Col,10,[2,8],[('Parity',p.EQ,p.Odd)])
		p.setConditionalSandwichSum(1,9,p.Col,3,[2,8],[('Parity',p.EQ,p.Odd)])
		
		p.setConditionalSandwichSum(1,1,p.Row,21,[2,8],[('Parity',p.EQ,p.Odd)])
		p.setConditionalSandwichSum(2,1,p.Row,25,[2,8],[('Parity',p.EQ,p.Odd)])
		p.setConditionalSandwichSum(3,1,p.Row,0,[2,8],[('Parity',p.EQ,p.Odd)])
		p.setConditionalSandwichSum(4,1,p.Row,6,[2,8],[('Parity',p.EQ,p.Odd)])
		p.setConditionalSandwichSum(5,1,p.Row,9,[2,8],[('Parity',p.EQ,p.Odd)])
		p.setConditionalSandwichSum(7,1,p.Row,13,[2,8],[('Parity',p.EQ,p.Odd)])
		
		p.setConditionalSandwichSum(1,9,p.Row,18,[1,9],[('Parity',p.EQ,p.Even)])
		p.setConditionalSandwichSum(2,9,p.Row,10,[1,9],[('Parity',p.EQ,p.Even)])
		p.setConditionalSandwichSum(3,9,p.Row,20,[1,9],[('Parity',p.EQ,p.Even)])
		p.setConditionalSandwichSum(7,9,p.Row,0,[1,9],[('Parity',p.EQ,p.Even)])
		
		p.setConditionalSandwichSum(9,1,p.Col,10,[1,9],[('Parity',p.EQ,p.Even)])
		p.setConditionalSandwichSum(9,3,p.Col,8,[1,9],[('Parity',p.EQ,p.Even)])
		p.setConditionalSandwichSum(9,8,p.Col,6,[1,9],[('Parity',p.EQ,p.Even)])
		p.setConditionalSandwichSum(9,9,p.Col,14,[1,9],[('Parity',p.EQ,p.Even)])
		
		self.assertEqual(p.countSolutions(test=True),'1:325798641894361752716524893251873964967245318438916527689132475542687139173459286','Failed Sudoku Variants Series (326) - Odd-Even Sandwich Sudoku')
		
if __name__ == '__main__':
    unittest.main()