import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (061) - Before Nine
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000268
	# Constraints tested: setGivenArray, setBeforeNine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([267,341,377,437,484,622,678,735,762,846])
		p.setBeforeNine(1,1,p.Row,19)
		p.setBeforeNine(2,1,p.Row,9)
		p.setBeforeNine(3,1,p.Row,28)
		p.setBeforeNine(4,1,p.Row,26)
		p.setBeforeNine(5,1,p.Row,28)
		p.setBeforeNine(6,1,p.Row,0)
		p.setBeforeNine(7,1,p.Row,10)
		p.setBeforeNine(8,1,p.Row,36)
		p.setBeforeNine(9,1,p.Row,6)
		p.setBeforeNine(1,1,p.Col,22)
		p.setBeforeNine(1,2,p.Col,36)
		p.setBeforeNine(1,3,p.Col,6)
		p.setBeforeNine(1,4,p.Col,22)
		p.setBeforeNine(1,5,p.Col,0)
		p.setBeforeNine(1,6,p.Col,20)
		p.setBeforeNine(1,7,p.Col,14)
		p.setBeforeNine(1,8,p.Col,7)
		p.setBeforeNine(1,9,p.Col,32)
		
		self.assertEqual(p.countSolutions(test=True),'1:476298315819537462253164798587321946364789251921456837145972683738645129692813574','Failed Sudoku Variants Series (061) - Before Nine')
		
if __name__ == '__main__':
    unittest.main()