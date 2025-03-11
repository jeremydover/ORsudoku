import unittest
from ORsudoku import sudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (317) - Sudoku Pair Up
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00061U
	# Constraints tested: setIndexedPairSum
	
	def test_puzzle(self):
		p = sudoku(3)
		p.setIndexedPairSum(1,3,p.Right,10)
		p.setIndexedPairSum(2,5,p.Left,10)
		p.setIndexedPairSum(2,6,p.Right,10)
		p.setIndexedPairSum(2,7,p.Left,10)
		p.setIndexedPairSum(3,8,p.Left,10)
		p.setIndexedPairSum(4,1,p.Down,10)
		p.setIndexedPairSum(4,4,p.Left,10)
		p.setIndexedPairSum(4,6,p.Up,10)
		p.setIndexedPairSum(4,8,p.Down,10)
		p.setIndexedPairSum(5,5,p.Up,10)
		p.setIndexedPairSum(6,6,p.Right,10)
		p.setIndexedPairSum(7,2,p.Up,10)
		p.setIndexedPairSum(7,4,p.Right,10)
		p.setIndexedPairSum(7,5,p.Left,10)
		p.setIndexedPairSum(7,9,p.Left,10)
		p.setIndexedPairSum(8,3,p.Up,10)
		p.setIndexedPairSum(8,9,p.Left,10)
		p.setIndexedPairSum(9,6,p.Up,10)
		p.setIndexedPairSum(9,8,p.Left,10)
		
		self.assertEqual(p.countSolutions(test=True),'1:841967253576132489392584176185293647927648315634751928468325791753419862219876534','Failed Sudoku Variants Series (317) - Sudoku Pair Up')
		
if __name__ == '__main__':
    unittest.main()