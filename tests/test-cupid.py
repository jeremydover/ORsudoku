import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Cupid Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002JT
	# Constraints tested: setCupid, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCupid(1,4,2,3)
		p.setCupid(2,4,3,3)
		p.setCupid(2,6,1,7)
		p.setCupid(3,1,4,2)
		p.setCupid(3,4,4,3)
		p.setCupid(3,6,2,7)
		p.setCupid(3,9,4,8)
		p.setCupid(4,1,3,2)
		p.setCupid(4,4,5,3)
		p.setCupid(4,6,3,7)
		p.setCupid(4,9,3,8)
		p.setCupid(5,4,6,3)
		p.setCupid(5,6,4,7)
		p.setCupid(6,1,7,2)
		p.setCupid(6,4,7,3)
		p.setCupid(6,6,5,7)
		p.setCupid(6,9,7,8)
		p.setCupid(7,1,6,2)
		p.setCupid(7,4,8,3)
		p.setCupid(7,6,6,7)
		p.setCupid(7,9,6,8)
		p.setCupid(8,4,9,3)
		p.setCupid(8,6,7,7)
		p.setCupid(9,6,8,7)
		p.setGivenArray([139,151,213,297,324,352,388,422,453,486,514,599,623,654,681,729,755,784,812,896,956,979])
		
		self.assertEqual(p.countSolutions(test=True),'1:859713624312486597647925183728139465461578239935642718196857342274391856583264971','Failed Cupid Sudoku')
		
if __name__ == '__main__':
    unittest.main()