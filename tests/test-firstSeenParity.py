import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: First Seen Odd Even Sudoku
	# Author: Realshaggy
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00032V
	# Constraints tested: setFirstSeenParity
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setFirstSeenParity(1,1,p.Row,7)
		p.setFirstSeenParity(2,1,p.Row,3)
		p.setFirstSeenParity(3,1,p.Row,5)
		p.setFirstSeenParity(4,1,p.Row,1)
		p.setFirstSeenParity(5,1,p.Row,7)
		p.setFirstSeenParity(6,1,p.Row,5)
		p.setFirstSeenParity(7,1,p.Row,3)
		p.setFirstSeenParity(8,1,p.Row,9)
		p.setFirstSeenParity(9,1,p.Row,3)
		
		p.setFirstSeenParity(1,1,p.Col,1)
		p.setFirstSeenParity(1,2,p.Col,4)
		p.setFirstSeenParity(1,3,p.Col,7)
		p.setFirstSeenParity(1,4,p.Col,3)
		p.setFirstSeenParity(1,5,p.Col,1)
		p.setFirstSeenParity(1,6,p.Col,9)
		p.setFirstSeenParity(1,7,p.Col,2)
		p.setFirstSeenParity(1,9,p.Col,4)
		
		p.setFirstSeenParity(1,9,p.Row,1)
		p.setFirstSeenParity(2,9,p.Row,7)
		p.setFirstSeenParity(3,9,p.Row,2)
		p.setFirstSeenParity(6,9,p.Row,3)
		p.setFirstSeenParity(7,9,p.Row,4)
		p.setFirstSeenParity(9,9,p.Row,8)
		
		p.setFirstSeenParity(9,2,p.Col,7)
		p.setFirstSeenParity(9,4,p.Col,7)
		p.setFirstSeenParity(9,5,p.Col,8)
		p.setFirstSeenParity(9,7,p.Col,6)
		p.setFirstSeenParity(9,8,p.Col,2)
		p.setFirstSeenParity(9,9,p.Col,6)
		
		self.assertEqual(p.countSolutions(test=True),'1:647329581239518764851674392163945278782163459594782136315296847978451623426837915','Failed First Seen Odd Even Sudoku')
		
if __name__ == '__main__':
    unittest.main()