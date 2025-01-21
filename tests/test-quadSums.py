import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Quad sums sudoku
	# Author: udukos
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0007B5
	# Constraints tested: setQuadSumArray, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([496,946])
		p.setQuadSumArray([16,18,22,26,44,45,47,48,51,54,63,77,78,83,84])
	
		self.assertEqual(p.countSolutions(test=True),'1:865291743739564281124783965597842316486317592312956478653478129978125634241639857','Failed Quad sums sudoku')
		
if __name__ == '__main__':
    unittest.main()