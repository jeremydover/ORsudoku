import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Knights who say Shhh
	# Author: jeremydover
	# Link: https://tinyurl.com/ycy23e7d
	# Constraints tested: setKnightMare, setGermanWhispersLine, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setKnightMare()
		p.setGermanWhispersLine([11,21,31,22,23,33])
		p.setGermanWhispersLine([19,29,39,28,27,37])
		p.setGermanWhispersLine([91,81,71,82,83,73])
		p.setGermanWhispersLine([44,45,46,55])
		p.setGivenArray([483,754,772])
		
		self.assertEqual(p.findSolution(test=True),'761829453239456178854137962596281734382764591417395826973648215128573649645912387','Failed Knights who say Shhh')
		
if __name__ == '__main__':
    unittest.main()