import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: GSP LOL
	# Author: Virtual and Grkles
	# https://sudokupad.app/mgkpb5mclu
	# Constraints tested: setWeakPalindromeLine, setGiven, setXVArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGiven(866)
		p.setXVArray([1301,1801,2100,3201,5311,5401,6211,6410,7300,8701,9700])
		p.setWeakPalindromeLine([13,12,11,21,31,32,33,23,22])
		p.setWeakPalindromeLine([26,25,24,14,15,16,17,18])
		p.setWeakPalindromeLine([52,62,63,53])
		p.setWeakPalindromeLine([46,45,44,54,55,56,66,65,64])
		p.setWeakPalindromeLine([97,87,77,78,79,89,88])
			
		self.assertEqual(p.countSolutions(test=True),'1:693754182417238695528619743746982531259371468831465279974123856382546917165897324','Failed GSP LOL')
		
if __name__ == '__main__':
    unittest.main()