import unittest
from crustSandwichSudoku import crustSandwichSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Crusties
	# Author: RockyRoer
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000AZZ
	# Constraints tested: crustSandwichSudoku, setSandwichSum, setCrustHasLength
	
	def test_puzzle(self):
		p = crustSandwichSudoku(3)
		p.setSandwichSum(1,1,p.Row,35)
		p.setSandwichSum(2,1,p.Row,13)
		p.setSandwichSum(4,1,p.Row,18)
		p.setSandwichSum(9,1,p.Row,9)
		p.setSandwichSum(1,1,p.Col,3)
		p.setSandwichSum(1,3,p.Col,8)
		p.setSandwichSum(1,4,p.Col,35)
		p.setSandwichSum(1,6,p.Col,26)
		p.setSandwichSum(1,9,p.Col,7)
		p.setCrustHasLength()
		
		self.assertEqual(p.countSolutions(test=True),'1:786142953394685271125937684539814762241769835678523149813256497952478316467391528100000001000100100100010000010001000001000001000010010001000100010000010000101000','Failed Crusties')
		
if __name__ == '__main__':
    unittest.main()