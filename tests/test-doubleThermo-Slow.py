import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Slow Double Thermo
	# Author: Reverend
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0004K4
	# Constraints tested: setGivenArray,setDoubleThermo
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)	
		p.setGivenArray([158,226,262,287,439,678,821,843,889,959])
		p.setDoubleThermo([15,14,23,34,43],slow=True)
		p.setDoubleThermo([15,16,27,36,47],slow=True)
		p.setDoubleThermo([55,54,53,42,33,22],slow=True)
		p.setDoubleThermo([55,54,53,62,73,82],slow=True)
		p.setDoubleThermo([55,56,57,48,37,28],slow=True)
		p.setDoubleThermo([55,56,57,68,77,88],slow=True)
		p.setDoubleThermo([95,94,83,74,63],slow=True)
		p.setDoubleThermo([95,96,87,76,67],slow=True)
		self.assertEqual(p.countSolutions(test=True),'1:423781956968542173175963482259876341381425769746139825594618237812357694637294518','Failed Slow Double Thermo')
		
if __name__ == '__main__':
    unittest.main()