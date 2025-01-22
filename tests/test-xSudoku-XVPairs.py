import unittest
from schroedingerSudoku import schroedingerCellSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Xtravaganza
	# Author: tallcat
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000BRI
	# Constraints tested: schroedingerCellSudoku, setXSudokuMain, setXSudokuOff, setXVXArray, setXVV
	
	def test_puzzle(self):
		p = schroedingerCellSudoku(3)
		p.setGivenArray([291,922])
		p.setXSudokuMain()
		p.setXSudokuOff()
		p.setXVXArray([160,310,341,361,440,450,541,561,580,730,760,751,841])
		p.setXVV(930)
		
		self.assertEqual(p.countSolutions(test=True),'1:915860342230745691467391850608237419143906528592184063784029135059613284321458906000000700800000000000002000000500000070000000000000007006000000000070000000000070','Failed Xtravaganza')
		
if __name__ == '__main__':
    unittest.main()
	

