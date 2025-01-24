import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (364) - Neighbour Sets Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009FU
	# Constraints tested: setPosNeighborSetArray, setNeighborSetNegative, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setPosNeighborSetArray([11,12,23,24,25,28,31,35,38,39,41,44,45,46,47,49,51,53,54,56,58,63,66,68,74,79,84,85,89,91,92,95])
		p.setNeighborSetNegative()
		p.setGivenArray([221,292,554,689,779,815,868])
		
		self.assertEqual(p.countSolutions(test=True),'1:784362519619875342253491768195286437367149285428537691841753926536928174972614853','Failed Sudoku Variants Series (364) - Neighbour Sets Sudoku')
		
if __name__ == '__main__':
    unittest.main()