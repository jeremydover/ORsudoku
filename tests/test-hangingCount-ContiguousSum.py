import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (267) - Sudoku 1020
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0003ES
	# Constraints tested: setHangingCount, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingCount(1,1,p.Col,1,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(1,2,p.Col,1,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(1,3,p.Col,1,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(1,4,p.Col,0,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(1,5,p.Col,1,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(1,6,p.Col,1,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(1,7,p.Col,0,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(1,8,p.Col,0,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(1,9,p.Col,0,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		
		p.setHangingCount(1,1,p.Row,0,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(2,1,p.Row,1,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(3,1,p.Row,0,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(4,1,p.Row,0,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(5,1,p.Row,2,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(6,1,p.Row,2,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(7,1,p.Row,0,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(8,1,p.Row,0,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		p.setHangingCount(9,1,p.Row,1,[('ContiguousSum',10,p.EQ,3)],[['Last']])
		
		p.setHangingCount(1,9,p.Row,1,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(2,9,p.Row,2,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(3,9,p.Row,2,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(4,9,p.Row,0,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(5,9,p.Row,0,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(6,9,p.Row,0,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(7,9,p.Row,2,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(8,9,p.Row,1,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(9,9,p.Row,1,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		
		p.setHangingCount(9,1,p.Col,1,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(9,2,p.Col,1,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(9,3,p.Col,0,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(9,4,p.Col,0,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(9,5,p.Col,0,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(9,6,p.Col,2,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(9,7,p.Col,0,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(9,8,p.Col,0,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		p.setHangingCount(9,9,p.Col,0,[('ContiguousSum',20,p.EQ,3)],[['Last']])
		
		p.setGivenArray([256,271,345,379,444,529,588,665,737,761,838,852])
		
		self.assertEqual(p.countSolutions(test=True),'1:369142578875963142124578936531489267492716385786235419947851623658324791213697854','Failed Sudoku Variants Series (267) - Sudoku 1020')
		
if __name__ == '__main__':
    unittest.main()