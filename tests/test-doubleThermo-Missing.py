import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: 183654729
	# Author: jeremydover
	# Link: https://sudokupad.app/a1sj6jqlkf
	# Constraints tested: setDoubleThermo,setKropkiBlackArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)	
		p.setDoubleThermo([11,12,13,14,15,16,17,18,19],increaseCriteria='MissingOpposite',missing=True)
		p.setDoubleThermo([21,22,23,24,25,26,27,28,29],increaseCriteria='MissingOpposite',missing=True)
		p.setDoubleThermo([91,92,93,94,95,96,97,98,99],increaseCriteria='MissingOpposite',missing=True)
		p.setDoubleThermo([81,82,83,84,85,86,87,88,89],increaseCriteria='MissingOpposite',missing=True)
		p.setDoubleThermo([55,56,46,45,44,54,64,65,66],increaseCriteria='MissingOpposite',missing=True)
		p.setDoubleThermo([73,74,75,76,77],increaseCriteria='MissingOpposite',missing=True)
		p.setKropkiBlackArray([120,230,980,860,670,410,491,441])
		self.assertEqual(p.countSolutions(test=True),'1:924768531816354279753912864481235796562497183379681425648123957297546318135879642','Failed 183654729')
		
if __name__ == '__main__':
    unittest.main()