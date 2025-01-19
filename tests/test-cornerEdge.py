import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Corner/Edge
	# Author: ropeko
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008UX
	# Constraints tested: setGivenArray, setCornerEdge
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([168,345,417,476,639,691,766,944])
		p.setCornerEdge(1,p.Corner,[1,4,5])
		p.setCornerEdge(1,p.Edge,[2,3,6])
		p.setCornerEdge(2,p.Edge,[2,7])
		p.setCornerEdge(3,p.Corner,[3,4,6])
		p.setCornerEdge(3,p.Edge,[1,2,5,9])
		p.setCornerEdge(4,p.Edge,[2,5,6,8])
		p.setCornerEdge(6,p.Edge,[3,5,7,9])
		p.setCornerEdge(7,p.Corner,[2,3,5])
		p.setCornerEdge(7,p.Edge,[1,4,6])
		p.setCornerEdge(8,p.Edge,[2,8,9])
		p.setCornerEdge(9,p.Corner,[1,3,5])
		p.setCornerEdge(9,p.Edge,[2,4,6,8])
		
		self.assertEqual(p.countSolutions(test=True),'1:125678493976134582438529716754912638812365947369847251543786129691253874287491365','Failed Sudoku Corner/Edge')
		
if __name__ == '__main__':
    unittest.main()