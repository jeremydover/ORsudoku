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
		
		self.assertEqual(p.countSolutions(test=True),'1:2*7*935186451684972*3*843*6*7219539*1*2845766247*9*5381758163*2*4996251*8*437*4*359276181874369*5*2','Failed Double Negative')
		
if __name__ == '__main__':
    unittest.main()