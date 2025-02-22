import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (020) - Even Sandwich
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0001XX
	# Constraints tested: setHangingInstance, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingInstance(1,1,p.Col,[9],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,2,p.Col,[6],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,3,p.Col,[],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,4,p.Col,[6],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,5,p.Col,[8],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,6,p.Col,[9],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,7,p.Col,[5],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,8,p.Col,[7],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,9,p.Col,[1],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		
		p.setHangingInstance(1,1,p.Row,[7],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(2,1,p.Row,[],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(3,1,p.Row,[3],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(4,1,p.Row,[9],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(5,1,p.Row,[2],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(6,1,p.Row,[],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(7,1,p.Row,[5],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(8,1,p.Row,[3],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(9,1,p.Row,[7],[('ParityBoth',0)],[['Last']],negativeConstraint=True)
		
		self.assertEqual(p.countSolutions(test=True),'1:346152789851769324297834615134698257582417936769523148623985471978341562415276893','Failed Sudoku Variants Series (020) - Even Sandwich')
		
if __name__ == '__main__':
    unittest.main()