import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sino De Times
	# Author: jeremydover
	# Link: https://tinyurl.com/3k7y5jbf
	# Constraints tested: setGermanWhispersLine, setChineseWhispersLine
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([358,755])
		p.setChineseWhispersLine([12,23])
		p.setChineseWhispersLine([21,32])
		p.setChineseWhispersLine([37,28,39])
		p.setChineseWhispersLine([42,43,53,62,61,51,42])
		p.setChineseWhispersLine([46,56])
		p.setChineseWhispersLine([71,72,83,92,91,81,71])
		p.setChineseWhispersLine([87,78,88,98,89])
		p.setGermanWhispersLine([21,31,32,22,12,13,23])
		p.setGermanWhispersLine([18,29,39,38,37,27,18])
		p.setGermanWhispersLine([44,54,64])
		p.setGermanWhispersLine([49,59])
		p.setGermanWhispersLine([57,58])
		p.setGermanWhispersLine([73,82,93])
		p.setGermanWhispersLine([77,78,89,99,98,87,77])
		
		self.assertEqual(p.countSolutions(test=True),'1:483927516629531847175684392957216483316845729248379165861752934794163258532498671','Failed Sine De Times')
		
if __name__ == '__main__':
    unittest.main()