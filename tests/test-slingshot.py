import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Slingshot Sudoku
	# Author: stephane.bura
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0003XC
	# Constraints tested: setSlingshot
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSlingshot(1,7,p.Right,p.Down)
		p.setSlingshot(2,5,p.Down,p.Right)
		p.setSlingshot(3,6,p.Left,p.Down)
		p.setSlingshot(4,1,p.Right,p.Up)
		p.setSlingshot(4,2,p.Right,p.Down)
		p.setSlingshot(4,3,p.Right,p.Up)
		p.setSlingshot(4,4,p.Right,p.Down)
		p.setSlingshot(4,6,p.Left,p.Up)
		p.setSlingshot(5,1,p.Down,p.Right)
		p.setSlingshot(5,3,p.Left,p.Up)
		p.setSlingshot(5,5,p.Up,p.Right)
		p.setSlingshot(6,1,p.Up,p.Right)
		p.setSlingshot(6,3,p.Up,p.Right)
		p.setSlingshot(8,3,p.Right,p.Down)
		p.setSlingshot(8,7,p.Down,p.Left)
		p.setSlingshot(9,1,p.Right,p.Up)
		p.setSlingshot(9,2,p.Right,p.Up)
		p.setSlingshot(9,4,p.Left,p.Up)
		p.setSlingshot(9,5,p.Left,p.Up)
		p.setSlingshot(9,6,p.Left,p.Up)
		p.setSlingshot(9,7,p.Left,p.Up)
		p.setSlingshot(9,8,p.Left,p.Up)
		p.setSlingshot(9,9,p.Left,p.Up)
		
		self.assertEqual(p.countSolutions(test=True),'1:914675823368249571527813946153492768872536194496781352685327419241958637739164285','Failed Slingshot Sudoku')
		
if __name__ == '__main__':
    unittest.main()