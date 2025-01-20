import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Submarine
	# Author: grkles?
	# https://f-puzzles.com/?id=25qy9dsk
	# Constraints tested: setMinimax, setSandwichSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setMinimax(1,1,p.Col,7)
		p.setMinimax(1,2,p.Col,13)
		p.setMinimax(1,8,p.Col,8)
		p.setMinimax(1,9,p.Col,14)
		p.setMinimax(1,1,p.Row,15)
		p.setMinimax(2,1,p.Row,9)
		p.setMinimax(4,1,p.Row,9)
		p.setMinimax(7,1,p.Row,12)
		p.setMinimax(8,1,p.Row,13)
		p.setMinimax(6,9,p.Row,11)
		
		p.setSandwichSum(1,1,p.Col,7)
		p.setSandwichSum(1,2,p.Col,13)
		p.setSandwichSum(1,8,p.Col,8)
		p.setSandwichSum(1,9,p.Col,14)
		p.setSandwichSum(1,1,p.Row,15)
		p.setSandwichSum(2,1,p.Row,9)
		p.setSandwichSum(4,1,p.Row,9)
		p.setSandwichSum(7,1,p.Row,12)
		p.setSandwichSum(8,1,p.Row,13)
		p.setSandwichSum(6,1,p.Row,11)
		
		self.assertEqual(p.countSolutions(test=True),'1:698712435372945168145386729726894513913527684854163297567239841489671352231458976','Failed Submarine')
		
if __name__ == '__main__':
    unittest.main()