import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Tritabs
	# Author: Maggie & BremSter
	# Link: https://sudokupad.app/fdo/tritabs
	# Constraints tested: setTripleTabs
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setTripleTab(1,2,p.Down,[1,2,3])
		p.setTripleTab(1,3,p.Right,[1,2,3])
		p.setTripleTab(1,9,p.Down,[3])
		p.setTripleTab(2,7,p.Right,[6])
		p.setTripleTab(3,2,p.Down,[3,4,5])
		p.setTripleTab(3,5,p.Left,[7])
		p.setTripleTab(3,8,p.Left,[1,4,5])
		p.setTripleTab(5,1,p.Right,[1,8])
		p.setTripleTab(5,6,p.Up,[6])
		p.setTripleTab(5,9,p.Left,[4,6])
		p.setTripleTab(6,3,p.Down,[2,4])
		p.setTripleTab(6,6,p.Right,[7,8])
		p.setTripleTab(7,9,p.Left,[1,5,9])
		p.setTripleTab(8,5,p.Up,[1])
		p.setTripleTab(8,6,p.Left,[6,7,8])
		p.setTripleTab(9,9,p.Left,[5,7,9])
			
		self.assertEqual(p.countSolutions(test=True),'1:965123874413978265827654193738496521251837649649512387374265918596781432182349756','Failed Tritabs')
		
if __name__ == '__main__':
    unittest.main()