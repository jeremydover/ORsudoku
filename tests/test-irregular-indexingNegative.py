import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Eclipse
	# Author: Xeonetix
	# Link: https://tinyurl.com/sudoku-eclipse
	# Constraints tested: setRegion, setGivenArray, setIndexColumn, setIndexRow
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3,irregular=True)
		p.setRegion([12,13,14,15,16,17,18,25,35])
		p.setRegion([11,21,22,23,24,32,33,34,43])
		p.setRegion([19,26,27,28,29,36,37,38,47])
		p.setRegion([44,45,46,54,55,56,64,65,66])
		p.setRegion([31,41,42,51,52,53,61,62,71])
		p.setRegion([39,48,49,57,58,59,68,69,79])
		p.setRegion([63,72,73,74,81,82,83,84,91])
		p.setRegion([67,76,77,78,86,87,88,89,99])
		p.setRegion([75,85,92,93,94,95,96,97,98])
			
		p.setGivenArray([196,337,374,736,777,918])
		p.setIndexColumn(1,True,[4,6,7,8])
		p.setIndexColumn(5,True,[3,7])
		p.setIndexColumn(9,True,[2,3,4,7])
		p.setIndexRow(1,True,[3,5,6,8])
		p.setIndexRow(5,True,[3,4,5,6,7])
		p.setIndexRow(9,True,[2,4,5,7,9])
		
		self.assertEqual(p.countSolutions(test=True),'1:581794326394867512267153498652471839418935267739628145946382751175249683823516974','Failed Eclipse')
		
if __name__ == '__main__':
    unittest.main()