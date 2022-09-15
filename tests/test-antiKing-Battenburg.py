import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Let them eat cake
	# Author: jeremydover
	# Link: https://f-puzzles.com/?id=2zhcfzeg
	# Link: https://tinyurl.com/mx6ku29j
	# Constraints tested: setRegion, setCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([455,152,958,687,626,221,889,413,815,195])
		p.setAntiKing()
		p.setBattenburgArray([13,33,63,83,16,36,66,86])
		p.setBattenburgNegative()
		
		self.assertEqual(p.findSolution(test=True),'693428715712965483458317629371652948845791362269834571184579236526143897937286154','Failed Let them eat cake')
		
if __name__ == '__main__':
    unittest.main()