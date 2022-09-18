import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Locking Out the Odds
	# Author: jeremydover
	# Link: https://link.sudokupad.app/polar-lockingouttheodds
	# Constraints tested: setGiven, setEvenArray, setLockoutLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGiven(556)
		p.setEvenArray([14,16,18,23,27,32,41,44,46,48,53,68,71,72,85,89,96,98])
		p.setLockoutLine([12,23,33,32,21])
		p.setLockoutLine([24,14,15,16,26])
		p.setLockoutLine([29,18,17,27,38])
		p.setLockoutLine([34,44,45,46,36])
		p.setLockoutLine([42,41,52,53,62])
		p.setLockoutLine([49,48,57,68,69])
		p.setLockoutLine([83,72,71,81,92])
		p.setLockoutLine([75,74,85,96,86])
		p.setLockoutLine([78,89,99,98,87])
		
		self.assertEqual(p.findSolution(test=True),'534896127768521439129743658497218365812365974356479281285134796943687512671952843','Failed Locking out the Odds')
		
if __name__ == '__main__':
    unittest.main()