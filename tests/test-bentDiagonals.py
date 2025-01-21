import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (050) - Bent Diagonals
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00023O
	# Constraints tested: setBentDiagonals, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([134,178,313,344,362,397,428,482,626,687,719,745,768,792,933,974])
		p.setBentDiagonals()
			
		self.assertEqual(p.countSolutions(test=True),'1:124976853697853241358412697481765329739124586265389174916548732842637915573291468','Failed Sudoku Variants Series (050) - Bent Diagonals')
		
if __name__ == '__main__':
    unittest.main()