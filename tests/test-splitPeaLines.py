import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (431) - Split Pea Lines
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000O32
	# Constraints tested: setSplitPeaLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSplitPeaLine([11,12,13,23,33])
		p.setSplitPeaLine([11,21,31,32,33])
		p.setSplitPeaLine([33,24,14,15])
		p.setSplitPeaLine([15,25,26,36,46])
		p.setSplitPeaLine([27,18,29,28])
		p.setSplitPeaLine([46,37,47,48,49,59,69,68,58,67,56])
		p.setSplitPeaLine([56,66,65,64,55])
		p.setSplitPeaLine([55,54,44,45,46])
		p.setSplitPeaLine([91,92,83,74])
		p.setSplitPeaLine([76,75,84,95,86])
		p.setSplitPeaLine([86,97,88,77,76])
		p.setSplitPeaLine([78,79,89,99,98])
		
		self.assertEqual(p.countSolutions(test=True),'1:748521369235796148961438257489253671573619824126847593852174936317962485694385712','Failed Sudoku Variants Series (431) - Split Pea Lines')
		
if __name__ == '__main__':
    unittest.main()