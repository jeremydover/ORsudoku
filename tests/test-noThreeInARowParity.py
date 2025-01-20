import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (017) - No three odd/even in line
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0001XL
	# Constraints tested: setNoThreeInARowParity, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setNoThreeInARowParity()
		p.setGivenArray([122,136,188,211,245,296,356,389,413,449,535,579,667,691,727,754,815,868,892,923,978,984])
	
		self.assertEqual(p.countSolutions(test=True),'1:926734185183529476457861293318956724765412938294387651872143569549678312631295847','Failed Sudoku Variants Series (017) - No three odd/even in line')
		
if __name__ == '__main__':
    unittest.main()