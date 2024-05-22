import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Parking Garage
	# Author: jeremydover
	# Link: https://tinyurl.com/2p9ccszz
	# Constraints tested: setDisjointGroups, setGivenArray, setModularLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setDisjointGroups()
		p.setGivenArray([137,434,496,619,675,978])
		p.setModularLine([11,22,33,44,55,66,77,88,99])
		p.setModularLine([17,27,37,38,47])
		p.setModularLine([18,28,39,29,19])
		p.setModularLine([57,48,58,59])
		p.setModularLine([21,31,41,51])
		p.setModularLine([63,72,73,83,93])
		p.setModularLine([74,75,76])
		p.setModularLine([81,71,82,92,91])
		
		self.assertEqual(p.countSolutions(test=True),'1:487965213125873964693124785854791326736582491912436578579648132348219657261357849','Failed Parking Garage')
		
if __name__ == '__main__':
    unittest.main()