import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (102) - Give me Five
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002B4
	# Constraints tested: setRepellingDigit, setAntiXVV, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setXVVNegative()
		p.setRepellingDigit(1,[6])
		p.setRepellingDigit(2,[7])
		p.setRepellingDigit(3,[8])
		p.setRepellingDigit(4,[9])
		p.setGivenArray([121,132,218,243,317,344,426,435,556,573,665,751,795,881,976,999])
			
		self.assertEqual(p.countSolutions(test=True),'1:912678543854392176736451892365847921471269358298135764629713485543986217187524639','Failed Sudoku Variants Series (102) - Give me Five')
		
if __name__ == '__main__':
    unittest.main()