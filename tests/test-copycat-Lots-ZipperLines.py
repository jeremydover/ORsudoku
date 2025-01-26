import unittest
from cellTransformSudoku import copycatSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Copycat Collaboration
	# Author: Scojo and friends
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000IP9
	# Constraints tested: copycatSudoku, setZipperLine, setLotLine
	
	def test_puzzle(self):
		p = copycatSudoku(3)
		p.setZipperLine([11,22,33])
		p.setLotLine([11,22,33],3,'Odd')
		p.setZipperLine([23,14,15,24,25,16,17])
		p.setLotLine([23,14,15,24,25,16,17],1,'Odd')
		p.setZipperLine([26,27,28,38,48])
		p.setZipperLine([52,42,41,51,61,62,63,53,43])
		p.setLotLine([52,42,41,51,61,62,63,53,43],9,'Odd')
		p.setZipperLine([55,56,66,65,64,54,44,45,46])
		p.setZipperLine([59,69,79,89,78])
		p.setLotLine([59,69,79,89,78],2,'Odd')
		p.setZipperLine([68,67,77])
		p.setLotLine([68,67,77],3,'Odd')
		p.setZipperLine([73,72,71,81,91,92,93,83,82])
		p.setZipperLine([85,95,96,86,76,75,74,84,94])
		p.setLotLine([85,95,96,86,76,75,74,84,94],4,'Odd')
		p.setZipperLine([88,99,98])
			
		self.assertEqual(p.countSolutions(test=True),'1:796512384534768129182493567379824615241657893865931472617349258428175936953286741100000000000001000000000010001000000000010000000000100000100000010000000000000001','Failed Copycat Collaboration')
		
if __name__ == '__main__':
    unittest.main()
	
