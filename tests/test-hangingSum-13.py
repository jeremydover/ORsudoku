import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (121) - Odd Even Frame Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002E6
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,1,p.Col,10,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(1,2,p.Col,12,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(1,3,p.Col,8,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(1,4,p.Col,12,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(1,5,p.Col,8,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(1,6,p.Col,13,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(1,7,p.Col,9,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(1,8,p.Col,12,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(1,9,p.Col,4,[['Uniparity']],[['Fixed',3]])
		
		p.setHangingSum(1,9,p.Row,17,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(2,9,p.Row,12,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(3,9,p.Row,8,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(4,9,p.Row,10,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(5,9,p.Row,1,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(6,9,p.Row,17,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(7,9,p.Row,10,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(8,9,p.Row,6,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(9,9,p.Row,6,[['Uniparity']],[['Fixed',3]])
		
		p.setHangingSum(9,1,p.Col,4,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(9,2,p.Col,7,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(9,3,p.Col,14,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(9,4,p.Col,14,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(9,5,p.Col,8,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(9,6,p.Col,14,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(9,7,p.Col,4,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(9,8,p.Col,12,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(9,9,p.Col,12,[['Uniparity']],[['Fixed',3]])
		
		p.setHangingSum(1,1,p.Row,7,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(2,1,p.Row,9,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(3,1,p.Row,6,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(4,1,p.Row,14,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(5,1,p.Row,4,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(6,1,p.Row,8,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(7,1,p.Row,13,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(8,1,p.Row,12,[['Uniparity']],[['Fixed',3]])
		p.setHangingSum(9,1,p.Row,14,[['Uniparity']],[['Fixed',3]])
		
		# Note: the solver produces two copies of the same solution, because there is one clue where either the evens or the odds could be picked. The solver has no way of determining which such selection is canonical.
		
		self.assertEqual(p.countSolutions(test=True),'2:687421953531897426492365871958132764743659218216784539175946382369278145824513697687421953531897426492365871958132764743659218216784539175946382369278145824513697','Failed Sudoku Variants Series (121) - Odd Even Frame Sudoku')
		
if __name__ == '__main__':
    unittest.main()