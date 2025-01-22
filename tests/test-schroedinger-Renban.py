import unittest
from schroedingerSudoku import schroedingerCellSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Archa
	# Author: zetamath
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008RS
	# Constraints tested: schroedingerCellSudoku, setXVXArray, SetRenbanLine

	def test_puzzle(self):
		p = schroedingerCellSudoku(3)
		p.setXVXArray([151,230,321,380,460,660,771,781,810,940,950])
		p.setRenbanLine([12,23,14,25])
		p.setRenbanLine([16,17,27,37])
		p.setRenbanLine([18,28,38])
		p.setRenbanLine([19,29,39,49])
		p.setRenbanLine([32,33,34,24])
		p.setRenbanLine([41,52])
		p.setRenbanLine([47,56])
		p.setRenbanLine([54,55,65,75,74])
		p.setRenbanLine([61,62])
		p.setRenbanLine([67,57,58,59])
		p.setRenbanLine([63,73,83,84])
		p.setRenbanLine([77,78,79])
		p.setRenbanLine([81,91,92,93])
		p.setRenbanLine([97,98,99])
		
		self.assertEqual(p.countSolutions(test=True),'1:563807924827394605910265837751432096089671452236059178675980241194723560302146789000010000000000010040000000000008000000000003400000000000000300008000000000500000','Failed Archa')
		
if __name__ == '__main__':
    unittest.main()
	
	
