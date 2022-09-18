import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Van de Graaff Generator
	# Author: jeremydover and Raumplaner
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000A31
	# Constraints tested: setGivenArray, setEntropicLine, setBetweenLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([113,198,531,555,759,992])
		p.setEntropicLine([13,24,14,25,16,26,17,27,18,29,38,39,48,49,58,69,68,79,78,77,87,97,86,96,85,94,84,93,83,92,81,72,71,62,61,52,41,42,31,32,33,23,13])
		p.setBetweenLine([22,23,24,25,26,27,28])
		p.setBetweenLine([28,38,48,58,68,78,88])
		p.setBetweenLine([88,87,86,85,84,83,82])
		p.setBetweenLine([82,72,62,52,42,32,22])
		p.setBetweenLine([41,51,61])
		p.setBetweenLine([34,35,36,37,47,57,67])
		p.setBetweenLine([67,66,65,64])
		p.setBetweenLine([64,54,44,34])
		p.setBetweenLine([94,95,96])
		p.setBetweenLine([79,89,98])
		
		self.assertEqual(p.findSolution(test=True),'347165928592483617186927543953714286621859734478632159265398471814276395739541862','Failed Van de Graaff Generator')
		
if __name__ == '__main__':
    unittest.main()