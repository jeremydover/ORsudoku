import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (237) - Before 1 - After 9 Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002VQ
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,1,p.Col,11,[['All']],[['DigitReached',1]],includeTerminator=False)
		p.setHangingSum(1,4,p.Col,27,[['All']],[['DigitReached',1]],includeTerminator=False)
		p.setHangingSum(1,5,p.Col,30,[['All']],[['DigitReached',1]],includeTerminator=False)
		p.setHangingSum(1,8,p.Col,22,[['All']],[['DigitReached',1]],includeTerminator=False)
		
		p.setHangingSum(1,1,p.Row,24,[['All']],[['DigitReached',1]],includeTerminator=False)
		p.setHangingSum(4,1,p.Row,42,[['All']],[['DigitReached',1]],includeTerminator=False)
		p.setHangingSum(5,1,p.Row,9,[['All']],[['DigitReached',1]],includeTerminator=False)
		p.setHangingSum(8,1,p.Row,5,[['All']],[['DigitReached',1]],includeTerminator=False)
		p.setHangingSum(9,1,p.Row,35,[['All']],[['DigitReached',1]],includeTerminator=False)
		
		p.setHangingSum(9,3,p.Col,13,[['All']],[['DigitReached',9]],includeTerminator=False)
		p.setHangingSum(9,5,p.Col,26,[['All']],[['DigitReached',9]],includeTerminator=False)
		p.setHangingSum(9,7,p.Col,26,[['All']],[['DigitReached',9]],includeTerminator=False)
		p.setHangingSum(9,9,p.Col,5,[['All']],[['DigitReached',9]],includeTerminator=False)
		
		p.setHangingSum(3,9,p.Row,22,[['All']],[['DigitReached',9]],includeTerminator=False)
		p.setHangingSum(5,9,p.Row,15,[['All']],[['DigitReached',9]],includeTerminator=False)
		p.setHangingSum(6,9,p.Row,24,[['All']],[['DigitReached',9]],includeTerminator=False)
		p.setHangingSum(9,9,p.Row,18,[['All']],[['DigitReached',9]],includeTerminator=False)
		
		self.assertEqual(p.countSolutions(test=True),'1:456271398798435261123896574635748912271659483849123756962514837514387629387962145','Failed Sudoku Variants Series (237) - Before 1 - After 9 Sudoku')
		
if __name__ == '__main__':
    unittest.main()