import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Distanz Chaos Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000126
	# Constraints tested: setNonConsecutive, setGivenArray, Irregular
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p = ORsudoku.sudoku(3,irregular=True)
		p.setRegion([41,31,21,11,12,13,14,15,25])
		p.setRegion([16,17,18,26,27,28,36,37,38])
		p.setRegion([19,29,39,47,48,49,57,58,59])
		p.setRegion([22,23,24,32,33,34,42,43,44])
		p.setRegion([35,45,46,54,55,56,64,65,75])
		p.setRegion([51,52,53,61,62,63,71,81,91])
		p.setRegion([66,67,68,76,77,78,86,87,88])
		p.setRegion([69,79,89,99,98,97,96,95,85])
		p.setRegion([72,73,74,82,83,84,92,93,94])
		p.setNonConsecutive()
		p.setGivenArray([221,286,438,479,553,635,677,827,885])
	
		self.assertEqual(p.countSolutions(test=True),'1:837415296514793862296357418628574931162938574385162749741629385479286153953841627','Failed Distanz Chaos Sudoku')
		
if __name__ == '__main__':
    unittest.main()