import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sum Amount of Trouble
	# Author: Tyrgannus
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000EV4
	# Constraints tested: setKnappDanebenCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setKnappDanebenCage([11,12,21],7)
		p.setKnappDanebenCage([14,15,16],8)
		p.setKnappDanebenCage([18,19,29],22)
		p.setKnappDanebenCage([32,33,34,43],12)
		p.setKnappDanebenCage([36,37,38,47],12)
		p.setKnappDanebenCage([45,55],16)
		p.setKnappDanebenCage([51,52,53],11)
		p.setKnappDanebenCage([57,58,59],18)
		p.setKnappDanebenCage([62,72,82,83,84],35)
		p.setKnappDanebenCage([64,74,73],23)
		p.setKnappDanebenCage([66,76,77],22)
		p.setKnappDanebenCage([68,78,88,87,86],16)
		p.setKnappDanebenCage([81,91,92],10)
		p.setKnappDanebenCage([85,95],15)
		p.setKnappDanebenCage([89,99,98],18)
		
		self.assertEqual(p.countSolutions(test=True),'1:518342679276819435934567128791285364453176892862934517347628951189753246625491783','Failed Sum Amount of Trouble')
		
if __name__ == '__main__':
    unittest.main()