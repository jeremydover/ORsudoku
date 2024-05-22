import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Flattened Helix
	# Author: Sotek
	# Link: currently private
	# Constraints tested: setMinMaxArray, setCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setMinMaxArray([140,351,360,411,471,530,570,631,690,751,760,960])
		p.setCage([13,14,15,24],25)
		p.setCage([31,41,51,42],13)
		p.setCage([34,35,36,45],27)
		p.setCage([43,53,63,54],13)
		p.setCage([47,57,67,56],17)
		p.setCage([59,69,79,68],19)
		p.setCage([74,75,76,65],23)
		p.setCage([95,96,97,86],17)
		
		self.assertEqual(p.countSolutions(test=True),'1:879452136253716849146893572532974618481365297967128453315687924624539781798241365','Failed Flattened Helix')
		
if __name__ == '__main__':
    unittest.main()