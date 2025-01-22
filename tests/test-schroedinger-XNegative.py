import unittest
from schroedingerSudoku import schroedingerCellSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Quantum X
	# Author: starwarigami
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008TQ
	# Constraints tested: schroedingerCellSudoku, setXVXArray, setXVXNegative
	
	def test_puzzle(self):
		p = schroedingerCellSudoku(3)
		p.setXVXArray([110,140,160,171,211,220,341,351,411,451,461,470,541,611,610,620,660,680,721,730,791,811,830,850])
		p.setXVXNegative()
		
		self.assertEqual(p.countSolutions(test=True),'1:527649108964018235180273694279836510803124967641907382412390876796482051058761429030000000000000700000005000000000040000050000005000000000500000000000003300000000','Failed Quantum X')
		
if __name__ == '__main__':
    unittest.main()
	
	
