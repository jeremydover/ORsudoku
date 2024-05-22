import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Competitive Tetris
	# Author: Bremster
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000BCI
	# Constraints tested: setIndexColumn,setLockoutLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setIndexColumn(1)
		p.setIndexColumn(5)
		p.setIndexColumn(9)
		p.setXSudokuMain()
		p.setXSudokuOff()
		p.setCage([22,32,33],9)
		p.setCage([38,48,49],6)
		p.setCage([44,54,64],9)
		p.setCage([46,56,66],19)
		p.setCage([61,62,72],14)
		p.setCage([77,78,88],7)
			
		self.assertEqual(p.countSolutions(test=True),'1:576413298138972564942865731897654312361297485425138679783549126659721843214386957','Failed Competitive Tetris')
		
if __name__ == '__main__':
    unittest.main()