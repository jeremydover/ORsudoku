import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Skyscraper Sums
	# Author: kuraban
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000AEU
	# Constraints tested: setSkyscraperSum, setGiven
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGiven(845)
		p.setSkyscraperSum(1,1,p.Col,24)
		p.setSkyscraperSum(1,3,p.Col,17)
		p.setSkyscraperSum(1,5,p.Col,39)
		p.setSkyscraperSum(1,7,p.Col,15)
		p.setSkyscraperSum(1,9,p.Col,25)
		
		p.setSkyscraperSum(5,9,p.Row,13)
		p.setSkyscraperSum(6,9,p.Row,29)
		
		p.setSkyscraperSum(9,1,p.Col,14)
		p.setSkyscraperSum(9,2,p.Col,25)
		p.setSkyscraperSum(9,5,p.Col,13)
		p.setSkyscraperSum(9,7,p.Col,28)
		p.setSkyscraperSum(9,9,p.Col,12)
		
		p.setSkyscraperSum(2,1,p.Row,23)
		p.setSkyscraperSum(5,1,p.Row,40)
		p.setSkyscraperSum(7,1,p.Row,21)
		
		self.assertEqual(p.countSolutions(test=True),'1:798342651641859327352167948874923516235671894916485732483296175167534289529718463','Failed Skyscraper Sums')
		
if __name__ == '__main__':
    unittest.main()