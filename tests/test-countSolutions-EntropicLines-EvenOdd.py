import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: A Pebble on the Garden Path (partial)
	# Author: jeremydover
		
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([194,336,469,811])
		p.setEvenArray([24,44,66,84,85])
		p.setEntropicLine([91,82,73,74,75,65,54,53,52,41,31,21,11,12,13,14,25,16,17,28,39,48,59,69,79,88,98])
		p.setEntropicLine([34,45,56,57,67,77,86,96,95,94,93])
		
		self.assertEqual(p.countSolutions(test=True),'2:853721964219468357476395821731649285524837196698512473342956718167283549985174632853721964219648357476395821731469285524837196698512473342956718167283549985174632','Failed A Pebble on the Garden Path (partial, 2 solutions)')
		
if __name__ == '__main__':
    unittest.main()