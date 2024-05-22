import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: XY-Differences Sudoku
	# Author: glum_hippo
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0003P8
	# Constraints tested: setEvenOddArray, setGivenArray, setXYDifferenceArray, setXYDifferenceNegative
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setEvenOddArray([111,120,221,230,331,340,430,441,520,531,610,621,581,690,780,860,881,890,971,991])
		p.setGivenArray([488,495,844,949])
		p.setXYDifferenceArray([131,140,170,271,291,370,351,430,450,461,550,580,591,551,631,640,671,710,740,760,761,780,820,821,870,960])
		p.setXYDifferenceNegative()										
		
		self.assertEqual(p.countSolutions(test=True),'1:764815293958243617321679854192367485647582139835194726489731562213456978576928341','Failed XY-Differences Sudoku')
		
if __name__ == '__main__':
    unittest.main()