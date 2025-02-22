import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (353) - Hostile Parity Sandwich Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008LG
	# Constraints tested: setHangingInstance
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingInstance(1,1,p.Col,[1,3,4,6,8],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,2,p.Col,[],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,3,p.Col,[2,4,5],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,4,p.Col,[2,4],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,5,p.Col,[3,4],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,6,p.Col,[3,8],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,7,p.Col,[2,9],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,8,p.Col,[5,7,8],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,9,p.Col,[2,4,7],[['ParityNeither']],[['Last']],negativeConstraint=True)
		
		p.setHangingInstance(1,1,p.Row,[1,4,8],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(2,1,p.Row,[9],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(3,1,p.Row,[2,3,4],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(4,1,p.Row,[2,6],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(5,1,p.Row,[1,2,5,6],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(6,1,p.Row,[2,6,9],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(7,1,p.Row,[],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(8,1,p.Row,[1,6],[['ParityNeither']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(9,1,p.Row,[4,6,9],[['ParityNeither']],[['Last']],negativeConstraint=True)
		
		self.assertEqual(p.countSolutions(test=True),'1:538794126496213758127568349843927561961485273752136984615342897374859612289671435','Failed Sudoku Variants Series (353) - Hostile Parity Sandwich Sudoku')
		
if __name__ == '__main__':
    unittest.main()