import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Entropic Skyscrapers
	# Author: Raumplaner
	# Link: https://tinyurl.com/LOEntropySP44
	# Constraints tested: setEntropicLine, setSkyscraper
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setEntropicLine([11,21,31])
		p.setEntropicLine([13,23,33,43,42,41,51])
		p.setEntropicLine([16,26,36,46])
		p.setEntropicLine([28,18,19,29])
		p.setEntropicLine([39,49,48,47])
		p.setEntropicLine([44,54,55])
		p.setEntropicLine([71,61,62,63,64,74,84,94])
		p.setEntropicLine([81,91,92,82])
		p.setEntropicLine([96,86,76,66,67,68,69,79,89,88,98,99])
		p.setSkyscraper(1,1,p.Row,4)
		p.setSkyscraper(2,1,p.Row,3)
		p.setSkyscraper(3,1,p.Row,4)
		p.setSkyscraper(4,1,p.Row,4)
		p.setSkyscraper(6,1,p.Row,4)
		p.setSkyscraper(8,1,p.Row,4)
		p.setSkyscraper(1,5,p.Col,4)
		p.setSkyscraper(1,6,p.Col,3)
		p.setSkyscraper(1,7,p.Col,4)
		p.setSkyscraper(2,9,p.Row,2)
		p.setSkyscraper(3,9,p.Row,2)
		p.setSkyscraper(4,9,p.Row,3)
		p.setSkyscraper(7,9,p.Row,3)
		p.setSkyscraper(8,9,p.Row,4)
		p.setSkyscraper(9,9,p.Col,4)
		p.setSkyscraper(9,7,p.Col,3)
		p.setSkyscraper(9,5,p.Col,3)
		p.setSkyscraper(9,4,p.Col,3)
		p.setSkyscraper(9,1,p.Col,2)
		
		self.assertEqual(p.countSolutions(test=True),'1:546827139789513246123964578374158962691472385258396714935681427462739851817245693','Failed Entropic Skyscrapers')
		
if __name__ == '__main__':
    unittest.main()