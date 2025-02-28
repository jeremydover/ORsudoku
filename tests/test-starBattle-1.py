import unittest
from starBattleSudoku import starBattleSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (138) - Star Battle Sudoku
	# Author: Richard
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002G5
	# Constraints tested: starBattleSudoku, setGivenArray
	
	def test_puzzle(self):
		p = starBattleSudoku(3,digitList=[1,2,3,4,5,6,7,0,0],starSymbols=[0])
		p.setGivenArray([117,166,193,226,255,282,344,433,497,522,551,586,611,675,764,795,825,853,914,942,971])
		
		self.assertEqual(p.countSolutions(test=True),'1:705126403364050721201473650543602017020517364176340502017064235652731040430205176','Failed Sudoku Variants Series (138) - Star Battle Sudoku')
		
if __name__ == '__main__':
    unittest.main()