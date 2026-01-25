import unittest
from multiSudoku import doubleDoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Multi-Sudoku No. 90166
	# Author: GrandGames.net
	# Link: https://en.grandgames.net/multisudoku/id90166
	# Constraints tested: doubleDoku, setDoubleDokuConstraint
	
	def test_puzzle(self):
		p = doubleDoku(3,6)
		p.setDoubleDokuConstraint(1,'GivenArray',[[121,175,218,266,313,357,368,461,555,589,639,692,733,746,797,816,862,938,959]])
		p.setDoubleDokuConstraint(2,'GivenArray',[[287,296,389,575,681,698,768,814,827,936,963,972]])
				
		self.assertEqual(p.findSolution(test=True),'417329568892516743356478921284961375761253894539847612923684157675132489148795236961375824253894176847612395684157932132489567795236418329568741478921653516743289','Failed Multi-Sudoku No. 90166')

if __name__ == '__main__':  
    unittest.main()