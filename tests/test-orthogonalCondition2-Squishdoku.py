import unittest
from squishdoku import squishdoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Neatly Squished
	# Author: marty_sears
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000G2X
	# Constraints tested: setOrthogonalCondition, squishdoku
	
	def test_puzzle(self):
		p = squishdoku(3)
		p.setOrthogonalCondition([['ParityAfter']],[('Parity',p.EQ,0)],2)
		p.setKropkiArray([(1,1,p.Vert,p.White),(1,6,p.Vert,p.White),(1,7,p.Vert,p.White),(3,3,p.Vert,p.Black),(3,5,p.Vert,p.Black),(6,1,p.Vert,p.White)])
			
		self.assertEqual(p.countSolutions(test=True),'1:9672583814967252381494765238189476563218947456321','Failed Neatly Squished')
		
if __name__ == '__main__':
    unittest.main()