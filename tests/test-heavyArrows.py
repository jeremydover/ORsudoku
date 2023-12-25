import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (389) - Heavy Arrows Sudoku
	# Author: Richard Stolk
	# Link: https://f-puzzles.com/?id=2dqkw9rf
	# Link: https://tinyurl.com/yc4vx7vp
	# Constraints tested: setHeavyArrow
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)	
		p.setHeavyArrow([12,23,24])
		p.setHeavyArrow([17,16,15])
		p.setHeavyArrow([22,33,34,35,36])
		p.setHeavyArrow([32,42,52])
		p.setHeavyArrow([39,28,27,26])
		p.setHeavyArrow([43,53,63,73])
		p.setHeavyArrow([47,37,38,49,48,58,57,67])
		p.setHeavyArrow([59,68,77,76])
		p.setHeavyArrow([61,51,42,31])
		p.setHeavyArrow([62,72,82])
		p.setHeavyArrow([64,54,44])
		p.setHeavyArrow([65,55,45])
		p.setHeavyArrow([66,56,46])
		p.setHeavyArrow([88,87,96])
		p.setHeavyArrow([94,95,85])		
		self.assertEqual(p.findSolution(test=True),'124697853593128647876354219765813924481279536932546178657931482319482765248765391','Failed Heavy Arrows')
		
if __name__ == '__main__':
    unittest.main()