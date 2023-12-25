import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Missing Arrow
	# Author: GradientGuru
	# Link: https://f-puzzles.com/?id=yh6on7a5
	# Constraints tested: setGivenArray,setMissingArrow
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)	
		p.setGivenArray([141,444,694,877])
		p.setMissingArrow([19,29,39,38])
		p.setMissingArrow([27,36,35,34])
		p.setMissingArrow([31,42])
		p.setMissingArrow([41,51,62,73,83,93])
		p.setMissingArrow([45,44,54])
		p.setMissingArrow([46,47,48,49])
		p.setMissingArrow([61,72,82])
		p.setMissingArrow([63,64,65,66])
		p.setMissingArrow([68,69,79])
		p.setMissingArrow([74,85,76])
		p.setMissingArrow([78,87,96])
		self.assertEqual(p.findSolution(test=True),'243156897518974362976823541397465128164287935825319674751692483632548719489731256','Failed Missing Arrow')
		
if __name__ == '__main__':
    unittest.main()