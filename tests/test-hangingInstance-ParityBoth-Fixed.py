import unittest
from ORsudoku import sudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (333) - Odd or Even Sandwich Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000792
	# Constraints tested: setHangingInstance
	
	def test_puzzle(self):
		p = sudoku(3)
		p.setHangingInstance(1,1,p.Col,[1,2,3],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,2,p.Col,[4,5],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,3,p.Col,[6],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,4,p.Col,[7],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,5,p.Col,[8,9],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,6,p.Col,[1],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,7,p.Col,[2,8],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,8,p.Col,[3,5],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(1,9,p.Col,[],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		
		p.setHangingInstance(1,1,p.Row,[8],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(2,1,p.Row,[],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(3,1,p.Row,[6,8],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(4,1,p.Row,[2,3,8],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(5,1,p.Row,[2,6],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(6,1,p.Row,[],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(7,1,p.Row,[3,6],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(8,1,p.Row,[3],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
		p.setHangingInstance(9,1,p.Row,[1,5],[('ParityBoth','Fixed',1)],[['Last']],negativeConstraint=True)
			
		self.assertEqual(p.countSolutions(test=True),'1:914238576265147389783569241129853764378496125546712893432681957851974632697325418','Failed Sudoku Variants Series (333) - Odd or Even Sandwich Sudoku')
		
if __name__ == '__main__':
    unittest.main()