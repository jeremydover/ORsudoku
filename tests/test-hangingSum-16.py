import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (299) - Teleportation Sums Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0004X4
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		for x in [(1,2,p.Col,9),(1,3,p.Col,14),(1,5,p.Col,5),(1,6,p.Col,5),(1,7,p.Col,10),(1,8,p.Col,11),(2,9,p.Row,10),(3,9,p.Row,10),(4,9,p.Row,9),(5,9,p.Row,12),(6,9,p.Row,5),(7,9,p.Row,12),(8,9,p.Row,9),(9,1,p.Col,8),(9,2,p.Col,2),(9,3,p.Col,14),(9,9,p.Col,12),(3,1,p.Row,10),(5,1,p.Row,11),(9,1,p.Row,8)]:
			var = p.model.NewIntVar(min(p.digits),max(p.digits),'')
			p.setHangingSum(x[0],x[1],x[2],var,[('Location','Indexed',1)],[['Last']])
			p.model.Add(var + p.cellValues[x[0]-1][x[1]-1] == x[3])
		
		self.assertEqual(p.countSolutions(test=True),'1:956734821423185697781926354237841965549263178168579432372618549894357216615492783','Failed Sudoku Variants Series (299) - Teleportation Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()