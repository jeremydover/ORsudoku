import unittest
from cellTransformSudoku import doublerSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Horses are better in pairs
	# Author: chameleon
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000HO0
	# Constraints tested: setgivenArray, set AntiKnight, doublerSudoku
	
	def test_puzzle(self):
		p = doublerSudoku(3)
		p.setAntiKnight()
		p.setGivenArray([153,181,214,221,288,337,376,445,466,647,669,735,779,824,882,898,922])
		
		self.assertEqual(p.countSolutions(test=True),'1:596832417413697285287451693874526139169384752352719864635278941741963528928145376000001000001000000000000010010000000000010000000000001100000000000000100000100000','Failed Horses are better in pairs')
		
if __name__ == '__main__':
    unittest.main()
	
