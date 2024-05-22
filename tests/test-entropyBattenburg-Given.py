import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Neapolitan Sponge
	# Author: jeremydover
	# Link: https://f-puzzles.com/?id=29pulppf
	# Link: https://tinyurl.com/5n7sazra
	# Constraints tested: setGivenArray,setEntropyBattenburgArray,setEntropyBattenburgNegative
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)	
		p.setGivenArray([111,154,173,195,316,351,398,448,475,636,661,717,759,793,915,932,958,999])
		p.setEntropyBattenburgArray([11,18,22,27,44,45,54,55,72,77,81,88])
		p.setEntropyBattenburgNegative()
		self.assertEqual(p.countSolutions(test=True),'1:189746325425938167673215498397824516251369784846571932714692853968453271532187649','Failed Neapolitan Sponge')
		
if __name__ == '__main__':
    unittest.main()