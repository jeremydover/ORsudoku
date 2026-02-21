import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Dutch Arrows
	# Author: juggler
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000R8Z
	# Constraints tested: setConditionalCountLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setConditionalCountLine([21,32,43,54,65,76,87,98],p.getCellVar(1,0),[('Difference',1,p.GE,4)],[['Last']])
		p.setConditionalCountLine([27,36,45,54,63,72,81],p.getCellVar(1,6),[('Difference',1,p.GE,4)],[['Last']])
		p.setConditionalCountLine([35,46,57,68,79],p.getCellVar(2,4),[('Difference',1,p.GE,4)],[['Last']])
		p.setConditionalCountLine([38,27,16],p.getCellVar(2,7),[('Difference',1,p.GE,4)],[['Last']])
		p.setConditionalCountLine([47,57,67,77,87,97],p.getCellVar(3,6),[('Difference',1,p.GE,4)],[['Last']])
		p.setConditionalCountLine([48,37,26,15],p.getCellVar(3,7),[('Difference',1,p.GE,4)],[['Last']])
		p.setConditionalCountLine([58,47,36,25,14],p.getCellVar(4,7),[('Difference',1,p.GE,4)],[['Last']])
		p.setConditionalCountLine([68,57,46,35,24,13],p.getCellVar(5,7),[('Difference',1,p.GE,4)],[['Last']])
		p.setConditionalCountLine([71,62,53,44,35,26,17],p.getCellVar(6,0),[('Difference',1,p.GE,4)],[['Last']])
		p.setConditionalCountLine([73,63,53,43,33,23,13],p.getCellVar(6,2),[('Difference',1,p.GE,4)],[['Last']])
		p.setConditionalCountLine([74,65,56,47,38,29],p.getCellVar(6,3),[('Difference',1,p.GE,4)],[['Last']])
		
		self.assertEqual(p.countSolutions(test=True),'1:248576193371829654965431728457918236639254817812763945523187469184695372796342581','Failed Dutch Arrows')
		
if __name__ == '__main__':
    unittest.main()