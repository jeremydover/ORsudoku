import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (065) - Descriptive Pairs
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000273
	# Constraints tested: setDescriptivePair
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setDescriptivePair(1,1,p.Col,25)
		p.setDescriptivePair(1,3,p.Col,48)
		p.setDescriptivePair(1,5,p.Col,24)
		p.setDescriptivePair(1,7,p.Col,89)
		p.setDescriptivePair(1,9,p.Col,67)
		p.setDescriptivePair(9,2,p.Col,49)
		p.setDescriptivePair(9,3,p.Col,36)
		p.setDescriptivePair(9,4,p.Col,16)
		p.setDescriptivePair(9,6,p.Col,17)
		p.setDescriptivePair(9,7,p.Col,37)
		p.setDescriptivePair(9,8,p.Col,49)
		p.setDescriptivePair(9,9,p.Col,39)
		p.setDescriptivePair(1,1,p.Row,59)
		p.setDescriptivePair(2,1,p.Row,78)
		p.setDescriptivePair(3,1,p.Row,39)
		p.setDescriptivePair(4,1,p.Row,16)
		p.setDescriptivePair(7,1,p.Row,18)
		p.setDescriptivePair(9,1,p.Row,47)
		p.setDescriptivePair(1,9,p.Row,14)
		p.setDescriptivePair(2,9,p.Row,35)
		p.setDescriptivePair(3,9,p.Row,36)
		p.setDescriptivePair(4,9,p.Row,15)
		p.setDescriptivePair(5,9,p.Row,27)
		p.setDescriptivePair(6,9,p.Row,59)
		p.setDescriptivePair(8,9,p.Row,48)
		p.setDescriptivePair(9,9,p.Row,28)
			
		self.assertEqual(p.countSolutions(test=True),'1:876291543152436897439875621643729185218564379597183264385942716764318952921657438','Failed Sudoku Variants Series (065) - Descriptive Pairs')
		
if __name__ == '__main__':
    unittest.main()