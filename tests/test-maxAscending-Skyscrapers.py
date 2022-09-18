import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Elevator Up
	# Author: jeremydover
	# Link: https://tinyurl.com/2sba7jaf
	# Link: https://f-puzzles.com/?id=2go4kegg
	# Constraints tested: setSkyscraper, setMaxAscending
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSkyscraper(1,1,p.Row,5)
		p.setMaxAscending(1,9,p.Row,5)
		p.setSkyscraper(2,1,p.Row,6)
		p.setMaxAscending(2,9,p.Row,4)
		p.setSkyscraper(3,1,p.Row,3)
		p.setMaxAscending(3,9,p.Row,7)
		p.setSkyscraper(1,5,p.Col,3)
		p.setMaxAscending(9,5,p.Col,6)
		
		p.setSkyscraper(9,1,p.Row,5)
		p.setMaxAscending(9,9,p.Row,4)
		
		p.setSkyscraper(9,6,p.Col,4)
		p.setSkyscraper(9,4,p.Col,2)
		
		p.setMaxAscending(9,2,p.Col,2)
		p.setMaxAscending(9,8,p.Col,4)
		
		p.setSkyscraper(8,1,p.Row,3)
		p.setMaxAscending(8,9,p.Row,4)
		
		p.setSkyscraper(6,1,p.Row,6)
		p.setMaxAscending(6,9,p.Row,3)
		
		self.assertEqual(p.findSolution(test=True),'465321789123789654789654321847593216596172438231468975972845163618937542354216897','Failed Elevator Up')
		
if __name__ == '__main__':
    unittest.main()