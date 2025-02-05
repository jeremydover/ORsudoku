import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: In Order
	# Author: Mesmer
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0003FY
	# Constraints tested: setInOrder, setGiven
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setInOrder(1,1,p.Col,[3,4,2])
		p.setInOrder(1,2,p.Col,[1,6,4])
		p.setInOrder(1,3,p.Col,[4,2,3])
		p.setInOrder(1,4,p.Col,[4,3,2])
		p.setInOrder(1,5,p.Col,[1,4,3])
		p.setInOrder(1,6,p.Col,[4,2,3])
		p.setInOrder(1,7,p.Col,[4,3,2])
		p.setInOrder(1,8,p.Col,[2,8,5])
		p.setInOrder(1,9,p.Col,[5,4,3])
		
		p.setInOrder(1,1,p.Row,[4,2,3])
		p.setInOrder(2,1,p.Row,[2,7,3])
		p.setInOrder(3,1,p.Row,[1,3,7])
		p.setInOrder(4,1,p.Row,[6,2,5])
		p.setInOrder(5,1,p.Row,[2,1,6])
		p.setInOrder(6,1,p.Row,[8,1,5])
		p.setInOrder(7,1,p.Row,[1,6,2])
		p.setInOrder(8,1,p.Row,[7,4,2])
		p.setInOrder(9,1,p.Row,[3,2,4])
		
		p.setGiven(387)
			
		self.assertEqual(p.countSolutions(test=True),'1:896427531527319468134568972319674825475982316268153794951746283742831659683295147','Failed In Order')
		
if __name__ == '__main__':
    unittest.main()