import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Zipper Lines
	# Author: clover!
	# https://sudokupad.app/clover/zipper-lines-gas
	# Constraints tested: setZipperLine, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([115,159,194,223,287,336,371,519,598,733,777,828,881,914,958,999])
		p.setZipperLine([12,13,14,15,16,17,18])
		p.setZipperLine([21,31,41,51,61,71,81])
		p.setZipperLine([29,39,49,59,69,79,89])
		p.setZipperLine([92,93,94,95,96,97,98])
		p.setZipperLine([35,24,23,32,42,52,63])
		p.setZipperLine([47,58,68,78,87,86,75])
			
		self.assertEqual(p.countSolutions(test=True),'1:571693824234518976896472153358247691947156238612839547163924785789365412425781369','Failed Zipper Lines')
		
if __name__ == '__main__':
    unittest.main()