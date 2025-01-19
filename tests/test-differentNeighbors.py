import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Different Neighbors
	# Author: clover!
	# https://sudokupad.app/m7ky62muv1
	# Constraints tested: setDifferentNeighbors, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setDifferentNeighbors(3,3)
		p.setDifferentNeighbors(3,7)
		p.setDifferentNeighbors(7,3)
		p.setDifferentNeighbors(7,7)
		p.setGivenArray([229,238,272,283,327,333,374,386,414,455,546,563,652,691,721,734,773,789,825,836,877,888])
		
		self.assertEqual(p.countSolutions(test=True),'1:642395817198746235573812469487951623921673548365428971814567392256139784739284156','Failed Different Neighbors')
		
if __name__ == '__main__':
    unittest.main()