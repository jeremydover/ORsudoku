import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: X-Sums and Sandwiches
	# Author: RockyRoer
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000OQU
	# Constraints tested: setRussianDollSum,setOdd,setEven
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		var = p.setXSum(1,1,p.Col,'var')
		p.setSandwichSum(1,1,p.Col,'var')
		p.model.Add(var >= 10)
		
		var = p.setXSum(1,3,p.Col,'var')
		p.setSandwichSum(1,3,p.Col,'var')
		p.model.Add(var >= 10)
		
		var = p.setXSum(1,9,p.Row,'var')
		p.setSandwichSum(1,9,p.Row,'var')
		p.model.Add(var < 10)
		p.model.Add(var >= 0)
		
		var = p.setXSum(5,9,p.Row,'var')
		p.setSandwichSum(5,9,p.Row,'var')
		p.model.Add(var >= 10)
		
		var = p.setXSum(8,9,p.Row,'var')
		p.setSandwichSum(8,9,p.Row,'var')
		p.model.Add(var < 10)
		p.model.Add(var >= 0)
		
		var = p.setXSum(9,6,p.Col,'var')
		p.setSandwichSum(9,6,p.Col,'var')
		p.model.Add(var >= 10)
		
		var = p.setXSum(9,3,p.Col,'var')
		p.setSandwichSum(9,3,p.Col,'var')
		p.model.Add(var >= 10)
		
		var = p.setXSum(9,1,p.Col,'var')
		p.setSandwichSum(9,1,p.Col,'var')
		p.model.Add(var >= 10)
		
		var = p.setXSum(9,1,p.Row,'var')
		p.setSandwichSum(9,1,p.Row,'var')
		p.model.Add(var >= 10)
		
		var = p.setXSum(3,1,p.Row,'var')
		p.setSandwichSum(3,1,p.Row,'var')
		p.model.Add(var >= 10)
		
		var = p.setXSum(1,1,p.Row,'var')
		p.setSandwichSum(1,1,p.Row,'var')
		p.model.Add(var < 10)
		p.model.Add(var >= 0)
		
		self.assertEqual(p.countSolutions(test=True),'1:276894513891375264543126798762941385938257146415683927627439851159768432384512679','Failed X-Sums and Sandwiches')
		
if __name__ == '__main__':
    unittest.main()