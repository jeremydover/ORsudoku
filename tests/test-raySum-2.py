import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Sudoku Variants Series (303) - Assorted Sandwiches Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00054S
	# Constraints tested: setRaySum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		for x in [(1,2,p.Col,29),(1,3,p.Col,36),(1,5,p.Col,27),(1,6,p.Col,12),(1,7,p.Col,29),(1,8,p.Col,28),(1,9,p.Col,16),(1,1,p.Row,35),(2,1,p.Row,15),(3,1,p.Row,36),(4,1,p.Row,16),(7,1,p.Row,24),(8,1,p.Row,31),(9,1,p.Row,13)]:
			y = x[3] // 10
			z = x[3] % 10
			p.setRaySum(x[0],x[1],x[2],x[3],('DigitReached',y),[['All']],[('DigitReached',z)],includeTerminator=False,forceTermination=False,failedTerminationBehavior='zero',includeSelf=False)
		
		self.assertEqual(p.countSolutions(test=True),'1:256974183891236457347518296538197642712465839964382715489723561175649328623851974','Failed Sudoku Variants Series (303) - Assorted Sandwiches Sudoku')
		
if __name__ == '__main__':
    unittest.main()