import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Pointing Differents
	# Author: clover!
	# https://sudokupad.app/g19kcxmim3
	# Constraints tested: setPointingDifferents, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setPointingDifferents(1,1,2,2,3)
		p.setPointingDifferents(1,2,2,3,2)
		p.setPointingDifferents(1,5,2,6,2)
		p.setPointingDifferents(1,6,2,7,2)
		p.setPointingDifferents(4,1,3,2,2)
		p.setPointingDifferents(6,9,7,8,2)
		p.setPointingDifferents(9,4,8,3,2)
		p.setPointingDifferents(9,5,8,4,2)
		p.setPointingDifferents(9,8,8,7,2)
		p.setGivenArray([163,227,265,272,322,398,411,466,645,693,719,784,834,846,888,941])
	
		self.assertEqual(p.countSolutions(test=True),'1:845263917371985264629417538193746852582391476467528193916832745254679381738154629','Failed Pointing Differents')
		
if __name__ == '__main__':
    unittest.main()