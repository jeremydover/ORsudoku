import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: The Mandalorian Sudoku
	# Author: Quarterthru
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0004RS
	# Constraints tested: setMultiDigitSumArrow,setXVVArray,setXVXArray,setCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setMultiDigitSumArrow([11,21,32,42,52,62,73,84,95,86,77,68,58,48,38,28,29],2)
		p.setCage([14,15,16],11)
		p.setCage([43,44,45,46,47],26)
		p.setCage([55,65],8)
		p.setCage([75,85],12)
		p.setXVVArray([161,171,330,370,411,451,680,730,880])
		p.setXVXArray([231,250,431,491,541,611,651,661,670,681,820,840,950])
			
		self.assertEqual(p.countSolutions(test=True),'1:735812496429673158861459237214538679386927541957164823192346785673285914548791362','Failed The Mandalorian Sudoku')
		
if __name__ == '__main__':
    unittest.main()