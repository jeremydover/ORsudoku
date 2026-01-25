import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (428) - Eight Lines
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000NO3
	# Constraints tested: set10Line
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.set10Line([11,21,12],8)
		p.set10Line([23,22,31,41,42,43],8)
		p.set10Line([16,25,35],8)
		p.set10Line([29,19,28,17,26,37],8)
		p.set10Line([24,34,44,54,64],8)
		p.set10Line([38,49,58,68,79],8)
		p.set10Line([45,46,56,66],8)
		p.set10Line([57,67,78],8)
		p.set10Line([63,72,71],8)
		p.set10Line([91,82,93],8)
		p.set10Line([94,84,75,85,95,96,97,86,76],8)
		p.set10Line([87,88,98,99],8)
		
		self.assertEqual(p.countSolutions(test=True),'1:839465172541732968267189543153826794674391285982547316425918637316274859798653421','Failed Sudoku Variants Series (428) - Eight Lines')
		
if __name__ == '__main__':
    unittest.main()