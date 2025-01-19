import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (322) - Ascending Starters Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0006FK
	# Constraints tested: setAscendingStarter
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setAscendingStarter(1,4,p.Col,14)
		p.setAscendingStarter(1,7,p.Col,26)
		p.setAscendingStarter(1,9,p.Row,22)
		p.setAscendingStarter(5,9,p.Row,20)
		p.setAscendingStarter(7,9,p.Row,10)
		p.setAscendingStarter(9,8,p.Col,11)
		p.setAscendingStarter(9,6,p.Col,6)
		p.setAscendingStarter(9,5,p.Col,6)
		p.setAscendingStarter(9,4,p.Col,25)
		p.setAscendingStarter(9,2,p.Col,10)
		p.setAscendingStarter(7,1,p.Row,22)
		p.setAscendingStarter(6,1,p.Row,13)
		p.setAscendingStarter(5,1,p.Row,12)
		p.setAscendingStarter(2,1,p.Row,11)
		
		self.assertEqual(p.countSolutions(test=True),'1:695387421473512698812694753734258916129463875586971342257839164361745289948126537','Failed Sudoku Variants Series (322) - Ascending Starters Sudoku')
		
if __name__ == '__main__':
    unittest.main()