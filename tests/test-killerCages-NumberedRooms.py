import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Roaches Check In...
	# Author: Twototenth
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000C5S
	# Constraints tested: setCage,setNumberedRoom
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCage([12,22,32],13)
		p.setCage([24,25,26],22)
		p.setCage([18,28,38],22)
		p.setCage([54,55,56],13)
		p.setCage([49,59,69],19)
		p.setCage([71,81,91],15)
		p.setCage([74,84,94],14)
		p.setCage([87,88,89],13)
		p.setNumberedRoom(1,1,p.Row,8)
		p.setNumberedRoom(2,1,p.Row,8)
		p.setNumberedRoom(3,1,p.Row,8)
		p.setNumberedRoom(5,1,p.Row,4)
		p.setNumberedRoom(7,1,p.Row,6)
		p.setNumberedRoom(6,9,p.Row,2)
		p.setNumberedRoom(1,2,p.Col,7)
		p.setNumberedRoom(1,6,p.Col,9)
		p.setNumberedRoom(9,2,p.Col,3)
		p.setNumberedRoom(9,4,p.Col,2)
		p.setNumberedRoom(9,8,p.Col,6)
			
		self.assertEqual(p.countSolutions(test=True),'1:358167492427895163961234578894571326572643819136982754785429631619358247243716985','Failed Roaches Check In...')
		
if __name__ == '__main__':
    unittest.main()