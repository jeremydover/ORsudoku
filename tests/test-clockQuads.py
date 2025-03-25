import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (243) - Clock Faces Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002X4
	# Constraints tested: setClockQuadArray, setClockQuadNegative, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setClockQuadArray([(1,1,p.Black),(2,1,p.White),(2,2,p.Black),(2,3,p.White),(2,7,p.Black),(3,3,p.Black),(3,6,p.White),(4,3,p.White),(4,4,p.Black),(4,5,p.White),(5,3,p.Black),(5,4,p.White),(5,5,p.Black),(5,6,p.White),(5,7,p.Black),(5,8,p.White),(6,1,p.White),(6,3,p.White),(6,6,p.Black),(6,7,p.White),(6,8,p.Black),(7,4,p.Black),(7,5,p.White),(7,7,p.Black),(7,8,p.White),(8,2,p.Black),(8,4,p.White),(8,5,p.Black),(8,6,p.White),(8,8,p.Black)])
		p.setClockQuadNegative()
		p.setGivenArray([136,261,384,434,497,526,559,581,617,675,722,843,978])
			
		self.assertEqual(p.countSolutions(test=True),'1:176245983349681752258739146894513267562897314713426598621978435987354621435162879','Failed Sudoku Variants Series (243) - Clock Faces Sudoku')
		
if __name__ == '__main__':
    unittest.main()