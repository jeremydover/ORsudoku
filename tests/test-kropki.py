import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Some Dots
	# Author: jeremydover
	# Link: https://tinyurl.com/4cc27xjy
	# Constraints tested: setKropkiWhiteArray, setKropkiBlackArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setKropkiWhiteArray([110,320,191,271,710,720,531,491,591,251,750,541,241])
		p.setKropkiBlackArray([210,220,170,380,781,881,820,850,411,511,580,151,551])
		
		self.assertEqual(p.countSolutions(test=True),'1:763945218124386597589271436251639874497528163836417952678154329912863745345792681','Failed Some Dots')
		
if __name__ == '__main__':
    unittest.main()