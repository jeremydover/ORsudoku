import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Axis and Allies
	# Author: jeremydover
	# Link: https://f-puzzles.com/?id=2etdyc54
	# Link: https://tinyurl.com/3rrem8y8
	# Constraints tested: setCage, setVault, setIndexColumn
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setFortress([78,79])
		p.setFortress([87,97])
		p.setFortress([13,23,33,32,31])
		p.setFortress([58,59,49])
		p.setFortress([85,95,94])
		p.setFortress([52])
		p.setFortress([25])
		p.setFortress([29])
		p.setFriendlyArray([14,18,22,28,34,38,41,42,43,45,47,48,57,64,72,74,75,76,81,82,84,99])
		p.setFriendlyNegative()
		
		self.assertEqual(p.findSolution(test=True),'237169485416385927598247136143952768682714593759638241921876354875493612364521879','Failed Axis and Allies')
		
if __name__ == '__main__':
    unittest.main()