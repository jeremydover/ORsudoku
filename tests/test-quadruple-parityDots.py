import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Circle in s Spiral
	# Author: BremSter
	# Link: https://bremster.tiny.us/circleinaspiral
	# Constraints tested: setQuadrupleArray, setParityDotArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setQuadrupleArray([1435,1546,22135,27246,347,4148,4879,5113,5826,654,72468,77579,8468,8579])
		p.setParityDotArray([1301,1601,2310,2710,3110,3211,3811,3910,4511,5301,5510,5600,6110,6211,6811,6910,7310,7710,9301,9601])
		
		self.assertEqual(p.findSolution(test=True),'624839715718546329953271468892163547435728196167954832286415973349687251571392684','Failed Circle in a Sprial')
		
if __name__ == '__main__':
    unittest.main()