import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Match-Making
	# Author: Emphyrio
	# Link: https://sudokupad.app/k1fg5tjqrf
	# Constraints tested: setCage, setShiftLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCage([17,18],6)
		p.setCage([19,29],6)
		p.setCage([24,25],11)
		p.setCage([43,53],8)
		p.setCage([57,67],9)
		p.setCage([75,76],13)
		p.setCage([81,82],5)
		p.setCage([98,99],5)
		p.setShiftLine([16,15,14,13,12,21,31,41,51,61])
		p.setShiftLine([28,38,39,49,48,58])
		p.setShiftLine([59,69,68,78,79,89])
		p.setShiftLine([92,93,83,84,94,95])
		p.setShiftLine([85,86,96,97,87,88])
			
		self.assertEqual(p.countSolutions(test=True),'1:375968421681472935429315786836524197512697348794831652257149863143286579968753214','Failed Match-Making')
		
if __name__ == '__main__':
    unittest.main()