import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Arsenic on Rye
	# Author: BremSter and randall
	# Link: https://bremster.tiny.us/arseniconrye
	# Constraints tested: setCage,setSandwichSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCage([14,24,23],13)
		p.setCage([28,38,37],22)
		p.setCage([31,32,33],8)
		p.setCage([45,55,65],15)
		p.setCage([51,52],11)
		p.setCage([58,59],11)
		p.setCage([63,73,83],7)
		p.setCage([77,78,87],8)
		p.setCage([84,85,86],17)
		p.setSandwichSum(1,1,p.Col,13)
		p.setSandwichSum(1,3,p.Col,14)
		p.setSandwichSum(1,5,p.Col,15)
		p.setSandwichSum(1,8,p.Col,26)
		p.setSandwichSum(3,1,p.Row,12)
		p.setSandwichSum(8,1,p.Row,25)
		p.setSandwichSum(9,1,p.Row,10)
		
		self.assertEqual(p.findSolution(test=True),'496817325783265491215439768379546182658321974142798653564983217821674539937152846','Failed Arsenic on Rye')
		
if __name__ == '__main__':
    unittest.main()