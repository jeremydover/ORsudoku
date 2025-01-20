import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Double Dutch Sudoku Advent (9) - Next to Nine vs. Battenburg
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00024J
	# Constraints tested: setBattenburgArray, setBattenburgNegative, setNextToNine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setBattenburgArray([23,37,62,76])
		p.setBattenburgNegative()
		p.setNextToNine(1,1,p.Col,[1,4])
		p.setNextToNine(1,3,p.Col,[3])
		p.setNextToNine(1,5,p.Col,[4,5])
		p.setNextToNine(1,7,p.Col,[1])
		p.setNextToNine(1,9,p.Col,[4,8])
		
		p.setNextToNine(1,1,p.Row,[3,8])
		p.setNextToNine(2,1,p.Row,[1,3])
		p.setNextToNine(4,1,p.Row,[4,5])
		p.setNextToNine(5,1,p.Row,[2,7])
		p.setNextToNine(6,1,p.Row,[3])
		p.setNextToNine(8,1,p.Row,[1])
		p.setNextToNine(9,1,p.Row,[2,7])
	
		self.assertEqual(p.countSolutions(test=True),'1:524168937786539142391427586617382495452971863938645271145793628263854719879216354','Failed Double Dutch Sudoku Advent (9) - Next to Nine vs. Battenburg')
		
if __name__ == '__main__':
    unittest.main()