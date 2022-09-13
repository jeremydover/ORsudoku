import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Xentropic Lines
	# Author: jeremydover and Raumplaner
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008W9
	# Constraints tested: setGivenArray, setEntropicLine, setXSudokuMain, setXSudokuOff
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([146,184,212,411,697,978])
		p.setXSudokuMain()
		p.setXSudokuOff()
		p.setEntropicLine([33,42,51,61,62,72,73,74,85,75,76,77,78,68,59,49,48,37])
		p.setEntropicLine([53,43,54,55,65,56,57])
		p.setEntropicLine([71,82,83,84,94,95,96,87,88,98,89,99])
		self.assertEqual(p.findSolution(test=True),'597682341284317596631945728149758263725163489368294157873426915952871634416539872','Failed Xentropic Lines')
		
if __name__ == '__main__':
    unittest.main()