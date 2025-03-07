import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (349) - X-Distance Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008FJ
	# Constraints tested: setXDistance
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setXDistance(1,1,p.Col,3,5)
		p.setXDistance(1,2,p.Col,4,9)
		p.setXDistance(1,3,p.Col,3,1)
		p.setXDistance(1,5,p.Col,1,6)
		p.setXDistance(1,6,p.Col,7,2)
		p.setXDistance(1,7,p.Col,8,4)
		p.setXDistance(1,8,p.Col,2,7)
		p.setXDistance(1,9,p.Col,2,6)
		
		p.setXDistance(1,1,p.Row,4,8)
		p.setXDistance(2,1,p.Row,8,2)
		p.setXDistance(3,1,p.Row,1,7)
		p.setXDistance(4,1,p.Row,8,2)
		p.setXDistance(6,1,p.Row,5,9)
		p.setXDistance(7,1,p.Row,8,6)
		p.setXDistance(8,1,p.Row,5,1)
		p.setXDistance(9,1,p.Row,4,1)
			
		self.assertEqual(p.countSolutions(test=True),'1:172954863349687125568123947784519632923876514615432789831745296456291378297368451','Failed Sudoku Variants Series (349) - X-Distance Sudoku')
		
if __name__ == '__main__':
    unittest.main()