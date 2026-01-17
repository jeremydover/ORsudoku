import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Disparity Sudoku
	# Author: WPF 2015 Round 8
	# Link: https://sudokupad.app/fgkq2dikkd
	# Constraints tested: irregular, setGivenArray, setDisparity
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3,irregular=True)
		p.setRegion([11,12,13,14,21,22,23,24,34])
		p.setRegion([15,16,25,26,27,35,36,37,47])
		p.setRegion([17,18,19,28,29,38,39,48,49])
		p.setRegion([31,32,33,41,42,43,51,52,53])
		p.setRegion([44,45,46,54,55,56,64,65,66])
		p.setRegion([57,58,59,67,68,69,77,78,79])
		p.setRegion([61,62,71,72,81,82,91,92,93])
		p.setRegion([63,73,74,75,83,84,85,94,95])
		p.setRegion([76,86,87,88,89,96,97,98,99])
		
		p.setDisparity()
		p.setGivenArray([258,267,391,492,542,555,561,619,711,849,854])
			
		self.assertEqual(p.countSolutions(test=True),'1:834612957295187436582769341713496582469251873956378124147823695321945768678534219','Failed Disparity Sudoku')
		
if __name__ == '__main__':
    unittest.main()