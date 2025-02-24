import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (272) - Parity Parade Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0003LP
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,1,p.Col,10,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(1,2,p.Col,11,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(1,4,p.Col,21,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(1,6,p.Col,19,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(1,7,p.Col,10,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(1,9,p.Col,7,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		
		p.setHangingSum(3,9,p.Row,15,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(5,9,p.Row,20,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(9,9,p.Row,12,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		
		p.setHangingSum(9,1,p.Col,11,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(9,3,p.Col,23,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(9,4,p.Col,20,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(9,6,p.Col,11,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(9,8,p.Col,3,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(9,9,p.Col,19,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		
		p.setHangingSum(1,1,p.Row,10,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(5,1,p.Row,18,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
		p.setHangingSum(7,1,p.Row,21,[['All']],[('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Last')
			
		self.assertEqual(p.countSolutions(test=True),'1:172895346348267591695431278821756934936124857754389162519672483463518729287943615','Failed Sudoku Variants Series (272) - Parity Parade Sudoku')
		
if __name__ == '__main__':
    unittest.main()