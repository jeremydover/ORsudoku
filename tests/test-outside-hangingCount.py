import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (301) - Median Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00051E
	# Constraints tested: setOutside, setHangingCount, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		for x in [(1,1,p.Col,5),(1,2,p.Col,6),(1,3,p.Col,4),(1,4,p.Col,3),(1,5,p.Col,5),(1,6,p.Col,7),(1,7,p.Col,5),(1,8,p.Col,4),(1,9,p.Col,6),(1,9,p.Row,6),(2,9,p.Row,4),(3,9,p.Row,5),(4,9,p.Row,6),(5,9,p.Row,3),(6,9,p.Row,7),(7,9,p.Row,5),(8,9,p.Row,2),(9,9,p.Row,8),(9,1,p.Col,3),(9,2,p.Col,4),(9,3,p.Col,6),(9,4,p.Col,7),(9,5,p.Col,3),(9,6,p.Col,5),(9,7,p.Col,6),(9,8,p.Col,5),(9,9,p.Col,3),(1,1,p.Row,4),(2,1,p.Row,8),(3,1,p.Row,6),(4,1,p.Row,7),(5,1,p.Row,5),(6,1,p.Row,3),(7,1,p.Row,6),(8,1,p.Row,5),(9,1,p.Row,2)]:
			p.setOutside(x[0],x[1],x[2],[x[3]])
			p.setHangingCount(x[0],x[1],x[2],1,[('Magnitude',p.GE,x[3]+1)],[('Fixed',3)])
			p.setHangingCount(x[0],x[1],x[2],1,[('Magnitude',p.LE,x[3]-1)],[('Fixed',3)])
	
		p.setGivenArray([451,659])
		
		self.assertEqual(p.countSolutions(test=True),'1:524387916189652347763149582478513269952876134631294875846921753395768421217435698','Failed Sudoku Variants Series (301) - Median Sudoku')
		
if __name__ == '__main__':
    unittest.main()