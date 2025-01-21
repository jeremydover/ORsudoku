import unittest
from schroedingerSudoku import schroedingerCellSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Bose-Einstein Condensate
	# Author: purpl
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008UI
	# Constraints tested: schroedingerCellSudoku, setIsNotSCellArray, setGivenArray, setBetweenLine
	
	def test_puzzle(self):
		p = schroedingerCellSudoku(3)
		p.setGivenArray([134,316,546,777,837])
		p.setIsNotSCellArray([13,31,54,77,83])
		p.setBetweenLine([15,16,26])
		p.setBetweenLine([34,23,12,22,21,32,43])
		p.setBetweenLine([36,27,18,28,29,38,47])
		p.setBetweenLine([43,42,52,63,62,73])
		p.setBetweenLine([47,48,57,58,68,79])
		p.setBetweenLine([82,81,71])
		p.setBetweenLine([71,72,73])
		p.setBetweenLine([73,84,75,85,95,96])
		p.setBetweenLine([76,86,97,88])
		p.setBetweenLine([77,78,79])
		p.setBetweenLine([43,54,64,65,66,56,47])
		
		self.assertEqual(p.countSolutions(test=True),'1:124356870785029631630178452459283016271605348063714529842930765307562184516847203900000000000400000000000900000000007000090000008000000000001000000000090090000000','Failed Bose-Einstein Condensate')
		
if __name__ == '__main__':
    unittest.main()
	
	

	
