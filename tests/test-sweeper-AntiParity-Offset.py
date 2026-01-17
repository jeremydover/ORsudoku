import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Easy Peasy Sudoku Advent (23) - Parity Poopers
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000QNY
	# Constraints tested: setSweeper, setSweeperNegative, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([322,333,651,662,972,985])
		p.setSweeper(1,1,[('DoNotMatchParity',1)],includeSelf=False,offset=-1)
		p.setSweeper(1,4)
		p.setSweeper(1,7)
		p.setSweeper(1,8)
		p.setSweeper(2,2)
		p.setSweeper(2,4)
		p.setSweeper(2,8)
		p.setSweeper(3,6)
		p.setSweeper(4,7)
		p.setSweeper(5,5)
		p.setSweeper(5,9)
		p.setSweeper(6,1)
		p.setSweeper(6,2)
		p.setSweeper(6,6)
		p.setSweeper(6,7)
		p.setSweeper(7,7)
		p.setSweeper(8,2)
		p.setSweeper(8,5)
		p.setSweeper(8,6)
		p.setSweeperNegative()
		
		self.assertEqual(p.countSolutions(test=True),'1:176285349958473162423691785841739526792564813635812497519328674264157938387946251','Failed Easy Peasy Sudoku Advent (23) - Parity Poopers')
		
if __name__ == '__main__':
    unittest.main()