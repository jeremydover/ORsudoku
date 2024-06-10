import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: -X Sums
	# Author: jeremydover
	# Link: https://tinyurl.com/2mvu9jxf
	# Constraints tested: negatorSudoku, setXSum
	
	def test_puzzle(self):
		p = ORsudoku.negatorSudoku(3)
		p.setXSum(1,1,p.Row,43)
		p.setXSum(1,9,p.Row,8)
		p.setXSum(7,1,p.Row,43)
		p.setXSum(7,9,p.Row,9)
		p.setXSum(1,8,p.Col,-3)
		p.setXSum(9,8,p.Col,28)
		p.setXSum(1,5,p.Col,41)
		p.setXSum(9,5,p.Col,30)
		p.setXSum(8,1,p.Row,2)
		p.setXSum(8,9,p.Row,28)
		p.setXSum(1,1,p.Col,39)
		p.setXSum(9,1,p.Col,33)
		p.setXSum(2,1,p.Row,15)
		p.setXSum(2,9,p.Row,23)
		p.setXSum(1,6,p.Col,8)
		p.setXSum(9,2,p.Col,12)
		p.setXSum(5,1,p.Row,28)
		p.setXSum(5,9,p.Row,19)
		p.setXSum(3,1,p.Row,12)
		
		self.assertEqual(p.countSolutions(test=True),'1:956781234387462915421593678235874169649135827178629543814356792593217486762948351000001000100000000000000010001000000000000100000100000000000001010000000000010000','Failed -X Sum')
		
if __name__ == '__main__':
    unittest.main()
	
	
