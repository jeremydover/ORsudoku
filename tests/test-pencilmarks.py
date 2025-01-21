import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Pencilmark Sudoku
	# Author: Florian Wortmann
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0007L4
	# Constraints tested: setPencilmarksArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setPencilmarksArray([1112,15146,1669,1819,1913,22129,2413,2589,28123589,33569,3657,3779,4223,44345,4549,4669,4756,5279,55678,5946,6367,66147,6848,7389,7446,77678,8312389,8512,8618,88289,9123,9556,99345])
	
		self.assertEqual(p.countSolutions(test=True),'1:278569413916384752435127968123496587894275136567831249759643821642718395381952674','Failed Pencilmark Sudoku')
		
if __name__ == '__main__':
    unittest.main()