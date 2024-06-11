import unittest
from japaneseSumSudoku import japaneseSumSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Shortcake Sudoku
	# Author: Panthera and Philip Newman
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0006ZS
	# Constraints tested: japaneseSumSudoku, setKropkiBlackArray
	
	def test_puzzle(self):
		p = japaneseSumSudoku(3,2)
		p.setJapaneseSum(1,1,1,[(15,2)])
		p.setJapaneseSum(1,2,1,[(27,2)])
		p.setJapaneseSum(1,3,1,[(41,2)])
		p.setJapaneseSum(1,4,1,[(44,2)])
		p.setJapaneseSum(1,5,1,[(32,2)])
		p.setJapaneseSum(1,6,1,[(9,0),(21,0)])
		p.setJapaneseSum(1,7,1,[(12,0),(22,0)])
		p.setJapaneseSum(1,8,1,[(11,0),(4,0)])
		p.setJapaneseSum(1,9,1,[(7,1),(6,1)])
		p.setJapaneseSum(1,1,0,[(4,1),(7,1)])
		p.setJapaneseSum(2,1,0,[(6,0),(5,0)])
		p.setJapaneseSum(3,1,0,[(14,0),(24,0)])
		p.setJapaneseSum(4,1,0,[(19,0),(5,0)])
		p.setJapaneseSum(5,1,0,[(39,2)])
		p.setJapaneseSum(6,1,0,[(44,2)])
		p.setJapaneseSum(7,1,0,[(42,2)])
		p.setJapaneseSum(8,1,0,[(26,2)])
		p.setJapaneseSum(9,1,0,[(16,2)])
		p.setKropkiBlackArray([241,420,450,541,660,621,751,820])
		
		self.assertEqual(p.countSolutions(test=True),'1:963182457871645239254379186436721598189456723527893641348567912712934865695218374000000101000200110002221111022222100022222200222222220222222200222222000022200000','Failed Shortcake Sudoku')
		
if __name__ == '__main__':
    unittest.main()