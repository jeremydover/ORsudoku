import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (318) - Thermometers - Removed Bulbs
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000637
	# Constraints tested: setRemovedBulbThermo
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)	
		p.setRemovedBulbThermo([13,22,31,42,51,62,71,72,73])
		p.setRemovedBulbThermo([65,64,63,53,43,33,34,35,25,26,36,37,47,57,56])
		p.setRemovedBulbThermo([44,45,55,66,75])
		p.setRemovedBulbThermo([81,82,92,91])
		p.setRemovedBulbThermo([93,83,84])
		p.setRemovedBulbThermo([85,76,67,68,79,89,98,97,86])
		self.assertEqual(p.countSolutions(test=True),'1:128967354657834192493125687834652719275419836916783425389546271541278963762391548','Failed Sudoku Variants Series (318) - Thermometers - Removed Bulbs')
		
if __name__ == '__main__':
    unittest.main()