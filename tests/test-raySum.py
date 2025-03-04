import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (378) - Shifted X-Sums Sudoku
	# Author: Richard
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000AOP
	# Constraints tested: setRaySum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRaySum(1,1,p.Row,5,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		p.setRaySum(8,1,p.Row,22,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		
		p.setRaySum(1,1,p.Col,8,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		p.setRaySum(1,4,p.Col,13,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		p.setRaySum(1,5,p.Col,41,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		p.setRaySum(1,6,p.Col,15,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		p.setRaySum(1,8,p.Col,13,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		
		p.setRaySum(2,9,p.Row,9,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		p.setRaySum(9,9,p.Row,20,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		
		p.setRaySum(9,2,p.Col,3,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		p.setRaySum(9,4,p.Col,12,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		p.setRaySum(9,5,p.Col,23,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		p.setRaySum(9,6,p.Col,1,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		p.setRaySum(9,9,p.Col,10,['Indexed',1],[['All']],[['Indexed',1]],backward=False)
		
		self.assertEqual(p.findSolution(test=True),'418236759725419368396578412241395876657182934839764125164957283572843691983621547','Failed Sudoku Variants Series (378) - Shifted X-Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()