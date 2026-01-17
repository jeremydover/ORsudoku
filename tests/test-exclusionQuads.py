import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Exclusion (Quadruples) Sudoku
	# Author: Bill Murphy
	# Link: https://www.gmpuzzles.com/blog/2026/01/exclusion-quadruples-sudoku-by-bill-murphy/
	# Constraints tested: setExclusionQuadArray,setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setExclusionQuadArray([22468,2435,2568,27357,4245,441,4728,5268,552,5757,72157,7426,7517,77268])
		p.setGivenArray([125,184,211,298,816,893,922,987])
		
		self.assertEqual(p.countSolutions(test=True),'1:856219347173645928492873165368421759217598634945367281734186592689752413521934876','Failed Exclusion (Quadruples) Sudoku')
		
if __name__ == '__main__':
    unittest.main()