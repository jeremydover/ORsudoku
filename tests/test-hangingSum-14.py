import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (091) - Inner Frame
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002AC
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,1,p.Col,16,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(1,2,p.Col,19,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(1,3,p.Col,7,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(1,4,p.Col,20,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(1,5,p.Col,9,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(1,6,p.Col,15,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(1,7,p.Col,19,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(1,8,p.Col,9,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(1,9,p.Col,21,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		
		p.setHangingSum(1,9,p.Row,17,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(2,9,p.Row,12,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(3,9,p.Row,12,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(4,9,p.Row,19,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(5,9,p.Row,22,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(6,9,p.Row,7,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(7,9,p.Row,16,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(8,9,p.Row,17,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(9,9,p.Row,13,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		
		p.setHangingSum(9,1,p.Col,21,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(9,2,p.Col,13,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(9,3,p.Col,22,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(9,4,p.Col,9,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(9,5,p.Col,21,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(9,6,p.Col,10,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(9,7,p.Col,13,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(9,8,p.Col,17,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(9,9,p.Col,9,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		
		p.setHangingSum(1,1,p.Row,20,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(2,1,p.Row,18,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(3,1,p.Row,13,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(4,1,p.Row,15,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(5,1,p.Row,12,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(6,1,p.Row,20,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(7,1,p.Row,8,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(8,1,p.Row,16,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		p.setHangingSum(9,1,p.Row,13,[['Location',p.GE,2],['Location',p.LE,4]],[['Last']])
		
		self.assertEqual(p.countSolutions(test=True),'1:583924761791836245642751839364518927127349586859672413915283674478165392236497158','Failed Sudoku Variants Series (091) - Inner Frame')
		
if __name__ == '__main__':
    unittest.main()