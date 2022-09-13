import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Double, Double
	# Author: zetamath
	# Link: https://zetamath.link/double-double
	# Constraints tested: setDoubleArrow, setEven, doublerSudoku
	
	def test_puzzle(self):
		p = ORsudoku.doublerSudoku(3)
		p.setEven(45)
		p.setDoubleArrow([23,12,11,22,31,32])
		p.setDoubleArrow([32,42,52,62])
		p.setDoubleArrow([25,26,16,17])
		p.setDoubleArrow([38,37,47])
		p.setDoubleArrow([47,36,35,34,33,43,53,63,74])
		p.setDoubleArrow([74,73,83,93,92,91])
		p.setDoubleArrow([74,84,94])
		p.setDoubleArrow([44,45,46,55,64,65,66,77])
		p.setDoubleArrow([76,87,78,88])
		p.setDoubleArrow([88,89,79,69])
		p.setDoubleArrow([69,68,67])
		
		self.assertEqual(p.findSolution(test=True),'37958*4*62112*5*697348684132*7*59453*8*219678*6*247951379135648*2*2367*1*58945179482*3*6*9*48263175','Failed Double, Double')
		
if __name__ == '__main__':
    unittest.main()