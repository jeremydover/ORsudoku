import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Duality
	# Author: Riffclown
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000AOO
	# Constraints tested: setGiven, setThermo, setRegionSumLine
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		lines = [[14,24,34,35,45,55],[17,27,37,47,57],[22,33,43],[49,59,69,79,89],[52,42,32],[58,48,38],[93,83,73,72,71,61,51],[95,96,87]]
		for x in lines:
			p.setThermo(x)
			p.setRegionSumLine(x)
		p.setGiven(536)
		
		self.assertEqual(p.findSolution(test=True),'365127489419386572287459631158963724936274815724518396643892157572631948891745263','Failed Duality')
		
if __name__ == '__main__':
    unittest.main()