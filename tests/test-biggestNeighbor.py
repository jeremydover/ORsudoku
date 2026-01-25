import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (366) - Biggest Neighbour Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009MW
	# Constraints tested: setBiggestNeighbor
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setBiggestNeighbor(1,3,p.Right)
		p.setBiggestNeighbor(1,5,p.Left)
		p.setBiggestNeighbor(1,9,p.Left)
		p.setBiggestNeighbor(2,4,p.Down)
		p.setBiggestNeighbor(2,6,p.Up)
		p.setBiggestNeighbor(2,8,p.Left)
		p.setBiggestNeighbor(3,1,p.Up)
		p.setBiggestNeighbor(3,3,p.Left)
		p.setBiggestNeighbor(3,9,p.Left)
		p.setBiggestNeighbor(4,6,p.Up)
		p.setBiggestNeighbor(5,2,p.Down)
		p.setBiggestNeighbor(5,6,p.Left)
		p.setBiggestNeighbor(5,8,p.Left)
		p.setBiggestNeighbor(7,1,p.Down)
		p.setBiggestNeighbor(7,7,p.Up)
		p.setBiggestNeighbor(8,3,p.Left)
		p.setBiggestNeighbor(8,4,p.Up)
		p.setBiggestNeighbor(8,6,p.Down)
		p.setBiggestNeighbor(8,7,p.Left)
		p.setBiggestNeighbor(9,3,p.Right)
		
		self.assertEqual(p.countSolutions(test=True),'1:743615928965823471281794536854937162326481795179256843438572619692148357517369284','Failed Sudoku Variants Series (366) - Biggest Neighbour Sudoku')
		
if __name__ == '__main__':
    unittest.main()