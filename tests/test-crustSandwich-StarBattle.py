import unittest
from crustSandwichSudoku import crustSandwichSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (319) - Star Battle Sandwich
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00066E
	# Constraints tested: setCrustStarBattle, setCrustSum, setSandwichSum
	
	def test_puzzle(self):
		p = crustSandwichSudoku(3,enforceRegions=True)
		p.setCrustStarBattle()
		p.setCrustSum(1,1,p.Col,7)
		p.setCrustSum(1,3,p.Col,11)
		p.setCrustSum(1,5,p.Col,9)
		p.setCrustSum(1,6,p.Col,12)
		p.setCrustSum(1,8,p.Col,8)
		
		p.setCrustSum(5,1,p.Row,12)
		p.setCrustSum(8,1,p.Row,16)
		
		p.setSandwichSum(1,9,p.Row,24)
		p.setSandwichSum(3,9,p.Row,7)
		p.setSandwichSum(4,9,p.Row,19)
		p.setSandwichSum(7,9,p.Row,12)
		p.setSandwichSum(8,9,p.Row,25)
		
		p.setSandwichSum(9,2,p.Col,9)
		p.setSandwichSum(9,5,p.Col,8)
		p.setSandwichSum(9,6,p.Col,8)
		p.setSandwichSum(9,7,p.Col,28)
		p.setSandwichSum(9,9,p.Col,25)
		
		self.assertEqual(p.countSolutions(test=True),'1:125973846793846125864215379476398251531427698982651734247169583319582467658734912010000100000100001010001000000100010100001000001000010100010000001000001000010100','Failed Sudoku Variants Series (319) - Star Battle Sandwich')
		
if __name__ == '__main__':
    unittest.main()