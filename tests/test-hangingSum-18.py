import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (170) - X? Sums Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002K4
	# Constraints tested: setHangingSum, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		s = p.model.NewIntVar(0,45,'')
		p.setHangingSum(1,1,p.Col,s,[['All']],[('Indexed',1)])
		p.setHangingSum(1,2,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(1,3,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(1,4,p.Col,s,[['All']],[('Indexed',1)])
		p.setHangingSum(1,5,p.Col,s,[['All']],[('Indexed',1)])
		p.setHangingSum(1,6,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(1,7,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(1,8,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(1,9,p.Col,s,[['All']],[('Indexed',1)])
		p.setHangingSum(9,1,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(9,2,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(9,3,p.Col,s,[['All']],[('Indexed',1)])
		p.setHangingSum(9,4,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(9,5,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(9,6,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(9,7,p.Col,s,[['All']],[('Indexed',1)])
		p.setHangingSum(9,8,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(9,9,p.Col,s,[['All']],[('Indexed',1)],comparator=p.NE)
	
		p.setHangingSum(1,1,p.Row,s,[['All']],[('Indexed',1)])
		p.setHangingSum(2,1,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(3,1,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(4,1,p.Row,s,[['All']],[('Indexed',1)])
		p.setHangingSum(5,1,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(6,1,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(7,1,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(8,1,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(9,1,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(1,9,p.Row,s,[['All']],[('Indexed',1)])
		p.setHangingSum(2,9,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(3,9,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(4,9,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(5,9,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(6,9,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(7,9,p.Row,s,[['All']],[('Indexed',1)])
		p.setHangingSum(8,9,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		p.setHangingSum(9,9,p.Row,s,[['All']],[('Indexed',1)],comparator=p.NE)
		
		p.setGivenArray([256,539,573,751,811,892])
		
		self.assertEqual(p.countSolutions(test=True),'1:593472186217863945846951723631729854729548361458136279982615437164387592375294618','Failed Sudoku Variants Series (170) - X? Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()