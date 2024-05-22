import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: XX-Sums
	# Author: jeremydover
	# Link: https://f-puzzles.com/?id=2jg39x9u
	# Link: https://tinyurl.com/2rp6ad95
	# Constraints tested: setDoubleXSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
	
		p.setDoubleXSum(1,1,0,15)
		p.setDoubleXSum(1,2,1,15)
		p.setDoubleXSum(1,3,1,15)
		p.setDoubleXSum(3,1,0,28)
		p.setDoubleXSum(9,1,0,47)
		p.setDoubleXSum(1,9,1,29)
		p.setDoubleXSum(7,1,0,55)
		p.setDoubleXSum(5,1,0,53)
		p.setDoubleXSum(1,6,1,75)
		p.setDoubleXSum(1,5,1,72)
		p.setDoubleXSum(2,1,0,73)
		
		self.assertEqual(p.countSolutions(test=True),'1:341879652829651437657423891136592784598714326472368915283146579965237148714985263','Failed XX-Sums')
		
if __name__ == '__main__':
    unittest.main()