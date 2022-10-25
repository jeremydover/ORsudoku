import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: A Magical Square
	# Author: Lisztes
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0004T9
	# Constraints tested: setCage,setXSudokuMain,setXSudokuOff,setMagicSquare,setCloneRegion
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCage([11,12,21],24)
		p.setCage([14,24],5)
		p.setCage([18,19,29],22)
		p.setCage([41,42],5)
		p.setCage([58,59],12)
		p.setCage([81,91,92],21)
		p.setCage([84,94],12)
		p.setCage([89,98,99],23)
		p.setXSudokuMain()
		p.setXSudokuOff()
		p.setMagicSquare(44)
		p.setCloneRegion([[81],[98]])
				
		self.assertEqual(p.findSolution(test=True),'872345196935216847461987352148672935327159684596834271259468713614793528783521469','Failed A Magical Square')

if __name__ == '__main__':  
    unittest.main()