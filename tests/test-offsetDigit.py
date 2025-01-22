import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (394) - Offset 1 and 9
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000C3L
	# Constraints tested: setOffsetDigit, setGivernArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setOffsetDigit(1)
		p.setOffsetDigit(9)
		p.setGivenArray([257,296,344,382,438,466,524,565,588,647,658,676,762,832,854,923])
			
		self.assertEqual(p.countSolutions(test=True),'1:261958734493271856857463921378196245649325187125784693784632519912547368536819472','Failed Sudoku Variants Series (394) - Offset 1 and 9')
		
if __name__ == '__main__':
    unittest.main()