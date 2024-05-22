import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Endless Knight
	# Author: jeremydover
	# Link: https://tinyurl.com/2d2f9hn3
	# Constraints tested: setAntiKnight, setRunOnRenbanLine, setThermo
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setAntiKnight()
		p.setRunOnRenbanLine([22,12,13,23,32,33])
		p.setRunOnRenbanLine([25,24,35,26,37,27])
		p.setRunOnRenbanLine([41,52,63,74,85,96,95,94,93,92,82,81,71,61,51,41,52,63,74])
		p.setRunOnRenbanLine([64,55,56,66,76,75])
		p.setRunOnRenbanLine([49,48,57,68,69,59,58])
		p.setRunOnRenbanLine([77,78,79,88,98,97])
		p.setThermo([19,29])
		p.setThermo([69,79])
		p.setThermo([91,92])
		
		self.assertEqual(p.countSolutions(test=True),'1:934528617715436829826971534582697143641352798397184265279813456458269371163745982','Failed Endless Knight')
		
if __name__ == '__main__':
    unittest.main()