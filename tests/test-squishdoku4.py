import unittest
from squishdoku import squishdoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Be Careful What You Squish For
	# Author: Laake
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000G6X
	# Constraints tested: squishdoku, irregular, setGivenArray, setCage, setRenbanLine
	
	def test_puzzle(self):
		p = squishdoku(3,irregular=True)
		p.setRegion([11,12,21,22,23,31,32,33,41])
		p.setRegion([12,13,14,23,24,25,33,34,35])
		p.setRegion([14,15,16,17,25,26,27,35,36])
		p.setRegion([32,33,41,42,43,51,52,53,61])
		p.setRegion([33,34,35,43,44,45,53,54,55])
		p.setRegion([27,35,36,37,45,46,47,55,56])
		p.setRegion([52,53,61,62,63,71,72,73,74])
		p.setRegion([53,54,55,63,64,65,74,75,76])
		p.setRegion([47,55,56,57,65,66,67,76,77])
		p.setGivenArray([137,753])
		p.setCage([27,37,36],23)
		p.setCage([51,52,61],7)
		p.setRenbanLine([15,16,17])
		p.setRenbanLine([32,42])
		p.setRenbanLine([46,56])
		p.setRenbanLine([71,72,73])
			
		self.assertEqual(p.countSolutions(test=True),'1:6879432914257625361897685243129475843586918761324','Failed Be Careful What You Squish For')
		
if __name__ == '__main__':
    unittest.main()