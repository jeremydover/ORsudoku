import unittest
from schroedingerSudoku import schroedingerCellSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Kodama
	# Author: zetamath
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008V6
	# Constraints tested: schroedingerCellSudoku, setXVXArray, setGermanWhispersLine
	
	def test_puzzle(self):
		p = schroedingerCellSudoku(3)
		p.setXVXArray([150,240,360,491,511,730])
		p.setGermanWhispersLine([22,13,24,33])
		p.setGermanWhispersLine([23,32,43])
		p.setGermanWhispersLine([17,26,37])
		p.setGermanWhispersLine([27,38,47,36])
		p.setGermanWhispersLine([35,46,57,66,75,64,53,44,35])
		p.setGermanWhispersLine([71,72,63])
		p.setGermanWhispersLine([67,68,79])
		p.setGermanWhispersLine([92,93,84,73])
		p.setGermanWhispersLine([74,85,76])
		p.setGermanWhispersLine([85,95])
		p.setGermanWhispersLine([77,86,97,98])
		
		self.assertEqual(p.countSolutions(test=True),'1:890425176356918420214067395437180259028549731165372084501796843749803512683251907000030000070000000000000008000000060000600000900000000002000000000000600000004000','Failed Kodama')
		
if __name__ == '__main__':
    unittest.main()
	
	
