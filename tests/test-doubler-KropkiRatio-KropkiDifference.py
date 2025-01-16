import unittest
from cellTransformSudoku import doublerSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Zeta and Kappa
	# Author: Twototenth
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000BNH
	# Constraints tested: setKropkiRatio,setKropkiDifference,doubler
	
	def test_puzzle(self):
		p = doublerSudoku(3)
		p.setKropkiDifference(5)
		p.setKropkiRatio(3)
		p.setKropkiWhiteArray([110,120,341,381,441,450,460,561,610,640,661,711,791,830])
		p.setKropkiBlackArray([171,270,340,491,750,770,771,821])
			
		self.assertEqual(p.countSolutions(test=True),'1:794568231328714695651329874576183429149652783832497156985246317413875962267931548100000000000000010000100000000000100000010000001000000000001000010000000000000001','Failed Zeta and Kappa')
		
if __name__ == '__main__':
    unittest.main()