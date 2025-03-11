import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (311) - A-Sums Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0005NE
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		A = p.model.NewIntVar(1,9,'SumTerminator')
		p.setHangingSum(1,1,p.Col,13,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(1,3,p.Col,24,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(1,4,p.Col,10,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(1,5,p.Col,33,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(1,6,p.Col,6,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(1,8,p.Col,19,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(1,9,p.Col,13,[['All']],[('DigitReached',A)],includeTerminator=False)
		
		p.setHangingSum(1,1,p.Row,5,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(2,1,p.Row,15,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(4,1,p.Row,16,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(6,1,p.Row,31,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(7,1,p.Row,10,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(8,1,p.Row,10,[['All']],[('DigitReached',A)],includeTerminator=False)
		p.setHangingSum(9,1,p.Row,27,[['All']],[('DigitReached',A)],includeTerminator=False)
		
		self.assertEqual(p.countSolutions(test=True),'1:587196234142538769396472158475863912861925347923714586738659421214387695659241873','Failed Sudoku Variants Series (311) - A-Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()