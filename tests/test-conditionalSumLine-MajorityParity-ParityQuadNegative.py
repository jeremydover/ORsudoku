import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (312) - Sum Parity Circles Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0005PF
	# Constraints tested: setParityQuadExclusion, setParityQuad, setParityQuadNegative, setConditionalSumLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setParityQuadExclusions([2])
		for x in [(1,7,15),(1,8,9),(2,8,15),(3,1,10),(3,3,8),(3,4,11),(3,7,20),(4,2,13),(4,3,13),(5,1,13),(6,3,21),(6,4),(6,7,12),(7,1,9),(7,2,15),(8,1),(8,3,18),(8,5,15),(8,6,15),(8,7,20)]:
			p.setParityQuad((x[0],x[1]))
			if len(x) > 2:
				p.setConditionalSumLine([(x[0],x[1]),(x[0],x[1]+1),(x[0]+1,x[1]+1),(x[0]+1,x[1])],x[2],[['MajorityParity']],[['Last']])
		p.setParityQuadNegative()
		
		self.assertEqual(p.countSolutions(test=True),'1:385749216674812953921365847263174589519283674748596321837921465156438792492657138','Failed Sudoku Variants Series (312) - Sum Parity Circles Sudoku')
		
if __name__ == '__main__':
    unittest.main()