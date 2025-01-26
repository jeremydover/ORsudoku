import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Dutch Flat Mates
	# Author: Flinty
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000FGP
	# Constraints tested: setDutchFlatMates, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setDutchFlatMates()
		p.setGivenArray([118,157,194,229,241,264,283,353,423,431,478,489,519,597,627,632,675,686,754,826,847,869,881,917,951,993])
		
		self.assertEqual(p.countSolutions(test=True),'1:853976124297184635614532789531467892986251347472893561128345976365729418749618253','Failed Dutch Flat Mates')
		
if __name__ == '__main__':
    unittest.main()