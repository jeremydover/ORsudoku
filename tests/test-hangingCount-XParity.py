import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (357) - X-Parity Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008XQ
	# Constraints tested: setHangingCount
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingCount(1,1,p.Row,2,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(2,1,p.Row,3,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(3,1,p.Row,1,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(4,1,p.Row,2,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(7,1,p.Row,3,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(8,1,p.Row,1,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(9,1,p.Row,0,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		
		p.setHangingCount(1,1,p.Col,3,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(1,2,p.Col,0,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(1,5,p.Col,2,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(1,6,p.Col,1,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(1,7,p.Col,3,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(1,8,p.Col,2,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		p.setHangingCount(1,9,p.Col,2,[('Parity',p.EQ,0)],[('Indexed',[1],'Any')])
		
		p.setHangingCount(1,9,p.Row,1,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		p.setHangingCount(3,9,p.Row,3,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		p.setHangingCount(4,9,p.Row,3,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		p.setHangingCount(5,9,p.Row,1,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		p.setHangingCount(7,9,p.Row,2,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		p.setHangingCount(8,9,p.Row,3,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		p.setHangingCount(9,9,p.Row,1,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		
		p.setHangingCount(9,4,p.Col,2,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		p.setHangingCount(9,5,p.Col,2,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		p.setHangingCount(9,6,p.Col,2,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		p.setHangingCount(9,7,p.Col,3,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		p.setHangingCount(9,8,p.Col,2,[('Parity',p.EQ,1)],[('Indexed',[1],'Any')])
		
		self.assertEqual(p.countSolutions(test=True),'1:718932564542167398396584217421396875963875421857421639674259183235718946189643752','Failed Sudoku Variants Series (357) - X-Parity Sudoku')
		
if __name__ == '__main__':
    unittest.main()