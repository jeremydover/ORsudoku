import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Elevator Down
	# Author: jeremydover
	# Link: https://tinyurl.com/3k333ja4
	# Constraints tested: negatorSudoku, setNumberedRoom
	
	def test_puzzle(self):
		p = ORsudoku.negatorSudoku(3)
		p.setNumberedRoom(1,1,p.Col,2)
		p.setNumberedRoom(1,2,p.Col,8)
		p.setNumberedRoom(1,3,p.Col,6)
		p.setNumberedRoom(1,4,p.Col,8)
		p.setNumberedRoom(1,5,p.Col,2)
		p.setNumberedRoom(1,6,p.Col,8)
		p.setNumberedRoom(1,7,p.Col,-9)
		p.setNumberedRoom(1,8,p.Col,7)
		p.setNumberedRoom(1,9,p.Col,3)
		p.setNumberedRoom(1,9,p.Row,8)
		p.setNumberedRoom(2,9,p.Row,9)
		p.setNumberedRoom(3,9,p.Row,7)
		p.setNumberedRoom(4,9,p.Row,6)
		p.setNumberedRoom(5,9,p.Row,-5)
		p.setNumberedRoom(6,9,p.Row,4)
		p.setNumberedRoom(7,9,p.Row,9)
		p.setNumberedRoom(8,9,p.Row,6)
		p.setNumberedRoom(9,9,p.Row,2)
		p.setNumberedRoom(9,1,p.Col,1)
		p.setNumberedRoom(9,2,p.Col,2)
		p.setNumberedRoom(9,3,p.Col,2)
		p.setNumberedRoom(9,5,p.Col,1)
		p.setNumberedRoom(9,7,p.Col,1)
		p.setNumberedRoom(9,9,p.Col,7)
		p.setNumberedRoom(3,1,p.Row,5)
		p.setNumberedRoom(5,1,p.Row,-5)
		p.setNumberedRoom(8,1,p.Row,7)
		p.setNumberedRoom(9,1,p.Row,4)
		
		self.assertEqual(p.findSolution(test=True),'89374562*1*5216*3*98747*4*628153996*7*124358432*5*98716158376*9*4231985*2*4672749631*8*5*6*85417293','Failed Elevator Down')
		
if __name__ == '__main__':
    unittest.main()