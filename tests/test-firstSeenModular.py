import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (444) - Easy as 369
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000PGX
	# Constraints tested: setFirstSeenModular, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([124,171,212,287,352,494,538,682,714,777,822,868,881,941])
		p.setFirstSeenModular(1,2,p.Col,6)
		p.setFirstSeenModular(1,4,p.Col,3)
		p.setFirstSeenModular(1,5,p.Col,3)
		p.setFirstSeenModular(1,6,p.Col,3)
		p.setFirstSeenModular(1,8,p.Col,3)
		p.setFirstSeenModular(1,1,p.Row,6)
		p.setFirstSeenModular(3,1,p.Row,9)
		p.setFirstSeenModular(4,1,p.Row,6)
		p.setFirstSeenModular(6,1,p.Row,3)
		p.setFirstSeenModular(7,1,p.Row,3)
		p.setFirstSeenModular(9,1,p.Row,9)
		
		self.assertEqual(p.countSolutions(test=True),'1:649375182213684975857921436562713894198246357374859621481532769726498513935167248','Failed Sudoku Variants Series (444) - Easy as 369')
		
if __name__ == '__main__':
    unittest.main()