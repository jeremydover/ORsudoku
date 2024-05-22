import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Hooked
	# Author: dumediat
	# Link: https://tinyurl.com/yc3ppdvw
	# Constraints tested: setRunOnRenbanLine, setRenbanLine, setXSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRunOnRenbanLine([31,21,12,13,24,34,44,55,66,76,86,97,98,89,79])
		p.setRenbanLine([22,32])
		p.setRenbanLine([36,47,38])
		p.setRenbanLine([52,61])
		p.setRenbanLine([72,63,74])
		p.setRenbanLine([78,88])
		p.setXSum(3,1,p.Row,25)
		p.setXSum(1,3,p.Col,20)
		p.setXSum(1,6,p.Col,16)
		p.setXSum(8,9,p.Row,28)
		p.setXSum(9,7,p.Col,17)
		p.setXSum(9,2,p.Col,26)
		
		self.assertEqual(p.countSolutions(test=True),'1:945783261381269754672154938794321586528647193136895472859432617413976825267518349','Failed Hooked')
		
if __name__ == '__main__':
    unittest.main()