import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Pointing Arrow Sudoku
	# Author: Hu Mengting
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0004N6
	# Constraints tested: setPointingArrow
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setPointingArrow([13,24])
		p.setPointingArrow([49,38,28,17,26])
		p.setPointingArrow([55,46,35,34])
		p.setPointingArrow([64,53,52,41,32])
		p.setPointingArrow([67,78,88,97,86])
		p.setPointingArrow([82,71,61,51])
		p.setPointingArrow([95,94,84,75])
			
		self.assertEqual(p.countSolutions(test=True),'1:623958174458371629917246538289513467541697382376824951162739845895462713734185296','Failed Pointing Arrow Sudoku')
		
if __name__ == '__main__':
    unittest.main()