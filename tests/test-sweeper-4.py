import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (155) - Treasure Hunt Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002HE
	# Constraints tested: setSweeper, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSweeper(1,1,[('RelatedDigit',1,p.GE,1,1)])
		p.setSweeper(2,7,[('RelatedDigit',1,p.GE,1,1)])
		p.setSweeper(3,3,[('RelatedDigit',1,p.GE,1,1)])
		p.setSweeper(3,6,[('RelatedDigit',1,p.GE,1,1)])
		p.setSweeper(6,3,[('RelatedDigit',1,p.GE,1,1)])
		p.setSweeper(7,2,[('RelatedDigit',1,p.GE,1,1)])
		p.setSweeper(8,9,[('RelatedDigit',1,p.GE,1,1)])
		p.setSweeper(9,8,[('RelatedDigit',1,p.GE,1,1)])
		
		p.setGivenArray([173,287,345,358,391,431,478,536,551,592,662,719,741,776,826,937,955])
		
		self.assertEqual(p.countSolutions(test=True),'1:289741365615293478473586921521379846836415792794862513952134687368927154147658239','Failed Sudoku Variants Series (155) - Treasure Hunt Sudoku')
		
if __name__ == '__main__':
    unittest.main()