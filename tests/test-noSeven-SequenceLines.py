import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: No Seven - Sequences
	# Author: Raumplaner
	# https://sudokupad.app/v6xopuhuof
	# Constraints tested: setNoSeven, setSequenceLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setNoSeven()
		p.setSequenceLine([11,12,13,22,31])
		p.setSequenceLine([14,23,32,33,34])
		p.setSequenceLine([27,36,37,38])
		p.setSequenceLine([47,46,45,54,63])
		p.setSequenceLine([51,52,61])
		p.setSequenceLine([73,82,91])
		p.setSequenceLine([66,75,84,83])
		p.setSequenceLine([78,87,96])
		
		self.assertEqual(p.countSolutions(test=True),'1:123584796946712835578936421832157964457369182691248573269475318385691247714823659','Failed No Seven - Sequences')
		
if __name__ == '__main__':
    unittest.main()