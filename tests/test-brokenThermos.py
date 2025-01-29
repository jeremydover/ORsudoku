import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Broken Thermo
	# Author: Belamis
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000ID8
	# Constraints tested: setBrokenThermo
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setBrokenThermo([66,65,64,54,44,45,46,36,35,34,33,32,42,43,53,63,73,72,82,83,84,85,86,87,77,67,68,69,79,78,88,98,97,96,95,94,93,92,91,81,71,61,51])
		p.setBrokenThermo([12,22])
		p.setBrokenThermo([47,37,27,26,25])
		
		self.assertEqual(p.countSolutions(test=True),'1:137264895654398712298751463712689354943517286865432179576843921489125637321976548','Failed Broken Thermo')
		
if __name__ == '__main__':
    unittest.main()