import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Keep off the Border!
	# Author: jeremydover
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000HH4
	# Constraints tested: setAntiKnight,setLockoutLine, setGiven
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setAntiKnight()
		p.setLockoutLine([11,21,22,13,14,25,26,16])
		p.setLockoutLine([31,32,33,34,35,36])
		p.setLockoutLine([18,27,28,29,38])
		p.setLockoutLine([41,51,61,71,81,91])
		p.setGiven(232)
		p.setLockoutLine([41,42,43])
		p.setLockoutLine([54,64,55,56,46,47])
		p.setLockoutLine([68,78,89,98])
		
		self.assertEqual(p.countSolutions(test=True),'1:537641298682597143491238657319784562856912734274356981923475816165823479748169325','Failed Keep off the Border!')
		
if __name__ == '__main__':
    unittest.main()