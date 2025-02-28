import unittest
from starBattleSudoku import starBattleSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sub Battle Sudoku
	# Author: jeremydover
	# https://puzzling.stackexchange.com/questions/111038/sub-battle-sudoku
	# Constraints tested: starBattleSudoku, setGiven, setSandwichSum
	
	def test_puzzle(self):
		p = starBattleSudoku(3,digitList=[1,2,3,4,5,6,7,8,9],starSymbols=[1,9],irregular=True)
		p.setRegion([11,12,13,21,22,23,32,33,34])
		p.setRegion([14,15,16,17,24,25,26,35,45])
		p.setRegion([18,19,28,29,38,39,48,49,59])
		p.setRegion([27,36,37,43,44,46,54,55,56])
		p.setRegion([31,41,42,51,52,53,62,63,64])
		p.setRegion([47,57,58,66,67,68,76,77,87])
		p.setRegion([61,71,72,73,74,81,83,84,91])
		p.setRegion([65,75,82,85,86,92,93,94,95])
		p.setRegion([69,78,79,88,89,96,97,98,99])
		
		p.setSandwichSum(1,1,p.Col,11)
		p.setSandwichSum(1,2,p.Col,29)
		p.setSandwichSum(1,5,p.Col,10)
		p.setSandwichSum(1,7,p.Col,8)
		p.setSandwichSum(1,9,p.Col,12)
		
		p.setSandwichSum(2,1,p.Row,26)
		p.setSandwichSum(4,1,p.Row,31)
		p.setSandwichSum(7,1,p.Row,7)
		p.setSandwichSum(9,1,p.Row,29)
		
		p.setGiven(999)
		
		self.assertEqual(p.countSolutions(test=True),'1:563941278794368512482179356138257694859614723326785941971423865245896137617532489','Failed Sub Battle Sudoku')
		
if __name__ == '__main__':
    unittest.main()