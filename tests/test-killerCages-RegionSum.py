import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Overlap
	# Author: BremSter
	# Link: https://bremster.tiny.us/overlap
	# Constraints tested: setCage, setRegionSumLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCage([11,12,21,31],19)
		p.setCage([14,15,16],15)
		p.setCage([23,33,32],10)
		p.setCage([26,36,35],10)
		p.setCage([41,42,43],12)
		p.setCage([44,45,54],17)
		p.setCage([47,48,57,67],10)
		p.setCage([49,59,69],19)
		p.setCage([51,61],14)
		p.setCage([62,63,73],18)
		p.setCage([71,72],10)
		p.setCage([83,93],8)
		p.setCage([94,95],12)
		p.setCage([78,87,88],10)
		p.setRegionSumLine([11,21,31,41,42])
		p.setRegionSumLine([15,16,27,38,49,59])
		p.setRegionSumLine([23,33,44,54,63,62])
		p.setRegionSumLine([26,36,47,57,67,78,88])
		p.setRegionSumLine([28,37,46,55])
		p.setRegionSumLine([61,72,83,94])
		
		self.assertEqual(p.findSolution(test=True),'387492651694851723215736849471689235928315476563247198739128564852964317146573982','Failed Overlap')
		
if __name__ == '__main__':
    unittest.main()