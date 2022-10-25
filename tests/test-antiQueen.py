import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Quevens
	# Author: Raumplaner and Skunkworks
	# Link: https://link.sudokupad.app/polar-quevens
	# Constraints tested: setgivenArray, setAntiQueenDigit
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([117,156,163,332,348,384,393,525,551,583,715,722,766,774,945,958,999])
		p.setAntiQueenDigit(2)
		p.setAntiQueenDigit(4)
		p.setAntiQueenDigit(6)
		p.setAntiQueenDigit(8)
			
		self.assertEqual(p.findSolution(test=True),'794163582835724961612895743241637895958412637376958124529376418187249356463581279','Failed Quevens')
		
if __name__ == '__main__':
    unittest.main()