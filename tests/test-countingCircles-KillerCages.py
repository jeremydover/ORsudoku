import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (055) - Black and White Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00024V
	# Constraints tested: setCountingCircles, setCage, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCountingCircles([11,13,14,15,18,19,21,23,24,25,28,29,33,35,36,37,39,42,43,45,46,47,48,52,56,57,58,62,63,65,71,72,73,74,75,77,79,81,85,89,91,95,96,97,99])
		p.setCage([42,52,62,72],29)
		p.setCage([13,23,33,43,63,73],39)
		p.setCage([14,24,74],15)
		p.setCage([15,25,35,45,65,75,85,95],41)
		p.setCage([36,46,56,96],27)
		p.setCage([37,47,57,77,97],32)
		p.setCage([18,28,48,58],30)
		p.setCage([21,23,24,25,28,29],39)
		p.setCage([33,35,36,37,39],30)
		p.setCage([42,43,45,46,47,48],37)
		p.setCage([62,63,65],24)
		p.setCage([71,72,73,74,75,77,79],40)
		p.setCage([81,85,89],22)
		p.setGivenArray([288,393,468,645,716,822])
		
		self.assertEqual(p.countSolutions(test=True),'1:768235194539461287214789653456328971392147865187596342675912438823654719941873526','Failed Sudoku Variants Series (055) - Black and White Sudoku')
		
if __name__ == '__main__':
    unittest.main()