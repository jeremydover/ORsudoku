import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Regionometers
	# Author: The Pedalling Pianist
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000H0Z
	# Constraints tested: setRegionometer, setGiven, setKropkiWhiteArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGiven(459)
		p.setRegionometer([31,41,51,61,71])
		p.setRegionometer([15,14,13,12,22,32,42,52])
		p.setRegionometer([16,17])
		p.setRegionometer([18,28,38,48,58,68,78,88,98])
		p.setRegionometer([39,49,59,69,79])
		p.setRegionometer([33,23,24,25,26,27,37,47])
		p.setRegionometer([43,53,63,73,83,84,85,86,76,66,56,46,36,35,34,44,54,64,74,75,65,55])
		p.setRegionometer([62,72,82,92,93])
		p.setRegionometer([94,95,96,97,87,77,67,57])
		p.setKropkiWhiteArray([331,471,751])
		
		self.assertEqual(p.countSolutions(test=True),'1:452987163986314257713562498364298571198475632275631984529743816847156329631829745','Failed Regionometers')
		
if __name__ == '__main__':
    unittest.main()