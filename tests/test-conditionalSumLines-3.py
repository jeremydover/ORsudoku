import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: N-Mates
	# Author: BremSter
	# Link: https://www.youtube.com/watch?v=CVE536VR19Y
	# Constraints tested: setConditionalSumLine, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setConditionalSumLine([13,14,15,16,17,18,19],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		p.setConditionalSumLine([17,16,15,14,13,12,11],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		p.setConditionalSumLine([33,43,53,63,73,83,93],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		p.setConditionalSumLine([53,54,55,56,57,58,59],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		p.setConditionalSumLine([57,56,55,54,53,52,51],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		p.setConditionalSumLine([62,52,42,32,22,12],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		p.setConditionalSumLine([68,67,66,65,64,63,62,61],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		p.setConditionalSumLine([77,67,57,47,37,27,17],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		p.setConditionalSumLine([91,92,93,94,95,96,97,98,99],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		p.setConditionalSumLine([95,85,75,65,55,45,35,25,15],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		p.setConditionalSumLine([99,98,97,96,95,94,93,92,91],10,[('Location',p.EQ,1,'Distance',1)],[['Last']])
		
		p.setGivenArray([232,273,321,384,453,555,729,786,838,877])
		
		self.assertEqual(p.countSolutions(test=True),'1:943587216572164389816329547789631425431952678625478931297845163168293754354716892','Failed N-Mates')
		
if __name__ == '__main__':
    unittest.main()