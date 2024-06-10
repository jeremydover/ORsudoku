import unittest
from japaneseSumSudoku import japaneseSumSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Red Herring (Japanese Sums Sudoku)
	# Author: Panthera
	# Link: https://f-puzzles.com/?id=yeohrlqb
	# Constraints tested: japaneseSumSudoku, setKropkiWhite
	
	def test_puzzle(self):
		p = japaneseSumSudoku(3)
		p.setJapaneseSum(1,1,p.Col,[25,14])
		p.setJapaneseSum(1,2,p.Col,[15,10])
		p.setJapaneseSum(1,3,p.Col,[6,16])
		p.setJapaneseSum(1,4,p.Col,[27,14])
		p.setJapaneseSum(1,5,p.Col,[1,7])
		p.setJapaneseSum(1,6,p.Col,[41])
		p.setJapaneseSum(1,7,p.Col,[28])
		p.setJapaneseSum(1,8,p.Col,[14])
		p.setJapaneseSum(1,9,p.Col,[4])
		p.setJapaneseSum(1,1,p.Row,[18])
		p.setJapaneseSum(2,1,p.Row,[26,5])
		p.setJapaneseSum(3,1,p.Row,[32])
		p.setJapaneseSum(4,1,p.Row,[1,4,20])
		p.setJapaneseSum(5,1,p.Row,[25])
		p.setJapaneseSum(6,1,p.Row,[8])
		p.setJapaneseSum(7,1,p.Row,[3,2,13])
		p.setJapaneseSum(8,1,p.Row,[39])
		p.setJapaneseSum(9,1,p.Row,[26])
		p.setKropkiWhite((2,4,p.Horz))
		
		self.assertEqual(p.countSolutions(test=True),'1:741623589963875421852914376176458932235197864498362157314286795687549213529731648111100000111101000111111100100101110000001111000001110100101100111111000111110000','Failed Red Herring')
		
if __name__ == '__main__':
    unittest.main()
	