import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (315) - Summing Up Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0005WJ
	# Constraints tested: setMaxAscendingRun
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setMaxAscendingRun(1,1,p.Row,17,lengthTest='sum',valueTest='sum')
		p.setMaxAscendingRun(4,1,p.Row,10,lengthTest='sum',valueTest='sum')
		p.setMaxAscendingRun(6,1,p.Row,12,lengthTest='sum',valueTest='sum')
		
		p.setMaxAscendingRun(1,3,p.Col,36,lengthTest='sum',valueTest='sum')
		p.setMaxAscendingRun(1,5,p.Col,33,lengthTest='sum',valueTest='sum')
		p.setMaxAscendingRun(1,8,p.Col,24,lengthTest='sum',valueTest='sum')
		
		p.setMaxAscendingRun(9,1,p.Col,22,lengthTest='sum',valueTest='sum')
		p.setMaxAscendingRun(9,7,p.Col,20,lengthTest='sum',valueTest='sum')
		p.setMaxAscendingRun(9,9,p.Col,12,lengthTest='sum',valueTest='sum')
		
		p.setMaxAscendingRun(4,9,p.Row,9,lengthTest='sum',valueTest='sum')
		p.setMaxAscendingRun(5,9,p.Row,24,lengthTest='sum',valueTest='sum')
		p.setMaxAscendingRun(8,9,p.Row,16,lengthTest='sum',valueTest='sum')
		
		self.assertEqual(p.countSolutions(test=True),'1:863217954952634187714958263546372819197486532328195746439821675285763491671549328','Failed Sudoku Variants Series (315) - Summing Up Sudoku')
		
if __name__ == '__main__':
    unittest.main()