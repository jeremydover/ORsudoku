import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Someday When Spring is Here
	# Author: Twototenth
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0007L9
	# Constraints tested: setMissingThermo
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setThermo([96,95])
		p.setMissingThermo([13,12,23,33,34])
		p.setMissingThermo([26,37,28,29])
		p.setMissingThermo([32,22,31,41,42,43])
		p.setMissingThermo([36,46,45])
		p.setMissingThermo([49,48,47,56,55,54,63,62,61])
		p.setMissingThermo([65,64,74])
		p.setMissingThermo([67,68,69,79,88,78])
		p.setMissingThermo([76,77,87,98,97])
		p.setMissingThermo([81,82,73,84])
			
		self.assertEqual(p.countSolutions(test=True),'1:231647895485291367796835241654123789879456132123789654968572413347918526512364978','Failed Someday When Spring is Here')
		
if __name__ == '__main__':
    unittest.main()