import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (439) - Top Heavy Parity
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000OXH
	# Constraints tested: setTopDownCondition, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setTopDownCondition([['ParityAfter']],[('Decrease','after')],1)
		p.setGivenArray([141,177,236,298,379,424,455,482,516,591,623,658,685,738,817,875,933,967])
		
		self.assertEqual(p.countSolutions(test=True),'1:489126735376495218152378946847651329695234871231789654928513467714862593563947182','Failed Sudoku Variants Series (439) - Top Heavy Parity')
		
if __name__ == '__main__':
    unittest.main()