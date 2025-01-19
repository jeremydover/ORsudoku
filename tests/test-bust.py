import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Bust Sudoku
	# Author: clover!
	# https://sudokupad.app/8blilv1wly
	# Constraints tested: setBust, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setBust(1,1,p.Row,7)
		p.setBust(4,1,p.Row,7)
		p.setBust(7,1,p.Row,7)
		p.setBust(3,9,p.Row,7)
		p.setBust(6,9,p.Row,7)
		p.setBust(9,9,p.Row,7)
		p.setBust(1,7,p.Col,4)
		p.setBust(1,8,p.Col,4)
		p.setBust(1,9,p.Col,4)
		p.setBust(9,2,p.Col,4)
		p.setBust(9,3,p.Col,4)
		p.setBust(9,4,p.Col,4)
		p.setGivenArray([134,179,248,282,317,371,443,465,535,576,644,661,732,797,821,869,938,973])
		
		self.assertEqual(p.countSolutions(test=True),'1:524136978163897524789254163641325789235978641897461235452613897316789452978542316','Failed Bust Sudoku')
		
if __name__ == '__main__':
    unittest.main()