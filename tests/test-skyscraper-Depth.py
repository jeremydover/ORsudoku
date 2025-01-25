import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (358) - Sandstorm Skyscrapers Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000905
	# Constraints tested: setSkyscraper, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([332,443,662,778])
		p.setSkyscraper(1,1,p.Col,2,depth=4)
		p.setSkyscraper(1,2,p.Col,1,depth=4)
		p.setSkyscraper(1,3,p.Col,3,depth=4)
		p.setSkyscraper(1,4,p.Col,1,depth=4)
		p.setSkyscraper(1,5,p.Col,2,depth=4)
		p.setSkyscraper(1,6,p.Col,4,depth=4)
		p.setSkyscraper(1,7,p.Col,3,depth=4)
		p.setSkyscraper(1,8,p.Col,3,depth=4)
		p.setSkyscraper(1,9,p.Col,3,depth=4)
		
		p.setSkyscraper(1,9,p.Row,4,depth=4)
		p.setSkyscraper(2,9,p.Row,3,depth=4)
		p.setSkyscraper(3,9,p.Row,3,depth=4)
		p.setSkyscraper(4,9,p.Row,4,depth=4)
		p.setSkyscraper(5,9,p.Row,1,depth=4)
		p.setSkyscraper(6,9,p.Row,2,depth=4)
		p.setSkyscraper(7,9,p.Row,1,depth=4)
		p.setSkyscraper(8,9,p.Row,2,depth=4)
		p.setSkyscraper(9,9,p.Row,3,depth=4)
		
		p.setSkyscraper(9,1,p.Col,2,depth=4)
		p.setSkyscraper(9,2,p.Col,1,depth=4)
		p.setSkyscraper(9,3,p.Col,3,depth=4)
		p.setSkyscraper(9,4,p.Col,2,depth=4)
		p.setSkyscraper(9,5,p.Col,4,depth=4)
		p.setSkyscraper(9,6,p.Col,1,depth=4)
		p.setSkyscraper(9,7,p.Col,2,depth=4)
		p.setSkyscraper(9,8,p.Col,3,depth=4)
		p.setSkyscraper(9,9,p.Col,2,depth=4)
		
		p.setSkyscraper(1,1,p.Row,2,depth=4)
		p.setSkyscraper(2,1,p.Row,3,depth=4)
		p.setSkyscraper(3,1,p.Row,1,depth=4)
		p.setSkyscraper(4,1,p.Row,2,depth=4)
		p.setSkyscraper(5,1,p.Row,2,depth=4)
		p.setSkyscraper(6,1,p.Row,2,depth=4)
		p.setSkyscraper(7,1,p.Row,2,depth=4)
		p.setSkyscraper(8,1,p.Row,1,depth=4)
		p.setSkyscraper(9,1,p.Row,2,depth=4)
		
		self.assertEqual(p.countSolutions(test=True),'1:697584321138296754542137986759318642826945137413672598275463819964851273381729465','Failed Sudoku Variants Series (358) - Sandstorm Skyscrapers Sudoku')
		
if __name__ == '__main__':
    unittest.main()