import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (368) - N-Sums - Smallest
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009P5
	# Constraints tested: setXSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setXSum(1,1,p.Row,23,depth=2,depthStyle='Smallest')
		p.setXSum(2,1,p.Row,23,depth=2,depthStyle='Smallest')
		p.setXSum(3,1,p.Row,23,depth=2,depthStyle='Smallest')
		p.setXSum(4,1,p.Row,43,depth=2,depthStyle='Smallest')
		p.setXSum(7,1,p.Row,25,depth=2,depthStyle='Smallest')
		p.setXSum(1,6,p.Col,19,depth=2,depthStyle='Smallest')
		p.setXSum(1,8,p.Col,18,depth=2,depthStyle='Smallest')
		p.setXSum(2,9,p.Row,22,depth=2,depthStyle='Smallest')
		p.setXSum(3,9,p.Row,6,depth=2,depthStyle='Smallest')
		p.setXSum(6,9,p.Row,11,depth=2,depthStyle='Smallest')
		p.setXSum(7,9,p.Row,1,depth=2,depthStyle='Smallest')
		p.setXSum(8,9,p.Row,7,depth=2,depthStyle='Smallest')
		p.setXSum(9,9,p.Row,13,depth=2,depthStyle='Smallest')
		p.setXSum(9,2,p.Col,15,depth=2,depthStyle='Smallest')
		p.setXSum(9,4,p.Col,22,depth=2,depthStyle='Smallest')
			
		self.assertEqual(p.countSolutions(test=True),'1:761243589583169247942857316896731452317524968425698173654372891139486725278915634','Failed Sudoku Variants Series (368) - N-Sums - Smallest')
		
if __name__ == '__main__':
    unittest.main()