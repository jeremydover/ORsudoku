import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (350) - David and Goliath Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008HN
	# Constraints tested: setDavidAndGoliath, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		pairs=[[13,23],[17,27],[24,34],[28,38],[31,32],[35,45],[39,49],[42,43],[46,56],[53,54],[57,67],[64,65],[68,78],[71,72],[75,76],[79,89],[82,83],[86,87],[93,94],[97,98]]
		for x in pairs:
			p.setDavidAndGoliath(x)
		p.setGivenArray([262,295,334,378,444,489,557,593,629,668,731,777,847,886,922,954,999])
		
		self.assertEqual(p.countSolutions(test=True),'1:275184936189362475634957821856431297412579683397628154561293748948715362723846519','Failed Sudoku Variants Series (350) - David and Goliath Sudoku')
		
if __name__ == '__main__':
    unittest.main()