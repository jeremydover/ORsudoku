import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Prime Party
	# Author: Realshaggy
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000BBL
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,2,p.Col,16,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(1,4,p.Col,11,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(1,6,p.Col,15,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(1,8,p.Col,22,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		
		p.setHangingSum(2,9,p.Row,15,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(4,9,p.Row,28,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(6,9,p.Row,16,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(8,9,p.Row,14,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		
		p.setHangingSum(9,1,p.Col,18,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(9,4,p.Col,28,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(9,6,p.Col,11,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(9,8,p.Col,22,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		
		p.setHangingSum(2,1,p.Row,8,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(4,1,p.Row,10,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(6,1,p.Row,28,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
		p.setHangingSum(8,1,p.Row,19,[],[('Fixed',1),('DigitSetReached',[2,3,5,7],1),('DigitSetReached',[1,4,6,8,9],1)],terminateOnFirst=False)
			
		self.assertEqual(p.countSolutions(test=True),'1:158674329624539178793182654271345986365298417849716235537961842982453761416827593','Failed Prime Party')
		
if __name__ == '__main__':
    unittest.main()