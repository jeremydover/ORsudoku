import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (248) - Ordering Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002Y8
	# Constraints tested: setOrderSumCages, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setOrderSumCages([[23,24],[66,67],[58,59],[71,72],[11,12],[86,87],[78,79],[31,32],[18,19],[43,44],[91,92],[83,84],[51,52],[46,47],[98,99],[63,64],[26,27],[38,39]],readAsNumber=True)
	
		p.setGivenArray([141,167,218,292,542,568,748,765,817,899,934,956,972])
			
		self.assertEqual(p.countSolutions(test=True),'1:249187356861359742357624198415796823673248915928531467192875634736412589584963271','Failed Sudoku Variants Series (248) - Ordering Sudoku')
		
if __name__ == '__main__':
    unittest.main()