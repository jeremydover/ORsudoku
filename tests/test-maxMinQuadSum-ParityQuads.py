import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (330) - HiLo Parity Sums Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00070R
	# Constraints tested: setParityQuadExclusions, setParityQuadArray, setParityQuadNegative,setMaxMinQuadSumArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setParityQuadExclusions([0,1,3,4])
		p.setParityQuadArray([24,27,28,32,35,38,41,43,44,45,46,51,55,57,58,66,68,72,75,76,77,78,81,82,84])
		p.setParityQuadNegative()
		p.setMaxMinQuadSumArray([2412,279,2812,325,3511,389,418,4311,4413,4512,4612,5111,5510,579,587,6610,6813,728,7511,7613,7713,7815,8110,8211,847])
		
		self.assertEqual(p.countSolutions(test=True),'1:158274639746931285932865174614783952275496813893512746461328597327159468589647321','Failed Sudoku Variants Series (330) - HiLo Parity Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()