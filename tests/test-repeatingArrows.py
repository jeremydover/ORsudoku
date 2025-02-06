import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (391) - Two arrows in one
	# Author: Richard
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000BVF
	# Constraints tested: setRepeatingArrow
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRepeatingArrow([21,11,22,32,23])
		p.setRepeatingArrow([14,24,34,44,54,64])
		p.setRepeatingArrow([15,25,35,45,55,65])
		p.setRepeatingArrow([16,17,18,29,38])
		p.setRepeatingArrow([27,37,47,58])
		p.setRepeatingArrow([74,73,62,53])
		p.setRepeatingArrow([94,83,92,91])
		p.setRepeatingArrow([95,84,75,66])
		p.setRepeatingArrow([96,86,76,67])
		p.setRepeatingArrow([97,98,89,88,87,78,68])
		
		self.assertEqual(p.countSolutions(test=True),'1:325987164741365982869124753194538276238716495657249318473851629986472531512693847','Failed Sudoku Variants Series (391) - Two arrows in one')
		
if __name__ == '__main__':
    unittest.main()