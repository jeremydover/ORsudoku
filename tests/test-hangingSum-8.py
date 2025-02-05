import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (251) - Sum by X Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002YX
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,2,p.Col,19,[['All']],[['Indexed',2]])
		p.setHangingSum(1,3,p.Col,27,[['All']],[['Indexed',4]])
		p.setHangingSum(1,4,p.Col,14,[['All']],[['Indexed',3]])
		p.setHangingSum(1,6,p.Col,40,[['All']],[['Indexed',3]])
		p.setHangingSum(1,7,p.Col,21,[['All']],[['Indexed',4]])
		p.setHangingSum(1,8,p.Col,11,[['All']],[['Indexed',2]])
			
		p.setHangingSum(1,9,p.Row,31,[['All']],[['Indexed',5]])
		p.setHangingSum(2,9,p.Row,20,[['All']],[['Indexed',2]])
		p.setHangingSum(3,9,p.Row,34,[['All']],[['Indexed',4]])
		p.setHangingSum(7,9,p.Row,20,[['All']],[['Indexed',4]])
			
		p.setHangingSum(9,2,p.Col,11,[['All']],[['Indexed',2]])
		p.setHangingSum(9,4,p.Col,42,[['All']],[['Indexed',3]])
		p.setHangingSum(9,5,p.Col,26,[['All']],[['Indexed',1]])
		p.setHangingSum(9,6,p.Col,15,[['All']],[['Indexed',3]])
		p.setHangingSum(9,8,p.Col,4,[['All']],[['Indexed',2]])
			
		p.setHangingSum(2,1,p.Row,22,[['All']],[['Indexed',2]])
		p.setHangingSum(6,1,p.Row,28,[['All']],[['Indexed',3]])
		p.setHangingSum(7,1,p.Row,39,[['All']],[['Indexed',4]])
		p.setHangingSum(8,1,p.Row,15,[['All']],[['Indexed',2]])
		p.setHangingSum(9,1,p.Row,28,[['All']],[['Indexed',5]])
		
		self.assertEqual(p.countSolutions(test=True),'1:815369724647521938293487165156238497372945681984716253521894376438672519769153842','Failed Sudoku Variants Series (251) - Sum by X Sudoku')
		
if __name__ == '__main__':
    unittest.main()