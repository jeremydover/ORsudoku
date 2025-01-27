import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (336) - Remote Clones Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0007GV
	# Constraints tested: setRemoteClone
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRemoteClone(1,7,p.Left,p.Down)
		p.setRemoteClone(2,4,p.Left,p.Down)
		p.setRemoteClone(2,7,p.Left,p.Down)
		p.setRemoteClone(2,8,p.Left,p.Down)
		p.setRemoteClone(3,7,p.Right,p.Down)
		p.setRemoteClone(4,3,p.Right,p.Down)
		p.setRemoteClone(4,4,p.Right,p.Down)
		p.setRemoteClone(4,6,p.Right,p.Up)
		p.setRemoteClone(4,8,p.Left,p.Down)
		p.setRemoteClone(5,4,p.Right,p.Up)
		p.setRemoteClone(5,5,p.Right,p.Up)
		p.setRemoteClone(5,7,p.Right,p.Up)
		p.setRemoteClone(6,9,p.Left,p.Down)
		p.setRemoteClone(8,5,p.Right,p.Up)
		p.setRemoteClone(9,5,p.Left,p.Up)
		p.setRemoteClone(9,7,p.Left,p.Up)
		p.setRemoteClone(9,9,p.Left,p.Up)
		
		self.assertEqual(p.countSolutions(test=True),'1:784913625156284379329675184931562847865347291247198563618459732473821956592736418','Failed Sudoku Variants Series (336) - Remote Clones Sudoku')
		
if __name__ == '__main__':
    unittest.main()