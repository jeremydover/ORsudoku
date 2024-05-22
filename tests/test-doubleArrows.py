import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Target Practice
	# Author: zetamath
	# Link: https://zetamath.link/target-practice
	# Constraints tested: setDoubleArrow, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([144,417])
		p.setDoubleArrow([14,15,16,27])
		p.setDoubleArrow([27,28,19,29,39])
		p.setDoubleArrow([39,49,48,57,58,59])
		p.setDoubleArrow([59,69,68,67,56])
		p.setDoubleArrow([27,37,47,56])
		p.setDoubleArrow([14,25,24,34])
		p.setDoubleArrow([34,44,45,46,56])
		p.setDoubleArrow([56,66,65,75,64])
		p.setDoubleArrow([64,74,85,76])
		p.setDoubleArrow([76,87,96])
		p.setDoubleArrow([96,97,88,79,89])
		p.setDoubleArrow([64,63,73,83,93,92])
		p.setDoubleArrow([92,91,81,71,61,51,52])
		p.setDoubleArrow([52,53,54,55,64])
		p.setDoubleArrow([52,43,42,41])
		p.setDoubleArrow([41,32,33,22,23,14])
		
		self.assertEqual(p.countSolutions(test=True),'1:976458213815236947423197685769312854184765329532984176648523791251679438397841562','Failed Target Practice')
		
if __name__ == '__main__':
    unittest.main()