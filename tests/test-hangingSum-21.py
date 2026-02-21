import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Easy Peasy Sudoku Advent (14) - Consecutive Sums
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000QJI
	# Constraints tested: setHangingSum, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,1,p.Col,3,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(1,4,p.Col,10,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(1,5,p.Col,44,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(1,6,p.Col,6,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(1,8,p.Col,41,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(1,9,p.Col,15,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(3,1,p.Row,7,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(4,1,p.Row,17,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(5,1,p.Row,11,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(6,1,p.Row,7,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(7,1,p.Row,45,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(8,1,p.Row,0,[['ConsecutiveNeighbor']],[['Last']])
		p.setHangingSum(9,1,p.Row,0,[['ConsecutiveNeighbor']],[['Last']])
		p.setGivenArray([267,332,384,727,778,844])
		
		self.assertEqual(p.countSolutions(test=True),'1:731824596594637281862951743389742615146583927257196438673219854918475362425368179','Failed Easy Peasy Sudoku Advent (14) - Consecutive Sums')
		
if __name__ == '__main__':
    unittest.main()