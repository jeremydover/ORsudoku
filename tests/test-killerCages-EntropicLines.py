import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Third-Degree Murder
	# Author: jeremydover and Raumplaner
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000AZI
	# Constraints tested: setEntropicLine, setCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setEntropicLine([11,21,22,13,12])
		p.setEntropicLine([14,15,25])
		p.setEntropicLine([17,27])
		p.setEntropicLine([18,19,29])
		p.setEntropicLine([24,34,33])
		p.setEntropicLine([36,37,47])
		p.setEntropicLine([41,42])
		p.setEntropicLine([45,44,54])
		p.setEntropicLine([49,59,58])
		p.setEntropicLine([56,66,65])
		p.setEntropicLine([61,51,52,62])
		p.setEntropicLine([63,73,74])
		p.setEntropicLine([68,69])
		p.setEntropicLine([77,76,86])
		p.setEntropicLine([78,88,89,98,97,87])
		p.setEntropicLine([83,93])
		p.setCage([11,21,22],14)
		p.setCage([17,27],8)
		p.setCage([18,19,29],13)
		p.setCage([24,34,33],18)
		p.setCage([36,37,47],12)
		p.setCage([41,42],9)
		p.setCage([44,45,54],12)
		p.setCage([56,66,65],18)
		p.setCage([62,72],10)
		p.setCage([63,73,74],18)
		p.setCage([76,77,86],12)
		p.setCage([83,93],11)
		
		self.assertEqual(p.countSolutions(test=True),'1:391726548742958361856314792638472159475189236129563874583691427914237685267845913','Failed Third-Degree Murder')
		
if __name__ == '__main__':
    unittest.main()