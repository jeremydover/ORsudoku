import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (119) - Even-Odd Japanese Sums Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002DP
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,1,p.Col,2,[('Parity',p.EQ,0)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,1,p.Col,8,[('Parity',p.EQ,0)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,1,p.Col,20,[('Parity',p.EQ,0)],[['ParityChangeReached',6],['Last']])
		p.setHangingSum(1,2,p.Col,10,[('Parity',p.EQ,0)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,2,p.Col,20,[('Parity',p.EQ,0)],[('ParityChangeReached',4),['Last']])
		p.setHangingSum(1,3,p.Col,8,[('Parity',p.EQ,0)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,3,p.Col,14,[('Parity',p.EQ,0)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,3,p.Col,20,[('Parity',p.EQ,0)],[['ParityChangeReached',6],['Last']])
		p.setHangingSum(1,4,p.Col,8,[('Parity',p.EQ,0)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,4,p.Col,14,[('Parity',p.EQ,0)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,4,p.Col,20,[('Parity',p.EQ,0)],[['ParityChangeReached',6],['Last']])
		p.setHangingSum(1,5,p.Col,6,[('Parity',p.EQ,0)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,5,p.Col,8,[('Parity',p.EQ,0)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,5,p.Col,20,[('Parity',p.EQ,0)],[['ParityChangeReached',6],['Last']])
		p.setHangingSum(1,6,p.Col,4,[('Parity',p.EQ,0)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,6,p.Col,18,[('Parity',p.EQ,0)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,6,p.Col,20,[('Parity',p.EQ,0)],[['ParityChangeReached',6],['Last']])
		p.setHangingSum(1,7,p.Col,6,[('Parity',p.EQ,0)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,7,p.Col,14,[('Parity',p.EQ,0)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,7,p.Col,18,[('Parity',p.EQ,0)],[('ParityChangeReached',6)],includeTerminator=False)
		p.setHangingSum(1,7,p.Col,20,[('Parity',p.EQ,0)],[('ParityChangeReached',8),['Last']])
		p.setHangingSum(1,8,p.Col,2,[('Parity',p.EQ,0)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,8,p.Col,8,[('Parity',p.EQ,0)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,8,p.Col,16,[('Parity',p.EQ,0)],[('ParityChangeReached',6)],includeTerminator=False)
		p.setHangingSum(1,8,p.Col,20,[('Parity',p.EQ,0)],[('ParityChangeReached',8),['Last']])
		p.setHangingSum(1,9,p.Col,4,[('Parity',p.EQ,0)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,9,p.Col,12,[('Parity',p.EQ,0)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(1,9,p.Col,14,[('Parity',p.EQ,0)],[('ParityChangeReached',6)],includeTerminator=False)
		p.setHangingSum(1,9,p.Col,20,[('Parity',p.EQ,0)],[('ParityChangeReached',8),['Last']])
	
		p.setHangingSum(1,1,p.Row,17,[('Parity',p.EQ,1)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(1,1,p.Row,25,[('Parity',p.EQ,1)],[('ParityChangeReached',4),['Last']])
		p.setHangingSum(2,1,p.Row,1,[('Parity',p.EQ,1)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(2,1,p.Row,25,[('Parity',p.EQ,1)],[('ParityChangeReached',4),['Last']])
		p.setHangingSum(3,1,p.Row,3,[('Parity',p.EQ,1)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(3,1,p.Row,8,[('Parity',p.EQ,1)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(3,1,p.Row,15,[('Parity',p.EQ,1)],[('ParityChangeReached',6)],includeTerminator=False)
		p.setHangingSum(3,1,p.Row,25,[('Parity',p.EQ,1)],[('ParityChangeReached',8),['Last']])
		p.setHangingSum(4,1,p.Row,15,[('Parity',p.EQ,1)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(4,1,p.Row,18,[('Parity',p.EQ,1)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(4,1,p.Row,25,[('Parity',p.EQ,1)],[('ParityChangeReached',6),['Last']])
		p.setHangingSum(5,1,p.Row,3,[('Parity',p.EQ,1)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(5,1,p.Row,11,[('Parity',p.EQ,1)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(5,1,p.Row,25,[('Parity',p.EQ,1)],[('ParityChangeReached',6),['Last']])
		p.setHangingSum(6,1,p.Row,7,[('Parity',p.EQ,1)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(6,1,p.Row,21,[('Parity',p.EQ,1)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(6,1,p.Row,25,[('Parity',p.EQ,1)],[('ParityChangeReached',6),['Last']])
		p.setHangingSum(7,1,p.Row,5,[('Parity',p.EQ,1)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(7,1,p.Row,14,[('Parity',p.EQ,1)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(7,1,p.Row,22,[('Parity',p.EQ,1)],[('ParityChangeReached',6)],includeTerminator=False)
		p.setHangingSum(7,1,p.Row,25,[('Parity',p.EQ,1)],[('ParityChangeReached',8),['Last']])
		p.setHangingSum(8,1,p.Row,13,[('Parity',p.EQ,1)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(8,1,p.Row,25,[('Parity',p.EQ,1)],[('ParityChangeReached',4),['Last']])
		p.setHangingSum(9,1,p.Row,7,[('Parity',p.EQ,1)],[('ParityChangeReached',2)],includeTerminator=False)
		p.setHangingSum(9,1,p.Row,16,[('Parity',p.EQ,1)],[('ParityChangeReached',4)],includeTerminator=False)
		p.setHangingSum(9,1,p.Row,25,[('Parity',p.EQ,1)],[('ParityChangeReached',6),['Last']])
			
		self.assertEqual(p.countSolutions(test=True),'1:197835624248169375365274918951423867634718592782596431529647183413982756876351249','Failed Sudoku Variants Series (119) - Even-Odd Japanese Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()