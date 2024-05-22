import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Cthulhu slowly rises
	# Author: jeremydover
	# Link: https://tinyurl.com/29pdnfb8
	# Constraints tested: setSlowThermo
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSlowThermo([94,83,74,63,54,43,34,23,14,15])
		p.setSlowThermo([96,87,76,67,56,47,36,27,16,15])
		p.setSlowThermo([66,55,44,35,24][::-1])
		p.setSlowThermo([64,55,46,35,26][::-1])
		p.setSlowThermo([41,32,33,42,53,62,73][::-1])
		p.setSlowThermo([52,61,71,81])
		p.setSlowThermo([37,48,57,68,69,78,77])
		p.setSlowThermo([89,98])
		
		self.assertEqual(p.countSolutions(test=True),'1:125897634368241795497536182974623518816475329253918467582364971641789253739152846','Failed Cthulhu slowly rises')
		
if __name__ == '__main__':
    unittest.main()