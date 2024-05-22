import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Lathe
	# Author: BremSter
	# Link: https://tinyurl.com/mprs4wys
	# Constraints tested: setRegion, setCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3,irregular=True)
		p.setRegion([11,12,21,22,23,31,33,43,44])
		p.setRegion([13,14,15,16,17,24,25,34,35])
		p.setRegion([18,19,26,27,28,29,36,37,47])
		p.setRegion([32,41,42,51,52,53,61,62,72])
		p.setRegion([45,46,54,55,56,57,58,65,66])
		p.setRegion([38,39,48,49,59,68,69,78,79])
		p.setRegion([63,64,71,73,81,82,83,91,92])
		p.setRegion([74,75,84,85,93,94,95,96,97])
		p.setRegion([67,76,77,86,87,88,89,98,99])
		p.setCage([14,24],16)
		p.setCage([15,16,26],12)
		p.setCage([21,31],15)
		p.setCage([28,29],13)
		p.setCage([34,35],8)
		p.setCage([36,37,47,57,67,76,77],28)
		p.setCage([41,51,61,52],21)
		p.setCage([53,54,55],15)
		p.setCage([49,59,69,58],19)
		p.setCage([63,64],10)
		p.setCage([74,75],9)
		p.setCage([81,91],15)
		p.setCage([84,94],11)
		p.setCage([86,96,95],13)
		p.setCage([98,99],15)
		
		self.assertEqual(p.countSolutions(test=True),'1:152946873643712985927354618478239156391865247586471392269187534735698421814523769','Failed Irregular Killer')
		
if __name__ == '__main__':
    unittest.main()