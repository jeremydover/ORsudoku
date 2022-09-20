import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Blank Spaces
	# Author: XeonRisq
	# Link: https://link.sudokupad.app/polar-blankspaces
	# Constraints tested: setEvenOddArray, setLittleKiller
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setOddEvenArray([120,140,280,321,451,480,511,521,560,571,631,661,671,730,740,750,781,821,890,930,960])
		p.setLittleKiller(1,2,2,3,52)
		p.setLittleKiller(1,4,2,3,9)
		p.setLittleKiller(1,5,2,4,23)
		p.setLittleKiller(3,9,4,8,49)
		p.setLittleKiller(3,9,2,8,6)
		p.setLittleKiller(8,9,9,8,11)
		p.setLittleKiller(7,1,8,2,20)
		p.setLittleKiller(5,1,6,2,10)
		p.setLittleKiller(4,1,5,2,26)
		
		self.assertEqual(p.findSolution(test=True),'584263179693571824217894653349156782176328945825749316732685491951437268468912537','Failed Blank Spaces')
		
if __name__ == '__main__':
    unittest.main()