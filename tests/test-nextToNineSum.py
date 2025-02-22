import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sum Next to 9
	# Author: clover!
	# Link: https://sudokupad.app/3azp8z15kx
	# Constraints tested: setGivenArray,setNextToNineSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([128,295,341,352,471,531,572,632,751,762,814,983])
		p.setNextToNineSum(1,1,p.Col,5)
		p.setNextToNineSum(1,2,p.Col,2)
		p.setNextToNineSum(1,4,p.Col,11)
		p.setNextToNineSum(1,5,p.Col,11)
		p.setNextToNineSum(1,6,p.Col,11)
		p.setNextToNineSum(1,8,p.Col,2)
		p.setNextToNineSum(1,9,p.Col,6)
		
		p.setNextToNineSum(1,1,p.Row,5)
		p.setNextToNineSum(2,1,p.Row,1)
		p.setNextToNineSum(5,1,p.Row,7)
		p.setNextToNineSum(6,1,p.Row,7)
		p.setNextToNineSum(8,1,p.Row,1)
		p.setNextToNineSum(9,1,p.Row,6)
			
		self.assertEqual(p.countSolutions(test=True),'1:287536491916784325354129876539267148861493257742851963673912584428375619195648732','Failed Sum Next to 9')
		
if __name__ == '__main__':
    unittest.main()