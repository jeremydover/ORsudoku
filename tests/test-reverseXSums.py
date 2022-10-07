import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Smus-X
	# Author: Qodec
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000BDU
	# Constraints tested: setReverseXSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setReverseXSum(1,1,p.Row,37)
		p.setReverseXSum(2,1,p.Row,37)
		p.setReverseXSum(4,1,p.Row,22)
		p.setReverseXSum(7,1,p.Row,34)
		p.setReverseXSum(9,2,p.Col,35)
		p.setReverseXSum(9,4,p.Col,15)
		p.setReverseXSum(9,6,p.Col,15)
		p.setReverseXSum(9,7,p.Col,20)
		p.setReverseXSum(6,9,p.Row,12)
		p.setReverseXSum(3,9,p.Row,6)
		p.setReverseXSum(1,9,p.Col,11)
		p.setReverseXSum(1,8,p.Col,11)
		p.setReverseXSum(1,5,p.Col,22)
		
		self.assertEqual(p.findSolution(test=True),'859641732713982564642537891384125679297463158165879243521396487436718925978254316','Failed Smus-X')
		
if __name__ == '__main__':
    unittest.main()