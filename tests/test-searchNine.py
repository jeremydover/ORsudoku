import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Spring Latch
	# Author: Qodec
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000FH6
	# Constraints tested: setSearchNine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSearchNine(1,2,p.Down,[8,9])
		p.setSearchNine(1,3,p.Down,[8,9])
		p.setSearchNine(1,4,p.Down,[8,9])
		p.setSearchNine(1,6,p.Down,[8,9])
		p.setSearchNine(1,7,p.Down,[8,9])
		p.setSearchNine(1,8,p.Down,[8,9])
		p.setSearchNine(2,5,p.Down,[8,9])
		p.setSearchNine(3,2,p.Down,[8,9])
		p.setSearchNine(3,8,p.Down,[8,9])
		p.setSearchNine(4,2,p.Right,[8,9])
		p.setSearchNine(4,3,p.Right,[8,9])
		p.setSearchNine(4,4,p.Down,[8,9])
		p.setSearchNine(4,6,p.Down,[8,9])
		p.setSearchNine(4,7,p.Left,[8,9])
		p.setSearchNine(4,8,p.Left,[8,9])
		p.setSearchNine(5,5,p.Right,[8,9])
		p.setSearchNine(6,5,p.Left,[8,9])
		p.setSearchNine(7,2,p.Right,[8,9])
		p.setSearchNine(7,3,p.Right,[8,9])
		p.setSearchNine(7,4,p.Right,[8,9])
		p.setSearchNine(7,6,p.Left,[8,9])
		p.setSearchNine(7,7,p.Left,[8,9])
		p.setSearchNine(7,8,p.Left,[8,9])
		p.setSearchNine(8,1,p.Up,[8,9])
		p.setSearchNine(8,9,p.Up,[8,9])
		p.setSearchNine(9,5,p.Up,[8,9])
		
		self.assertEqual(p.countSolutions(test=True),'1:381462759729853416564719823932185674645937182817246395476591238258374961193628547','Failed Spring Latch')
		
if __name__ == '__main__':
    unittest.main()