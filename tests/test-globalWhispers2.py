import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Close Neighbors
	# Author: Dennis Chen
	# Link: https://sudokupad.app/LFJg87q9gt
	# Constraints tested: setGivenArray, setGlobalWhispers
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([182,195,267,274,334,341,417,426,478,485,556,565,743,754,827,833,881,899,961,975])
		p.setGlobalWhispers(1,p.LE)
		self.assertEqual(p.countSolutions(test=True),'1:897634125321587496654192387769213854148965732235478961512349678473856219986721543','Failed Close Neighbors')
		
if __name__ == '__main__':
    unittest.main()