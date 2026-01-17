import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Easy Peasy Sudoku Advent (13) - Zipper Lines ++
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000QJD
	# Constraints tested: setZipperLines
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setZipperLine([24,34,33,42,43,52,63],augment=1)
		p.setZipperLine([26,36,35,46,47,57,67,66,77,78,79,69,59,49,48,37,27],augment=1)
		p.setZipperLine([65,76,87],augment=1)
		p.setZipperLine([75,74,84,73,83,72,71,81,91,82,92,93,94,85,95],augment=1)
		p.setZipperLine([86,96,97],augment=1)
		p.setZipperLine([88,99,89],augment=1)
		
		self.assertEqual(p.countSolutions(test=True),'1:927346581861527934534189672185234769492678315376915428253791846749862153618453297','Failed Easy Peasy Sudoku Advent (13) - Zipper Lines ++')
		
if __name__ == '__main__':
    unittest.main()