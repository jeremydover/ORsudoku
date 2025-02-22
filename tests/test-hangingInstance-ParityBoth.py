import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (352) - Friendly Parity Sandwich Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008LG
	# Constraints tested: setHangingInstance
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingInstance(1,1,p.Col,[3,9],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,2,p.Col,[7],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,3,p.Col,[1,2,8],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,4,p.Col,[1,3,4],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,5,p.Col,[2,7,9],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,6,p.Col,[],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,7,p.Col,[1,5,6],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,8,p.Col,[],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,9,p.Col,[2,9],[['ParityBoth']],[['Last']],negativeConstraint=True)
		
		p.setHangingInstance(1,1,p.Row,[7],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(2,1,p.Row,[3],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(3,1,p.Row,[3],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(4,1,p.Row,[1,2,3],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(5,1,p.Row,[],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(6,1,p.Row,[6],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(7,1,p.Row,[7],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(8,1,p.Row,[7],[['ParityBoth']],[['Last']],negativeConstraint=True)
		p.setHangingInstance(9,1,p.Row,[4],[['ParityBoth']],[['Last']],negativeConstraint=True)
		
		self.assertEqual(p.countSolutions(test=True),'1:245617983813942576796853142962471358358296417174538629437189265681325794529764831','Failed Sudoku Variants Series (352) - Friendly Parity Sandwich Sudoku')
		
if __name__ == '__main__':
    unittest.main()