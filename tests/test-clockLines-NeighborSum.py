import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Lonely Satellite
	# Author: AnalyticalNinja
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000BPW
	# Constraints tested: setClockLine, setNeighborSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setClockLine([12,13,24,34,43,42,31,21,12])
		p.setClockLine([35,36,37,28])
		p.setClockLine([37,48,49])
		p.setClockLine([57,47,46,45,44,54,64,55,66,65])
		p.setClockLine([64,73,83,82,72])
		p.setClockLine([68,69,79,89,98,97,96,86,77,68])
		p.setNeighborSum(56)
		
		self.assertEqual(p.countSolutions(test=True),'1:729853614458216937613497582246531879935728146871964253382645791564179328197382465','Failed Lonely Satellite')
		
if __name__ == '__main__':
    unittest.main()