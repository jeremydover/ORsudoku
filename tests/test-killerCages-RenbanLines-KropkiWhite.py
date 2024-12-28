import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Radiant Heat
	# Author: jeremydover
	# Link: https://sudokupad.app/dmyzcjpj4g
	# Constraints tested: setCage, setRenbanLine, setKropkiWhiteArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRenbanLine([33,43,53,63,73,74,75,76])
		p.setRenbanLine([34,35,36,37,47,57,67,77])
		p.setRenbanLine([49,59,69])
		p.setRenbanLine([42,51,61])
		p.setRenbanLine([46,56,66])
		p.setRenbanLine([45,55,65])
		p.setRenbanLine([44,54,64])
		p.setCage([11,12,21,22],13)
		p.setCage([88,89,98,99],14)
		p.setCage([18,19,28,29],27)
		p.setCage([84,85,86,94,95,96],24)
		p.setKropkiWhiteArray([310,171,271,120,220,291,140,351,630,570,820,851])
		
		self.assertEqual(p.countSolutions(test=True),'1:145238679267149583893765412938472156572691348416583297324957861689314725751826934','Failed Radiant Heat')
		
if __name__ == '__main__':
    unittest.main()