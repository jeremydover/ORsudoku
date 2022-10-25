import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Zeta and Kappa
	# Author: Twototenth
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000BNH
	# Constraints tested: setKropkiRatio,setKropkiDifference,doubler
	
	def test_puzzle(self):
		p = ORsudoku.doublerSudoku(3)
		p.setKropkiDifference(5)
		p.setKropkiRatio(3)
		p.setKropkiWhiteArray([110,120,341,381,441,450,460,561,610,640,661,711,791,830])
		p.setKropkiBlackArray([171,270,340,491,750,770,771,821])
			
		self.assertEqual(p.findSolution(test=True),'*7*945682313287146*9*5651*3*29874576183*4*291496*5*278383*2*49715698524*6*3174*1*387596226793154*8*','Failed Zeta and Kappa')
		
if __name__ == '__main__':
    unittest.main()