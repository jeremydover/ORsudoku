import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Same but different
	# Author: jeremydover
	# Link: https://sudokupad.app/5b0b11n4k2
	# Constraints tested: setOrthogonalCondition, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setOrthogonalCondition([('DoNotMatchParity',1)],[('Difference','previous',p.LE,1)],1)
		p.setGivenArray([225,248,267,284,476,488,934])
			
		self.assertEqual(p.countSolutions(test=True),'1:768243951159867342243951768432195687591786423687324519876432195915678234324519876','Failed Same but different')
		
if __name__ == '__main__':
    unittest.main()