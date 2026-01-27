import unittest
from squishdoku import squishdoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Squishdoku
	# Author: Jay Dyer
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000FWO
	# Constraints tested: setRegionSumLine, setGermanWhispersLine
	
	def test_puzzle(self):
		p = squishdoku(3)
		p.setRegionSumLine([41,31,21,12,13,14])
		p.setRegionSumLine([24,15,16,27,37,46])
		p.setGermanWhispersLine([36,35,45,44])
		p.setGermanWhispersLine([54,65,76,77])
			
		self.assertEqual(p.countSolutions(test=True),'1:7328419186975249513866284971317624585931672645893','Failed Squishdoku')
		
if __name__ == '__main__':
    unittest.main()