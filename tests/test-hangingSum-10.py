import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (296) - Flexible Sandwich Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0004S7
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,2,p.Col,21,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		p.setHangingSum(1,3,p.Col,39,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		p.setHangingSum(1,7,p.Col,5,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		
		p.setHangingSum(5,9,p.Row,21,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		p.setHangingSum(7,9,p.Row,13,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		p.setHangingSum(8,9,p.Row,19,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		
		p.setHangingSum(9,2,p.Col,4,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		p.setHangingSum(9,3,p.Col,16,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		p.setHangingSum(9,4,p.Col,14,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		p.setHangingSum(9,9,p.Col,18,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		
		p.setHangingSum(3,1,p.Row,15,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		p.setHangingSum(7,1,p.Row,23,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		p.setHangingSum(8,1,p.Row,17,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		p.setHangingSum(9,1,p.Row,10,[('Location',p.GE,2)],[('RelatedDigit',1,p.EQ,1,1,1)],includeTerminator=False)
		
		self.assertEqual(p.countSolutions(test=True),'1:421963785398751462756482193217645839864329571935178246689517324542836917173294658','Failed Sudoku Variants Series (296) - Flexible Sandwich Sudoku')
		
if __name__ == '__main__':
    unittest.main()