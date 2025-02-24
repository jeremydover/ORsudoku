import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (112) - Outside Odd Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002DA
	# Constraints tested: setHangingCount, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingCount(1,3,p.Col,2,[('Parity',p.EQ,1)],[('Fixed',3)])
		p.setHangingCount(1,9,p.Col,1,[('Parity',p.EQ,1)],[('Fixed',3)])
		
		p.setHangingCount(1,9,p.Row,1,[('Parity',p.EQ,1)],[('Fixed',3)])
		p.setHangingCount(3,9,p.Row,1,[('Parity',p.EQ,1)],[('Fixed',3)])
		p.setHangingCount(5,9,p.Row,1,[('Parity',p.EQ,1)],[('Fixed',3)])
		p.setHangingCount(8,9,p.Row,1,[('Parity',p.EQ,1)],[('Fixed',3)])
		
		p.setHangingCount(9,5,p.Col,1,[('Parity',p.EQ,1)],[('Fixed',3)])
		
		p.setHangingCount(7,1,p.Row,2,[('Parity',p.EQ,1)],[('Fixed',3)])
		p.setHangingCount(9,1,p.Row,2,[('Parity',p.EQ,1)],[('Fixed',3)])
		
		p.setGivenArray([112,123,211,254,345,435,493,524,557,585,613,676,766,855,899,987,998])
			
		self.assertEqual(p.countSolutions(test=True),'1:239761584156842937487539216625418793941673852378295641794186325812357469563924178','Failed Sudoku Variants Series (112) - Outside Odd Sudoku')
		
if __name__ == '__main__':
    unittest.main()