import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Boulevard of Broken Dreams
	# Author: Xeonetix
	# Link: https://tinyurl.com/broken-dreams-sudoku
	# Constraints tested: setCage, setVault, setIndexColumn
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setIndexColumn(1,True,[1,5,7,9])
		p.setIndexColumn(5,True,[1,3,5,7,9])
		p.setIndexColumn(9,True,[1,5,7,9])
		p.setCage([22,23,24,32],10)
		p.setVault([22,23,24,32])
		p.setCage([26,27,28,38],14)
		p.setVault([26,27,28,38])
		p.setCage([34,42,43,44],30)
		p.setVault([34,42,43,44])
		p.setCage([36,46,47,48],23)
		p.setVault([36,46,47,48])
		p.setCage([62],5)
		p.setVault([62])
		p.setCage([63,64],9)
		p.setVault([63,64])
		p.setCage([72,82,83],11)
		p.setVault([72,82,83])
		p.setCage([74,84],6)
		p.setVault([74,84])
		p.setCage([66,67,68,76],14)
		p.setVault([66,67,68,76])
		p.setCage([78,86,87,88],23)
		p.setVault([78,86,87,88])
		
		self.assertEqual(p.countSolutions(test=True),'1:196547382834192657725638914387926541642351798951874236219465873473289165568713429','Failed Boulevard of Broken Dreams')
		
if __name__ == '__main__':
    unittest.main()