import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Big-Small Japanese Sums Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00031C
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.configureDigitSize('Big')
		p.setHangingSum(1,1,p.Col,5,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,1,p.Col,11,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,1,p.Col,35,[('DigitSize',p.EQ,p.Big)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
		p.setHangingSum(1,2,p.Col,9,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,2,p.Col,24,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,2,p.Col,35,[('DigitSize',p.EQ,p.Big)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
		p.setHangingSum(1,3,p.Col,15,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,3,p.Col,26,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,3,p.Col,35,[('DigitSize',p.EQ,p.Big)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
		p.setHangingSum(1,4,p.Col,14,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,4,p.Col,35,[('DigitSize',p.EQ,p.Big)],[['DigitSizeChangeReached',4],['Last']],terminateOn='First')
		p.setHangingSum(1,5,p.Col,21,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,5,p.Col,26,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,5,p.Col,35,[('DigitSize',p.EQ,p.Big)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
		p.setHangingSum(1,6,p.Col,15,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,6,p.Col,30,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,6,p.Col,35,[('DigitSize',p.EQ,p.Big)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
		p.setHangingSum(1,7,p.Col,11,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,7,p.Col,20,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,7,p.Col,27,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',6)],includeTerminator=False)
		p.setHangingSum(1,7,p.Col,35,[('DigitSize',p.EQ,p.Big)],[['DigitSizeChangeReached',8],['Last']],terminateOn='First')
		p.setHangingSum(1,8,p.Col,8,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,8,p.Col,17,[('DigitSize',p.EQ,p.Big)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,8,p.Col,35,[('DigitSize',p.EQ,p.Big)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
		p.setHangingSum(1,9,p.Col,35,[('DigitSize',p.EQ,p.Big)],[['DigitSizeChangeReached',2],['Last']],terminateOn='First')
		
		p.setHangingSum(1,1,p.Row,3,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,1,p.Row,8,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,1,p.Row,10,[('DigitSize',p.EQ,p.Small)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
		p.setHangingSum(2,1,p.Row,4,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(2,1,p.Row,6,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(2,1,p.Row,10,[('DigitSize',p.EQ,p.Small)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
		p.setHangingSum(3,1,p.Row,3,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(3,1,p.Row,10,[('DigitSize',p.EQ,p.Small)],[['DigitSizeChangeReached',4],['Last']],terminateOn='First')
		p.setHangingSum(4,1,p.Row,5,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(4,1,p.Row,10,[('DigitSize',p.EQ,p.Small)],[['DigitSizeChangeReached',4],['Last']],terminateOn='First')
		p.setHangingSum(5,1,p.Row,3,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(5,1,p.Row,6,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(5,1,p.Row,10,[('DigitSize',p.EQ,p.Small)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
		p.setHangingSum(6,1,p.Row,5,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(6,1,p.Row,10,[('DigitSize',p.EQ,p.Small)],[['DigitSizeChangeReached',4],['Last']],terminateOn='First')
		p.setHangingSum(7,1,p.Row,4,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(7,1,p.Row,10,[('DigitSize',p.EQ,p.Small)],[['DigitSizeChangeReached',4],['Last']],terminateOn='First')
		p.setHangingSum(8,1,p.Row,4,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(8,1,p.Row,7,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(8,1,p.Row,10,[('DigitSize',p.EQ,p.Small)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
		p.setHangingSum(9,1,p.Row,2,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',2)],includeTerminator=False)
		p.setHangingSum(9,1,p.Row,5,[('DigitSize',p.EQ,p.Small)],[('DigitSizeChangeReached',4)],includeTerminator=False)
		p.setHangingSum(9,1,p.Row,10,[('DigitSize',p.EQ,p.Small)],[['DigitSizeChangeReached',6],['Last']],terminateOn='First')
			
		self.assertEqual(p.countSolutions(test=True),'1:537419682498276531621583497145967328376128945982354176813642759754891263269735814','Failed Big-Small Japanese Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()