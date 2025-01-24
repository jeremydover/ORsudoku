import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Weight before Eight
	# Author: jeremydover
	# Link: https://sudokupad.app/sh8ldeh4d9
	# Constraints tested: setHangingSum, setThermo
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setThermo([55,45,35,25,15])
		p.setThermo([55,64,63,72,71])
		p.setHangingSum(9,5,p.Col,17,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(1,4,p.Col,16,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(1,6,p.Col,20,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(9,9,p.Row,20,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(7,1,p.Row,11,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(6,9,p.Row,10,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(5,1,p.Row,16,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(4,9,p.Row,16,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(3,1,p.Row,12,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(1,9,p.Row,9,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(1,8,p.Col,20,[('Parity',1)],[('DigitReached',8)])
		p.setHangingSum(1,3,p.Col,11,[('Parity',1)],[('DigitReached',8)])
			
		self.assertEqual(p.countSolutions(test=True),'1:251763894847951236693842517928136475416527389375489621764318952132695748589274163','Failed Weight before Eight')
		
if __name__ == '__main__':
    unittest.main()