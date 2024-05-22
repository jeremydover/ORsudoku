import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Entropic Whispers
	# Author: gdc
	# Link: https://sudokupad.app/o8jrs7sb48
	# Constraints tested: setXVArray, setEntropicWhispersLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setEntropicWhispersLine([13,24,35,46,55,45,44,53,64,75,76,67,58,59])
		p.setEntropicWhispersLine([17,27,37])
		p.setEntropicWhispersLine([19,29,39])
		p.setEntropicWhispersLine([68,78,77])
		p.setEntropicWhispersLine([22,32,31,41,51,52,62,72,82,83,84,85,86])
		p.setXVArray([(4,4,p.Horz,p.X),(8,5,p.Vert,p.V)])
		
		self.assertEqual(p.countSolutions(test=True),'1:532641789846579132197283465678192543924357816351864927283715694415926378769438251','Failed Entropic Whispers')
		
if __name__ == '__main__':
    unittest.main()