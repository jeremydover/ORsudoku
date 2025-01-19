import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Positive Odds
	# Author: Lisztes
	# https://f-puzzles.com/?id=2fjn8dam
	# Constraints tested: setCage, digitSet
	# Note: in original puzzle, for cages odds count as positive, evens as negative. But it comes to the same thing as replacing the even digits with their negatives.
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3,digitSet=[1,-2,3,-4,5,-6,7,-8,9])
		p.setXSudokuOff()
		p.setCage([11,12],-7)
		p.setCage([14,15,16],-1)
		p.setCage([19,29],1)
		p.setCage([22,23,32,33],8)
		p.setCage([27,28],3)
		p.setCage([34,44,43],6)
		p.setCage([37,38],-3)
		p.setCage([41,51,61],1)
		p.setCage([46,47],-3)
		p.setCage([49,59,69],1)
		p.setCage([56,57,58],-2)
		p.setCage([63,64],3)
		p.setCage([65,75,85],2)
		p.setCage([66,67,76],6)
		p.setCage([72,82],3)
		p.setCage([73,83],-1)
		p.setCage([77,78,87,88],6)
		p.setCage([81,91],-3)
		p.setCage([94,95,96],-1)
		p.setCage([98,99],-7)
		
		self.assertEqual(p.countSolutions(test=True),'1:1-8-6-45-23797-493-615-2-83-2597-8-41-6-21-85-43-697957-2-8-613-4-63-4719-85-2-491-8-257-63-8-6-21379-45573-69-4-2-81','Failed Positive Odds')
		
if __name__ == '__main__':
    unittest.main()