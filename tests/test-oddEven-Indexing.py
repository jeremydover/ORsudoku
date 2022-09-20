import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Shipping Hub
	# Author: Sotek & Riffclown
	# Link: https://link.sudokupad.app/polar-shippinghub
	# Constraints tested: setEvenOddArray, setIndexing, setGivenArray, countSolutions
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([143,366,748,967])
		p.setEvenOddArray([221,231,271,281,331,340,371,490,520,550,580,610,731,760,771,821,831,871,881])
		p.setIndexColumn(1,True,[2,4,6,8])
		p.setIndexColumn(5,True,[2,5,6,8])
		p.setIndexColumn(9,True,[2,3,4,6,8])
		
		self.assertEqual(p.findSolution(test=True),'968315247217489356345276198132968574789543621654721839471832965893654712526197483','Failed Shipping Hub')
		#self.assertEqual(p.countSolutions(test=True),'1:968315247217489356345276198132968574789543621654721839471832965893654712526197483','Failed Shipping Hub')
		
if __name__ == '__main__':
    unittest.main()