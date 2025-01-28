import unittest
from ORsudoku import sudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Positional X-Sums
	# Author: Richard
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000L1F
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = sudoku(3)
		p.setHangingSum(2,1,p.Row,6,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(4,1,p.Row,14,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(7,1,p.Row,10,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(8,1,p.Row,8,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		
		p.setHangingSum(1,3,p.Col,14,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(1,5,p.Col,10,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(1,7,p.Col,5,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(1,9,p.Col,10,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		
		p.setHangingSum(2,9,p.Row,5,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(3,9,p.Row,12,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(6,9,p.Row,6,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(8,9,p.Row,8,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		
		p.setHangingSum(9,1,p.Col,11,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(9,3,p.Col,14,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(9,5,p.Col,6,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
		p.setHangingSum(9,7,p.Col,13,[('Location',p.EQ,1,'Indexed',1)],[['Last']])
			
		self.assertEqual(p.countSolutions(test=True),'1:816235479574916832923874615642398157159467328738152964397581246261749583485623791','Failed Positional X-Sums')
		
if __name__ == '__main__':
    unittest.main()
	
