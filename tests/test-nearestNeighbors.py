import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Nearest Neighbors
	# Author: clover!
	# https://sudokupad.app/c1jh0nu5iv
	# Constraints tested: setNearestNeighbors, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([111,123,249,363,387,399,483,491,614,628,718,726,742,868,984,992])
		p.setNearestNeighbor(1,1,p.Down)
		p.setNearestNeighbor(1,2,p.Down)
		p.setNearestNeighbor(1,3,p.Right)
		p.setNearestNeighbor(1,9,[p.Down,p.Left])
		p.setNearestNeighbor(3,7,p.Down)
		p.setNearestNeighbor(3,8,p.Up)
		p.setNearestNeighbor(3,9,p.Up)
		p.setNearestNeighbor(7,1,p.Down)
		p.setNearestNeighbor(7,2,p.Down)
		p.setNearestNeighbor(7,3,p.Up)
		p.setNearestNeighbor(9,1,[p.Up,p.Right])
		p.setNearestNeighbor(9,7,[p.Up,p.Left])
		p.setNearestNeighbor(9,8,p.Up)
		p.setNearestNeighbor(9,9,p.Up)
	
		self.assertEqual(p.countSolutions(test=True),'1:139867425247951368658423179796584231321679584485312796864235917972148653513796842','Failed Nearest Neighbors')
		
if __name__ == '__main__':
    unittest.main()