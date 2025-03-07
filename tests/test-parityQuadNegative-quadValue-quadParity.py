import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (359) - Sudoku HiLo Odd-Even
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00092U
	# Constraints tested: setParityQuadExclusions, setParityQuadArray, setParityQuadNegative, setQuadMaxValueArray, setQuadMinValueArray, setQuadMaxParityArray, setQuadMinParityArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setParityQuadExclusions([0,1,3,4])
		p.setParityQuadArray([14,17,25,28,33,36,37,43,44,45,55,57,64,71,72,74,77,78,81,84,86])
		p.setParityQuadNegative()
		
		p.setQuadMaxValueArray([149,258,436,459,559,645,718,749,779,819,849])
		p.setQuadMinValueArray([146,251,431,454,552,642,711,742,772,811,842])
		
		p.setQuadMaxParityArray([171,280,331,360,370,441,571,721,780,860])
		p.setQuadMinParityArray([171,280,331,360,370,441,571,721,780,860])
			
		self.assertEqual(p.countSolutions(test=True),'1:258764391371982645694513287462178539583649172719325468837451926146297853925836714','Failed Sudoku Variants Series (359) - Sudoku HiLo Odd-Even')
		
if __name__ == '__main__':
    unittest.main()