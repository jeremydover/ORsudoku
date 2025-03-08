import unittest
from crustSandwichSudoku import crustSandwichSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Six-Inch Sub
	# Author: jeremydover
	# Link: https://sudokupad.app/enfxauq15e
	# Constraints tested: setXDistanceCrust, setXDistanceCrustNegative, crustSandwichSudoku, setSandwichSum
	
	def test_puzzle(self):
		p = crustSandwichSudoku(3)
		p.setTwoCrustDigits()
		for x in [(1,1,p.Col,35),(9,1,p.Row,1),(1,9,p.Row,12),(9,9,p.Col,26),
				(1,5,p.Col,21),(8,9,p.Row,9),(3,1,p.Row,16),
				(1,3,p.Col,25),(4,9,p.Row,15),(7,9,p.Row,0),(6,1,p.Row,19)]:
			p.setSandwichSum(x[0],x[1],x[2],x[3])
			p.setXDistanceCrust(x[0],x[1],x[2])
		for x in [(1,2,p.Col),(1,4,p.Col),(1,6,p.Col),(1,7,p.Col),(1,8,p.Col),(1,9,p.Col),(2,9,p.Row),(3,9,p.Row),(5,9,p.Row),(6,9,p.Row),(9,9,p.Row),(9,1,p.Col),(9,2,p.Col),(9,3,p.Col),(9,4,p.Col),(9,5,p.Col),(9,6,p.Col),(9,7,p.Col),(9,8,p.Col),(1,1,p.Row),(1,2,p.Row),(1,4,p.Row),(1,5,p.Row),(1,7,p.Row),(1,8,p.Row)]:
			p.setXDistanceCrustNegative(x[0],x[1],x[2])
			
		self.assertEqual(p.countSolutions(test=True),'1:875241963924763518361589724692374185147852639583196247459628371736415892218937456100100000010000001000010010001000010000101000010000100000011000000000101101000000','Failed Six-Inch Sub')
		
if __name__ == '__main__':
    unittest.main()