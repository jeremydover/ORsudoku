import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (256) - Outside Anti Parity Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000301
	# Constraints tested: setHangingCount, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		# OK, this one is going to require some explanation why it works. Our selection criteria is to select digits which do not have 
		# any parity matches, which forces parity to alternate. BUT, the last digit that alternates is forced to have a following
		# neighbor which is the same parity, so it will not count toward the selection. Hence all of the values are one less than the
		# clues given in the puzzle. Note however, that this last digit is correct: the fact that the previous digit satisfies ParityNone
		# means it has a different parity; while the terminator being ParityRepeat reached means it matches parity with the subsequent
		# digit.
		
		p.setHangingCount(1,5,p.Col,5,[['ParityNone']],[('ParityRepeatReached',1)])
		p.setHangingCount(1,7,p.Col,2,[['ParityNone']],[('ParityRepeatReached',1)])
		p.setHangingCount(1,8,p.Col,1,[['ParityNone']],[('ParityRepeatReached',1)])
		p.setHangingCount(1,9,p.Col,1,[['ParityNone']],[('ParityRepeatReached',1)])
		
		p.setHangingCount(1,9,p.Row,0,[['ParityNone']],[('ParityRepeatReached',1)])
		p.setHangingCount(4,9,p.Row,2,[['ParityNone']],[('ParityRepeatReached',1)])
		
		p.setHangingCount(9,3,p.Col,1,[['ParityNone']],[('ParityRepeatReached',1)])
		p.setHangingCount(9,9,p.Col,2,[['ParityNone']],[('ParityRepeatReached',1)])
		
		p.setHangingCount(2,1,p.Row,1,[['ParityNone']],[('ParityRepeatReached',1)])
		p.setHangingCount(4,1,p.Row,2,[['ParityNone']],[('ParityRepeatReached',1)])
		p.setHangingCount(6,1,p.Row,0,[['ParityNone']],[('ParityRepeatReached',1)])
		p.setHangingCount(7,1,p.Row,3,[['ParityNone']],[('ParityRepeatReached',1)])
		p.setHangingCount(9,1,p.Row,2,[['ParityNone']],[('ParityRepeatReached',1)])
		
		p.setGivenArray([163,321,518,535,569,679,684,762,827,872,971])
			
		self.assertEqual(p.countSolutions(test=True),'1:759163428386294571412587639941376852835429716267851943694712385178635294523948167','Failed Sudoku Variants Series (256) - Outside Anti Parity Sudoku')
		
if __name__ == '__main__':
    unittest.main()