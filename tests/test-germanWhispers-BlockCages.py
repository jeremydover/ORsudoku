import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Strange Portal
	# Author: BremSter
	# Link: https://bremster.tiny.us/strangeportal
	# Constraints tested: setGermanWhispersLine, setBlockCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGermanWhispersLine([12,13])
		p.setGermanWhispersLine([17,18])
		p.setGermanWhispersLine([34,35,36])
		p.setGermanWhispersLine([14,23,33,43,52])
		p.setGermanWhispersLine([16,27,37,47,58])
		p.setGermanWhispersLine([32,41,51])
		p.setGermanWhispersLine([55,56,57])
		p.setGermanWhispersLine([62,73,84])
		p.setGermanWhispersLine([68,77,86])
		p.setGermanWhispersLine([81,92,93])
		p.setGermanWhispersLine([97,98,89])
		p.setBlockCage([75],4)
		p.setBlockCage([85,95],37)
		p.setBlockCage([52,62,61],[2,8])
		p.setBlockCage([58,68,69],[2,8])
		p.setBlockCage([35,45,55],12)
		p.setBlockCage([94,84,83,73,63,53,43,33,23,24,25,26,27,37,47,57,67,77,87,86,96],19)
		
		self.assertEqual(p.findSolution(test=True),'461378925978625341532491867857146239216539478394287516183964752745812693629753184','Failed Strange Portal')
		
if __name__ == '__main__':
    unittest.main()