import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: ReflX-Sum
	# Author: Twototenth
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00094V
	# Constraints tested: setXSum,setKropkiWhiteArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setXSum(1,2,p.Col,18)
		p.setXSum(1,5,p.Col,28)
		p.setXSum(1,7,p.Col,19)
		p.setXSum(3,1,p.Row,34)
		p.setXSum(4,1,p.Row,8)
		p.setXSum(7,1,p.Row,31)
		p.setXSum(3,9,p.Row,34)
		p.setXSum(4,9,p.Row,8)
		p.setXSum(7,9,p.Row,31)
		p.setXSum(9,2,p.Col,18)
		p.setXSum(9,5,p.Col,28)
		p.setXSum(9,7,p.Col,19)
		p.setKropkiWhiteArray([230,830])
			
		self.assertEqual(p.countSolutions(test=True),'1:854769312926513784713428956267985143348271695591346278689134527475692831132857469','Failed ReflX-Sum')
		
if __name__ == '__main__':
    unittest.main()