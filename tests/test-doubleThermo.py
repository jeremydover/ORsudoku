import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Double Thermo #4
	# Author: Reverend
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0004Q1
	# Constraints tested: setGivenArray,setDoubleThermo
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)	
		p.setGivenArray([833,875,956])
		p.setDoubleThermo([11,21,31,41,52])
		p.setDoubleThermo([15,24,23,12])
		p.setDoubleThermo([15,26,27,18])
		p.setDoubleThermo([19,29,39,49,58])
		p.setDoubleThermo([42,43,54,65,75])
		p.setDoubleThermo([48,47,56,65,75])
		p.setDoubleThermo([51,61,71,82,83])
		p.setDoubleThermo([59,69,79,88,87])
		p.setDoubleThermo([55,44,33,32])
		p.setDoubleThermo([55,46,37,38])
		p.setDoubleThermo([95,94,93,92,81])
		p.setDoubleThermo([95,96,97,98,89])
		self.assertEqual(p.countSolutions(test=True),'1:184927635329654817567183249738219456492536781651478923846395172913742568275861394','Failed Double Thermo #4')
		
if __name__ == '__main__':
    unittest.main()