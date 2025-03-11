import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (283) - Next X-Sums Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00046Y
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		for x in [(1,4,p.Col,33),(1,5,p.Col,11),(1,6,p.Col,11),(1,7,p.Col,11),(1,9,p.Row,16),(3,9,p.Row,31),(4,9,p.Row,20),(7,9,p.Row,12),(9,3,p.Col,30),(9,4,p.Col,18),(9,5,p.Col,30),(9,6,p.Col,36),(3,1,p.Row,16),(6,1,p.Row,33),(7,1,p.Row,26),(9,1,p.Row,14)]:
			p.setHangingSum(x[0],x[1],x[2],x[3],[('Location',p.GE,2)],[('ModelVariable',p.cellValues[x[0]-1][x[1]-1]+1)])
		
		self.assertEqual(p.countSolutions(test=True),'1:987642315641753298352918476874129563126534987539876124468391752713285649295467831','Failed Sudoku Variants Series (283) - Next X-Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()