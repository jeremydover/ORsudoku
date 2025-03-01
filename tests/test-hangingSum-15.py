import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (385) - Consecutive Sums Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000BB2
	# Constraints tested: setHangingSum, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,2,p.Col,0,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(1,3,p.Col,5,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(1,5,p.Col,0,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(1,7,p.Col,9,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(1,8,p.Col,45,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(1,9,p.Col,27,[['ConsecutiveNeighbor']],[['Last']])
		
		p.setHangingSum(2,1,p.Row,45,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(3,1,p.Row,37,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(5,1,p.Row,9,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(7,1,p.Row,40,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(8,1,p.Row,45,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(9,1,p.Row,35,[['ConsecutiveNeighbor']],[['Last']])
		
		p.setGivenArray([321,337,777,789])
	
		self.assertEqual(p.countSolutions(test=True),'1:286435971349871265517629834174568329638294517952317486423156798765982143891743652','Failed Sudoku Variants Series (385) - Consecutive Sums Sudoku')
		
if __name__ == '__main__':
    unittest.main()