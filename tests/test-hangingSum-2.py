import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: DSM Qualitraining 2021: Parity Party Sudoku
	# Author: Realshaggy
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000566
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,2,p.Col,14,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(1,4,p.Col,12,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(1,6,p.Col,18,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(1,8,p.Col,16,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		
		p.setHangingSum(2,9,p.Row,6,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(4,9,p.Row,12,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(6,9,p.Row,20,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(8,9,p.Row,5,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		
		p.setHangingSum(9,2,p.Col,15,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(9,4,p.Col,12,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(9,6,p.Col,14,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(9,8,p.Col,8,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		
		p.setHangingSum(2,1,p.Row,20,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(4,1,p.Row,12,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(6,1,p.Row,16,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
		p.setHangingSum(8,1,p.Row,15,[['All']],[('Fixed',1),('DigitSetReached',[2,4,6,8],1),('DigitSetReached',[1,3,5,7,9],1)],terminateOn='Any')
			
		self.assertEqual(p.countSolutions(test=True),'1:672543198938127456541698327354876219827915634196432875719284563285369741463751982','Failed DSM Qualitraining 2021: Parity Party Sudoku')
		
if __name__ == '__main__':
    unittest.main()