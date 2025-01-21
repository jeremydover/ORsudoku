import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Fast Thermo
	# Author: clover!
	# https://sudokupad.app/03qfw765i7
	# Constraints tested: setFastThermo, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([125,176,213,397,715,895,933,987])
		p.setFastThermo([11,21,31,41])
		p.setFastThermo([12,13,14])
		p.setFastThermo([18,17,16])
		p.setFastThermo([19,29,39,49])
		p.setFastThermo([22,32,42,52])
		p.setFastThermo([26,15,24,33])
		p.setFastThermo([58,68,78,88])
		p.setFastThermo([61,71,81,91])
		p.setFastThermo([69,79,89,99])
		p.setFastThermo([77,86,95,84])
		p.setFastThermo([94,93,92])
		p.setFastThermo([96,97,98])
			
		self.assertEqual(p.countSolutions(test=True),'1:157948632329671584648235917871426359495317826236589741582794163714863295963152478','Failed Fast Thermo')
		
if __name__ == '__main__':
    unittest.main()