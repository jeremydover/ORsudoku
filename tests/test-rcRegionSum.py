import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (310) - Sum Triplets Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0005LF
	# Constraints tested: setRCRegionSum, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		for x in [(1,1,p.Col,7),(1,2,p.Col,6),(1,3,p.Col,12),(1,4,p.Col,7),(1,5,p.Col,9),(1,6,p.Col,10),(1,7,p.Col,18),(1,8,p.Col,21),(1,9,p.Col,23),(1,1,p.Row,21),(2,1,p.Row,22),(3,1,p.Row,10),(4,1,p.Row,10),(5,1,p.Row,17),(6,1,p.Row,21),(7,1,p.Row,11),(8,1,p.Row,24),(9,1,p.Row,15)]:
			p.setRCRegionSum(x[0],x[1],x[2],x[3])
		
		p.setGivenArray([332,443,665,778])
		
		self.assertEqual(p.countSolutions(test=True),'1:341286759679153248852479316495368172287914563163725984714632895526897431938541627','Failed Sudoku Variants Series (310) - Sum Triplets Sudoku')
		
if __name__ == '__main__':
    unittest.main()