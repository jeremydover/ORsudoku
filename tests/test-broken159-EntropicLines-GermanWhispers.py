import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Coprólito
	# Author: Bellsita
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000FUH
	# Constraints tested: setIndexColumn, setEntropicLine, setGermanWhispersLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setIndexColumn(1,True,[1,3,4,5,6,7,9])
		p.setIndexColumn(5,True,[1,3,4,5,6,7,9])
		p.setIndexColumn(9,True,[1,3,4,5,6,7,9])
		p.setEntropicLine([12,22,32])
		p.setEntropicLine([18,28,38])
		p.setEntropicLine([72,82,92])
		p.setEntropicLine([78,88,98])
		p.setEntropicLine([34,35,36])
		p.setEntropicLine([74,75,76])
		p.setEntropicLine([68,69])
		p.setGermanWhispersLine([31,41,42])
		p.setGermanWhispersLine([39,49])
		p.setGermanWhispersLine([34,43,53,63])
		p.setGermanWhispersLine([47,57,67,76])
		p.setGermanWhispersLine([61,71])
		p.setGermanWhispersLine([69,79])
		p.setGermanWhispersLine([84,85])
		
		self.assertEqual(p.countSolutions(test=True),'1:213549876976812345845736219381957624759624183624381957198473562567298431432165798','Failed Fishie')
		
if __name__ == '__main__':
    unittest.main()