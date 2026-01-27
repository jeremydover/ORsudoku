import unittest
from ORsudoku import sudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Easy Peasy Sudoku Advent (11) - Killer Skyscrapers
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000QHV
	# Constraints tested: setSkyscraper (variable exterior clues), setCage
	
	def test_puzzle(self):
		p = sudoku(3)
		p.setSkyscraper(1,3,p.Col,'')
		p.setSkyscraper(1,5,p.Col,'')
		p.setSkyscraper(1,9,p.Col,'')
		p.setSkyscraper(1,9,p.Row,'')
		p.setSkyscraper(5,9,p.Row,'')
		p.setSkyscraper(7,9,p.Row,'')
		p.setSkyscraper(9,7,p.Col,'')
		p.setSkyscraper(9,6,p.Col,'')
		p.setSkyscraper(9,4,p.Col,'')
		p.setSkyscraper(9,3,p.Col,'')
		p.setSkyscraper(9,1,p.Row,'')
		p.setSkyscraper(8,1,p.Row,'')
		p.setSkyscraper(7,1,p.Row,'')
		p.setSkyscraper(6,1,p.Row,'')
		p.setSkyscraper(5,1,p.Row,'')
		p.setSkyscraper(4,1,p.Row,'')
		p.setSkyscraper(3,1,p.Row,'')
		p.setSkyscraper(2,1,p.Row,'')
		p.setCage([(0,3),(1,3),(2,3)],9)
		p.setCage([(0,5),(1,5)],6)
		p.setCage([(0,9),(1,9),(1,10)],11)
		p.setCage([(5,8),(5,9),(5,10)],13)
		p.setCage([(7,9),(7,10)],3)
		p.setCage([(10,6),(10,7)],17)
		p.setCage([(10,3),(10,4)],3)
		p.setCage([(9,0),(9,1)],10)
		p.setCage([(7,0),(8,0)],8)
		p.setCage([(5,0),(6,0)],4)
		p.setCage([(4,0),(4,1)],10)
		p.setCage([(2,0),(3,0)],10)
			
		self.assertEqual(p.countSolutions(test=True),'1:874529136123468957569137824345216789912875643687394512256783491491652378738941265','Failed Easy Peasy Sudoku Advent (11) - Killer Skyscrapers')
		
if __name__ == '__main__':
    unittest.main()