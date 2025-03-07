import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (363) - Potpourri N-Sums Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009DK
	# Constraints tested: setPotpourriNSums
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setPotpourriNSums(p.Top,[15,None,24,None,16,43,5,5])
		p.setPotpourriNSums(p.Right,[10,None,33,None,24,28,7,7])
		p.setPotpourriNSums(p.Bottom,[None,None,18,4,25,40,None,12])
		p.setPotpourriNSums(p.Left,[21,None,None,None,23,19,39,None,31])
			
		self.assertEqual(p.countSolutions(test=True),'1:293781546568234719147659283356148972471925368982367451735896124624513897819472635','Failed Sudoku Variants Series (363) - Potpourri N-Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()