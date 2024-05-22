import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Space Oddity
	# Author: jeremydover
	# Link: https://link.sudokupad.app/polar-spaceoddity
	# Constraints tested: setGiven, setRenbanLine, setParityLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGiven(848)
		lines = [[11,21,12,23,13],[14,24,35,26,16],[27,17,28,19,29],[33,43,53,62,72],[42,52,51],[45,54,55,56,65],[47,57,58,48,59],[63,73,82,91,81],[85,74,83,93,94],[67,77,87,86,95],[79,89,99,88]]
		for x in lines:
			p.setRenbanLine(x)
			p.setParityLine(x)
		
		self.assertEqual(p.countSolutions(test=True),'1:513927486294618735687354129438169257129785364765243918356492871971836542842571693','Failed Space Oddity')
		
if __name__ == '__main__':
    unittest.main()