import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Index Lines
	# Author: marty_sears
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000JFA
	# Constraints tested: setIndexLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setIndexLine([32,31,21,11,12,13])
		p.setIndexLine([37,36,46,35,34,25,14])
		p.setIndexLine([38,48,39,29,19,18,27,28])
		p.setIndexLine([44,45,55,54,53,52])
		p.setIndexLine([69,58,57,56,66,67,68])
		p.setIndexLine([73,63,62,51,42,43,33,24,23])
		p.setIndexLine([76,86,96,95,84,85,74,83,72])
		p.setIndexLine([79,89,78,77,87,88,99,98,97])
		p.setIndexLine([91,81,71])
			
		self.assertEqual(p.countSolutions(test=True),'1:423178956687459213519632784951324678864517329732896541276981435398245167145763892','Failed Index Lines')
		
if __name__ == '__main__':
    unittest.main()