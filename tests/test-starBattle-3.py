import unittest
from starBattleSudoku import starBattleSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: 24 Ways to survive a Dutch Advent (11): Star battle Sudoku
	# Author: Eisbär
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0001KX
	# Constraints tested: starBattleSudoku, setGivenArray, irregular
	
	def test_puzzle(self):
		p = starBattleSudoku(3,digitList=[1,2,3,4,5,6,7,8,9],numberOfStars=2,irregular=True)
		p.setRegion([11,12,13,21,22,23,24,31,33])
		p.setRegion([14,15,16,25,26,27,34,35,36])
		p.setRegion([17,18,19,28,29,37,38,39,48])
		p.setRegion([32,41,42,43,51,52,53,61,63])
		p.setRegion([44,45,46,54,55,56,64,65,66])
		p.setRegion([47,49,57,58,59,67,68,69,78])
		p.setRegion([62,71,72,73,81,82,91,92,93])
		p.setRegion([74,75,76,83,84,85,94,95,96])
		p.setRegion([77,79,86,87,88,89,97,98,99])
		p.setGivenArray([179,222,259,285,394,446,492,536,554,571,613,661,716,824,856,887,932])
		
		# Note: the solver generates two solutions to this puzzle. However, in the original puzzle, the solver is to convert two 
		# digits into stars, which are then considered indistinguishable. The computer can't readily do that, so we content ourselves
		# with reporting the two solutions. Note that it is possible that there could be a solution to a puzzle like this (with stars
		# replacing digits) that the solver could not find because there is no reconcilable way to assign distinct digits. Limitation
		# of the solver.
		
		self.assertEqual(p.countSolutions(test=True),'2:568472913427198356983516724719635482256849137394721865675384291841263579132957648865472913427198356983516724719635482256849137394721568678354291541263879132987645','Failed 24 Ways to survive a Dutch Advent (11): Star battle Sudoku')
		
if __name__ == '__main__':
    unittest.main()