import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (244) - Outside Consecutive Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002XC
	# Constraints tested: setHangingCount, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingCount(1,1,p.Col,2,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(1,2,p.Col,0,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(1,3,p.Col,1,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(1,4,p.Col,0,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(1,5,p.Col,1,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(1,6,p.Col,3,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(1,7,p.Col,2,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(1,8,p.Col,1,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(1,9,p.Col,0,[['ConsecutiveBefore']],[['Last']])
		
		p.setHangingCount(1,1,p.Row,2,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(2,1,p.Row,3,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(3,1,p.Row,3,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(4,1,p.Row,2,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(5,1,p.Row,1,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(6,1,p.Row,3,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(7,1,p.Row,3,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(8,1,p.Row,4,[['ConsecutiveBefore']],[['Last']])
		p.setHangingCount(9,1,p.Row,2,[['ConsecutiveBefore']],[['Last']])
		
		p.setGivenArray([112,198,224,258,287,346,365,373,437,475,521,586,639,671,736,747,769,822,856,889,917,996])
			
		self.assertEqual(p.countSolutions(test=True),'1:265973418943281675178645329437196582512837964689452137856719243324568791791324856','Failed Sudoku Variants Series (244) - Outside Consecutive Sudoku')
		
if __name__ == '__main__':
    unittest.main()