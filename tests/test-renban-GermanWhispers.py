import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Candy Cane Sudoku
	# Author: jeremydover
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008TV
	# Constraints tested: setGivenArray, setRenban, setRenbanLine, setGermanWhispersLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([151,177,726,758,884])
		p.setRenbanLine([11,12,13,23])
		p.setRenbanLine([25,35,45])
		p.setRenbanLine([31,41,42])
		p.setRenbanLine([47,57,67])
		p.setRenbanLine([64,65,76,86,95,94,93,92,91])
		p.setRenbanLine([69,79,89])
		p.setGermanWhispersLine([14,24,34])
		p.setGermanWhispersLine([21,22,32])
		p.setGermanWhispersLine([27,18,29,39,49,59])
		p.setGermanWhispersLine([36,46,56])
		p.setGermanWhispersLine([58,68,78])
		p.setGermanWhispersLine([62,71,82,83,84,85])
		p.setGermanWhispersLine([88,87,97,98,99])
		
		self.assertEqual(p.findSolution(test=True),'356918724714235869892746351679521438481367592235894617963482175528173946147659283','Failed Candy Cane Sudoku')
		
if __name__ == '__main__':
    unittest.main()