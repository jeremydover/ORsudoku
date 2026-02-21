import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (457) - Hot Arrows
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000R4R
	# Constraints tested: setConditionalCountLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setConditionalCountLine([11,12,13,14,15,16,17,18,19],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([14,15,16,17,18,19],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([16,17,18,19],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([17,18,19],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([13,23,33,43,53,63,73,83,93],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([26,36,46,56,66,76,86,96],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([31,32,33,34,35,36,37,38,39],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([34,44,54,64,74,84,94],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([49,48,47,46,45,44,43,42,41],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([48,47,46,45,44,43,42,41],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([47,46,45,44,43,42,41],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([46,45,44,43,42,41],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([45,44,43,42,41],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([44,43,42,41],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([43,42,41],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([42,41],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([51,41,31,21,11],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([53,54,55,56,57,58,59],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([54,55,56,57,58,59],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([56,57,58,59],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([57,56,55,54,53,52,51],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([61,71,81,91],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([63,53,43,33,23,13],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([73,74,75,76,77,78,79],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([74,64,54,44,34,24,14],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([76,66,56,46,36,26,16],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([79,78,77,76,75,74,73,72,71],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([81,82,83,84,85,86,87,88,89],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([83,73,63,53,43,33,23,13],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([91,92,93,94,95,96,97,98,99],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([96,95,94,93,92,91],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		p.setConditionalCountLine([97,87,77,67,57,47,37,27,17],1,[('Location','Distance',1),('RelatedDigit',1,p.GE,1,1)],[['Last']])
		
		self.assertEqual(p.countSolutions(test=True),'1:748253196293716854561498327912345678476182539385967241834571962127639485659824713','Failed Sudoku Variants Series (457) - Hot Arrows')
		
if __name__ == '__main__':
    unittest.main()