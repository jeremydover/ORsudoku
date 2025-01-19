import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Genetics
	# Author: Angelo
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009QE
	# Constraints tested: setGenetics, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGeneticArray([[14,15,24],[16,17,26],[18,19,29],[21,22,31],[24,25,34],[24,25,35],[26,27,37],[32,33,43],[34,35,44],[36,37,46],[37,38,47],[41,42,52],[43,44,53],[43,44,54],[45,46,55],[52,53,63],[53,54,64],[54,55,64],[54,55,65],[58,59,68],[58,59,69],[63,64,74],[65,66,76],[72,73,82],[74,75,84],[76,77,86],[81,82,92],[84,85,94],[86,87,96]])
		p.setGivenArray([433,644,659])
		
		self.assertEqual(p.countSolutions(test=True),'1:236718549745369218891254376953672184472581963618493752569837421184925637327146895','Failed Genetics')
		
if __name__ == '__main__':
    unittest.main()