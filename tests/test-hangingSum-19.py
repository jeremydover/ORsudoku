import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (145) - First even-odd Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002GV
	# Constraints tested: setHangingSum, setGivenArray, getCellVar
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		for x in [(1,1,p.Row,13),(2,1,p.Row,11),(3,1,p.Row,9),(5,1,p.Row,9),(7,1,p.Row,11),(8,1,p.Row,5),(9,1,p.Row,11),(1,1,p.Col,7),(1,2,p.Col,15),(1,4,p.Col,15),(1,6,p.Col,15),(1,8,p.Col,11),(1,9,p.Col,7),(9,1,p.Col,15),(9,2,p.Col,11),(9,4,p.Col,15),(9,5,p.Col,13),(9,6,p.Col,9),(9,8,p.Col,7),(9,9,p.Col,15),(1,9,p.Row,15),(2,9,p.Row,9),(3,9,p.Row,9),(5,9,p.Row,9),(7,9,p.Row,9),(8,9,p.Row,9),(9,9,p.Row,9)]:
			# A couple of things are going on here that need explaining. The variable t is the value of the first cell in the row/column...note the need to shift from 1-base to 0-base. This will always be either the first odd or first even digit. The hanging sum then looks for all of the digits which do not match the parity of the first digit, and terminates when it finds the first parity change. Hence, only this last digit, which is necessarily the first digit whose parity does not match that of t.
			s = p.model.NewIntVar(1,9,'')
			t = p.getCellVar(x[0]-1,x[1]-1)
			p.setHangingSum(x[0],x[1],x[2],s,[('DoNotMatchParity',1)],[('ParityChangeReached',1)])
			p.model.Add(s+t == x[3])
	
		p.setGivenArray([357,461,643,756])
		
		self.assertEqual(p.countSolutions(test=True),'1:573819246296435871184276593348751629721698435965324187837162954419583762652947318','Failed Sudoku Variants Series (145) - First even-odd Sudoku')
		
if __name__ == '__main__':
    unittest.main()