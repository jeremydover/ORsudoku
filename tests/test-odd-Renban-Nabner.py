import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Forwards & Backwards
	# Author: zetamath
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0006Y1
	# Constraints tested: setRenbanLine, setNabnerLine, setGiven, setOdd
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setOdd(93)
		p.setGiven(943)
		p.setRenbanLine([13,23,33,43])
		p.setRenbanLine([15,16,26,25])
		p.setRenbanLine([31,42,52,62])
		p.setRenbanLine([37,38,39])
		p.setRenbanLine([48,49,59])
		p.setRenbanLine([55,56,66])
		p.setRenbanLine([67,76,86])
		p.setRenbanLine([72,82,93,94])
		p.setRenbanLine([74,73,83])
		p.setRenbanLine([77,88])
		p.setNabnerLine([11,21,22,32])
		p.setNabnerLine([27,28,29,19])
		p.setNabnerLine([44,35,36,46])
		p.setNabnerLine([53,63,64,65])
		p.setNabnerLine([57,58,68,78])
		p.setNabnerLine([71,81,91,92])
		p.setNabnerLine([87,97,98,99])
		
		self.assertEqual(p.countSolutions(test=True),'1:694157823835264791712983564483621975259478316167539482348716259926845137571392648','Failed Forwards & Backwards')
		
if __name__ == '__main__':
    unittest.main()