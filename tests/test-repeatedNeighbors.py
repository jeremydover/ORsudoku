import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (123) - Repeated Neighbours Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002EJ
	# Constraints tested: setRepeatedNeighborsArray, setRepeatedNeighboursNegative, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRepeatedNeighborsArray([24,26,33,37,42,48,62,68,73,77,84,86])
		p.setRepeatedNeighboursNegative()
		p.setGivenArray([134,155,176,223,287,312,398,511,558,599,717,791,822,884,931,959,978])
			
		self.assertEqual(p.countSolutions(test=True),'1:814357692639218475275964318387429156142586739596173284763845921928631547451792863','Failed Sudoku Variants Series (123) - Repeated Neighbours Sudoku')
		
if __name__ == '__main__':
    unittest.main()