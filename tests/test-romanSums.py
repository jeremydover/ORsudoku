import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Nine-Eleven
	# Author: Raumplaner
	# Constraints tested: setRomanSumArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRomanSumArray([12011,16111,2209,2409,27011,3309,34011,3509,36011,42011,4409,45011,4609,47011,63011,6409,65011,6709,72011,7419,77011,92011,95011,97011])
			
		self.assertEqual(p.countSolutions(test=True),'1:865372914472819563913654728247183659581926347396547182638291475154738296729465831','Failed Nine-Eleven')
		
if __name__ == '__main__':
    unittest.main()