import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (181) - Deformable Kropki Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002MJ
	# Constraints tested: setKopkriGrayArray, setKropkiNegative
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setKropkiGrayArray([120,150,180,181,191,211,220,240,280,321,341,351,361,451,510,551,620,621,721,740,750,770,820,840,850,891,910,940,950,970])
		p.setKropkiNegative()
			
		self.assertEqual(p.countSolutions(test=True),'1:478312965612895734359647281147538629895261473263974158731456892524789316986123547','Failed Sudoku Variants Series (181) - Deformable Kropki Sudoku')
		
if __name__ == '__main__':
    unittest.main()