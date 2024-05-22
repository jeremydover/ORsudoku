import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: E is for Entropic
	# Author: jeremydover
	# Link: https://sudokupad.app/0z13a2vu6c
	# Constraints tested: setKnightMare, setEntropicLine, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setKnightMare()
		p.setEntropicLine([13,12,22,11,21,31,32,33])
		p.setEntropicLine([17,18,28,19,29,39,38,37])
		p.setEntropicLine([14,15,16,26,25,24,34])
		p.setEntropicLine([74,84,85,94,95,96,86,76])
		p.setEntropicLine([64,54,65,56,46,55,45])
		p.setEntropicLine([49,48,47,57,58,59])
		p.setGivenArray([737,673,922])
		
		self.assertEqual(p.countSolutions(test=True),'1:263519748589734126714682593346827951158943267972165384837296415695471832421358679','Failed E is for Entropic')
		
if __name__ == '__main__':
    unittest.main()