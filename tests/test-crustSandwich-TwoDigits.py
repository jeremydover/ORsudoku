import unittest
from crustSandwichSudoku import crustSandwichSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (274) - Mystery Sandwich Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0003QI
	# Constraints tested: crustSandwich, setSandwichSum, setTwoCrustDigits, setGivenArray
	
	def test_puzzle(self):
		p = crustSandwichSudoku(3)
		p.setTwoCrustDigits()
		p.setGivenArray([331,367,375,433,676,732,744,778])
		p.setSandwichSum(1,2,p.Col,19)
		p.setSandwichSum(1,4,p.Col,20)
		p.setSandwichSum(1,5,p.Col,26)
		p.setSandwichSum(1,6,p.Col,25)
		p.setSandwichSum(1,7,p.Col,9)
		p.setSandwichSum(1,8,p.Col,8)
		
		p.setSandwichSum(1,1,p.Row,25)
		p.setSandwichSum(3,1,p.Row,1)
		p.setSandwichSum(4,1,p.Row,7)
		p.setSandwichSum(6,1,p.Row,17)
		p.setSandwichSum(7,1,p.Row,20)
		p.setSandwichSum(9,1,p.Row,16)
			
		self.assertEqual(p.countSolutions(test=True),'1:347952168598614273621387594863729451419865327275143689952471836136298745784536912100001000000000101010100000001010000000000110100001000001000010010100000000010001','Failed Sudoku Variants Series (274) - Mystery Sandwich Sudoku')
		
if __name__ == '__main__':
    unittest.main()