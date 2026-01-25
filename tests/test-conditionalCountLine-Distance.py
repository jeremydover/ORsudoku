import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (384) - Sudoku - Distant Relations
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000B5K
	# Constraints tested: setConditionalCountLine
	# Note: the puzzle as stated has a negative constraint, but it is not needed to force a unique solution.
	#       It would be possible to implement the negative constraint using selection criteria:
	#       [('Location','Distance',1),('RelatedDigit',1,p.NE,1,1),('RelatedDigit',1,p.NE,1,-1)]
	# However, we'd have to implement this for about 400 non-chosen diagonals.
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		lines = [[11,22,33,44,55,66,77,88,99],
				[15,25,35,45,55,65,75,85,95],
				[19,28,37,46,55,64,73,82,91],
				[22,32,42,52,62,72,82,92],
				[23,33,43,53,63,73,83,93],
				[24,33,42,51],
				[28,27,26,25,24,23,22,21],
				[29,28,27,26,25,24,23,22,21],
				[32,43,54,65,76,87,98],
				[38,47,56,65,74,83,92],
				[39,38,37,36,35,34,33,32,31],
				[44,55,66,77,88,99],
				[46,35,24,13],
				[46,37,28,19],
				[47,48,49],
				[51,61,71,81,91],
				[51,62,73,84,95],
				[52,43,34,25,16],
				[61,62,63,64,65,66,67,68,69],
				[62,52,42,32,22,12],
				[66,56,46,36,26,16],
				[66,76,86,96],
				[66,77,88,99],
				[67,56,45,34,23,12],
				[74,65,56,47,38,29],
				[75,66,57,48,39],
				[77,67,57,47,37,27,17],
				[81,71,61,51,41,31,21,11],
				[82,83,84,85,86,87,88,89],
				[83,73,63,53,43,33,23,13],
				[87,76,65,54,43,32,21],
				[91,82,73,64,55,46,37,28,19],
				[91,92,93,94,95,96,97,98,99],
				[92,83,74,65,56,47,38,29]]
		for x in lines:
			p.setConditionalCountLine(x,1,[('Location','Distance',1),('RelatedDigit',1,p.LE,1,1),('RelatedDigit',1,p.GE,1,-1),('RelatedDigit',1,p.NE,1,0)],[['Last']])
		
		self.assertEqual(p.countSolutions(test=True),'1:364815792517329846829674315985463271246157983731982564193548627652791438478236159','Failed Sudoku Variants Series (384) - Sudoku - Distant Relations')
		
if __name__ == '__main__':
    unittest.main()