import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Line Sums
	# Author: clover!
	# https://sudokupad.app/hjrivcryuv
	# Constraints tested: setLineSumeLine, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setLineSumLine([12,21,31])
		p.setLineSumLine([17,18,29])
		p.setLineSumLine([23,32,42])
		p.setLineSumLine([24,25,36])
		p.setLineSumLine([26,27,38])
		p.setLineSumLine([43,52,62])
		p.setLineSumLine([44,55,66])
		p.setLineSumLine([48,58,67])
		p.setLineSumLine([68,78,87])
		p.setLineSumLine([72,83,84])
		p.setLineSumLine([74,85,86])
		p.setLineSumLine([79,89,98])
		p.setLineSumLine([81,92,93])
		p.setGivenArray([125,171,238,256,272,297,312,321,383,528,585,727,781,792,814,832,851,875,931,986])
		
		self.assertEqual(p.countSolutions(test=True),'1:657329184348165297219847635196574823784231956523698741975486312462913578831752469','Failed Line Sums')
		
if __name__ == '__main__':
    unittest.main()