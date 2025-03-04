import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (365) - Skyscrapers after 1 Sudoku
	# Author: Richard
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009KL
	# Constraints tested: setRayCount
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRayCount(1,1,p.Row,4,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(2,1,p.Row,1,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(9,1,p.Row,0,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		
		p.setRayCount(1,3,p.Col,5,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(1,4,p.Col,2,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(1,5,p.Col,3,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(1,7,p.Col,3,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(1,8,p.Col,4,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		
		p.setRayCount(2,9,p.Row,3,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(3,9,p.Row,2,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(4,9,p.Row,4,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(6,9,p.Row,4,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(7,9,p.Row,0,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(9,9,p.Row,4,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		
		p.setRayCount(9,1,p.Col,4,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(9,4,p.Col,2,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		p.setRayCount(9,5,p.Col,5,['DigitReached',1],[['Skyscrapers']],[['Last']],backward=False,includeSelf=False)
		
		self.assertEqual(p.countSolutions(test=True),'1:321478659954362187786159432697845213218936745543217968169523874432781596875694321','Failed Sudoku Variants Series (365) - Skyscrapers after 1 Sudoku')
		
if __name__ == '__main__':
    unittest.main()