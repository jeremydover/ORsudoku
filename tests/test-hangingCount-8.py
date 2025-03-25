import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (241) - Outside Killer Pair Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002WK
	# Constraints tested: setHangingCount, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingCount(1,1,p.Col,1,[['ContiguousSum',13,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(1,2,p.Col,1,[['ContiguousSum',3,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(1,3,p.Col,1,[['ContiguousSum',6,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(1,4,p.Col,1,[['ContiguousSum',5,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(1,6,p.Col,1,[['ContiguousSum',17,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(1,7,p.Col,1,[['ContiguousSum',11,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(1,8,p.Col,1,[['ContiguousSum',12,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(1,9,p.Col,1,[['ContiguousSum',14,p.EQ,2]],[['Last']],comparator=p.GE)
		
		p.setHangingCount(1,1,p.Row,1,[['ContiguousSum',15,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(2,1,p.Row,1,[['ContiguousSum',10,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(3,1,p.Row,1,[['ContiguousSum',17,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(4,1,p.Row,1,[['ContiguousSum',4,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(5,1,p.Row,1,[['ContiguousSum',10,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(6,1,p.Row,1,[['ContiguousSum',15,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(7,1,p.Row,1,[['ContiguousSum',11,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(8,1,p.Row,1,[['ContiguousSum',17,p.EQ,2]],[['Last']],comparator=p.GE)
		p.setHangingCount(9,1,p.Row,1,[['ContiguousSum',17,p.EQ,2]],[['Last']],comparator=p.GE)
		
		p.setGivenArray([117,138,171,192,241,264,518,531,572,599,657,748,763,837,876])
			
		self.assertEqual(p.countSolutions(test=True),'1:738965142629134857514728963472589316851346279396271485165893724987452631243617598','Failed Sudoku Variants Series (241) - Outside Killer Pair Sudoku')
		
if __name__ == '__main__':
    unittest.main()