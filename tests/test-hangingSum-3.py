import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Entropic Party
	# Author: Alaric Taqi A. (Crusader175)
	# Link: https://sudokupad.app/357r5hpoxo
	# Constraints tested: setHangingSum, setEntropicLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,1,p.Col,8,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		p.setHangingSum(1,2,p.Col,8,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		p.setHangingSum(1,4,p.Col,14,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		
		p.setHangingSum(1,9,p.Row,14,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		p.setHangingSum(2,9,p.Row,14,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		p.setHangingSum(6,9,p.Row,10,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		
		p.setHangingSum(9,8,p.Col,8,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		p.setHangingSum(9,9,p.Col,8,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		
		p.setHangingSum(4,1,p.Row,14,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		p.setHangingSum(8,1,p.Row,10,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		p.setHangingSum(9,1,p.Row,10,[['All']],[('Fixed',1),('EntropyChangeReached',1)],terminateOn='Any')
		
		p.setEntropicLine([13,12,11,21,31])
		p.setEntropicLine([17,18,19,29,39])
		p.setEntropicLine([71,81,91,92,93])
		p.setEntropicLine([79,89,99,98,97])
			
		self.assertEqual(p.countSolutions(test=True),'1:374592168518647923962381745123859674647123859895764231289436517451278396736915482','Failed Entropic Party')
		
if __name__ == '__main__':
    unittest.main()