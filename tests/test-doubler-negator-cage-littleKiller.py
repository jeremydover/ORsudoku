import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Double Negative
	# Author: jeremydover
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000GLW
	# Constraints tested: affineTransformSudoku, setCage, setLittleKiller
	
	def test_puzzle(self):
		p = ORsudoku.affineTransformSudoku(3,-2,0)
		p.setLittleKiller(1,1,2,2,0)
		p.setLittleKiller(1,2,2,3,0)
		p.setLittleKiller(2,1,3,2,0)
		p.setLittleKiller(1,9,2,8,0)
		p.setLittleKiller(1,8,2,9,0)
		p.setLittleKiller(8,1,9,2,0)
		p.setLittleKiller(1,6,2,5,0)
		p.setLittleKiller(4,9,5,8,0)
		p.setCage([81,82,83],0)
		p.setCage([19,28,29],0)
		p.setCage([75,76,85,94,95,96],0)
		p.setCage([11,12,21,22,23],0)
		p.setCage([89,98,99],0)
		
		self.assertEqual(p.countSolutions(test=True),'1:279351864516849723843672195391284576624795381758163249962518437435927618187436952010000000000000001000100000001000000000010000000000100000001000100000000000000010','Failed Double Negative')
		
if __name__ == '__main__':
    unittest.main()
	
	
