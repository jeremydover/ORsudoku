import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Even Odd Thermos
	# Author: TheMonsterOx
	# https://tinyurl.com/yv2kz5na
	# Constraints tested: setOddEvenThermo
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setOddEvenThermo([17,28,39,38])
		p.setOddEvenThermo([18,29,19])
		p.setOddEvenThermo([21,12,11])
		p.setOddEvenThermo([24,15,26])
		p.setOddEvenThermo([31,22,13,23])
		p.setOddEvenThermo([34,35,36])
		p.setOddEvenThermo([48,59,68])
		p.setOddEvenThermo([61,51,41])
		p.setOddEvenThermo([73,63])
		p.setOddEvenThermo([79,88,97,87])
		p.setOddEvenThermo([89,98,99])
		p.setOddEvenThermo([92,81,91])
		p.setOddEvenThermo([93,82,71,72])
		p.setOddEvenThermo([96,95,94])
			
		self.assertEqual(p.countSolutions(test=True),'1:647539128239187654185246397972863415514792863368415279796324581451678932823951746','Failed Even Odd Thermos')
		
if __name__ == '__main__':
    unittest.main()