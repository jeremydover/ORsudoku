import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (396) - N-Sums - Odd Counter
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000C98
	# Constraints tested: setHangingSum, setHangingCount
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		for x in [(1,4,p.Col,11),(1,6,p.Col,22),(2,1,p.Row,18),(3,1,p.Row,20),(4,1,p.Row,15),(5,1,p.Row,22),(6,1,p.Row,11),(7,1,p.Row,24),(8,1,p.Row,10),(2,9,p.Row,14),(3,9,p.Row,22),(4,9,p.Row,3),(5,9,p.Row,22),(6,9,p.Row,18),(7,9,p.Row,13),(8,9,p.Row,16),(9,2,p.Col,5),(9,3,p.Col,14),(9,4,p.Col,25),(9,6,p.Col,12),(9,7,p.Col,13),(9,8,p.Col,4)]:

			numOdd = p.model.NewIntVar(0,5,'')
			p.setHangingCount(x[0],x[1],x[2],numOdd,[('Parity',p.EQ,1)],[('Fixed',6)])
			p.setHangingSum(x[0],x[1],x[2],x[3],[['All']],[('ModelVariable',numOdd)])
	
		self.assertEqual(p.countSolutions(test=True),'1:251849376378256194496137852537684921829315647164792583983471265712568439645923718','Failed Sudoku Variants Series (396) - N-Sums - Odd Counter')
		
if __name__ == '__main__':
    unittest.main()