import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Ice Cubes
	# Author: Tyrgannus
	# Link: https://f-puzzles.com/?id=yesx24yy
	# Constraints tested: setKropkiWhiteArray,setKropkiBlackArray, setDoublingLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)	
		p.setKropkiWhiteArray([111,140,151,220,261,310,350,441,631,720,721,731,770,780])
		p.setKropkiBlackArray([160,331,641,651,740,741])
		p.setDoublingLine([16,27,38,47,56,45,34,25])
		p.setDoublingLine([17,28,39,48,57,46,35,26])
		p.setDoublingLine([53,64,75,84,93,82,71,62])
		p.setDoublingLine([54,65,76,85,94,83,72,63])
		self.assertEqual(p.findSolution(test=True),'513982476489376152762145938971538264824697513635214897356421789147869325298753641','Failed Ice Cubes')
		
if __name__ == '__main__':
    unittest.main()