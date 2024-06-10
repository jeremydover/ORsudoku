import unittest
from japaneseSumSudoku import japaneseSumSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Have Courage
	# Author: Panthera
	# Link: https://sudokupad.app/hd99afq5a0
	# Constraints tested: japaneseSumSudoku
	
	def test_puzzle(self):
		p = japaneseSumSudoku(3,2)
		p.setJapaneseSum(1,1,p.Col,[(2,1),(12,2),(4,2)])
		p.setJapaneseSum(1,2,p.Col,[(16,2)])
		p.setJapaneseSum(1,3,p.Col,[(18,2)])
		p.setJapaneseSum(1,4,p.Col,[(19,2)])
		p.setJapaneseSum(1,5,p.Col,[(4,2),(16,1),(11,2)])
		p.setJapaneseSum(1,6,p.Col,[(8,1),(15,2),(11,1),(10,2)])
		p.setJapaneseSum(1,7,p.Col,[(5,1),(14,2),(15,1),(6,2)])
		p.setJapaneseSum(1,8,p.Col,[(1,1),(17,2),(11,1),(14,2)])
		p.setJapaneseSum(1,9,p.Col,[(9,2),(21,1)])
		p.setJapaneseSum(2,1,p.Row,[(4,2),(14,1),(9,2)])
		p.setJapaneseSum(3,1,p.Row,[(7,1),(14,2),(6,1)])
		p.setJapaneseSum(4,1,p.Row,[(2,1),(5,1),(13,2),(8,1)])
		p.setJapaneseSum(5,1,p.Row,[(3,2),(1,1),(19,2),(5,1)])
		p.setJapaneseSum(6,1,p.Row,[(23,2),(22,1)])
		p.setJapaneseSum(7,1,p.Row,[(21,2),(20,1)])
		p.setJapaneseSum(8,1,p.Row,[(34,2)])
		p.setJapaneseSum(9,1,p.Row,[(7,2),(6,2),(7,2),(9,2)])
		
		self.assertEqual(p.countSolutions(test=True),'1:894561327672348519513972486246759138387214965951836742169425873728193654435687291000000000000021112000012221100012221200012221222211111022221110022222220220202020','Failed Have Courage')
		
if __name__ == '__main__':
    unittest.main()