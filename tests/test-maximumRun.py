import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (015) - Maximum Triplet Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0001X7
	# Constraints tested: setMaximumTriplet, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([117,149,195,239,283,328,377,413,464,551,642,691,738,785,826,872,919,962,993])
		p.setMaximumTriplet(1,1,p.Col,18)
		p.setMaximumTriplet(1,2,p.Col,21)
		p.setMaximumTriplet(1,5,p.Col,19)
		p.setMaximumTriplet(1,6,p.Col,17)
		p.setMaximumTriplet(1,9,p.Col,23)
		
		p.setMaximumTriplet(3,1,p.Row,18)
		p.setMaximumTriplet(5,1,p.Row,23)
		p.setMaximumTriplet(6,1,p.Row,18)
		p.setMaximumTriplet(7,1,p.Row,21)
		p.setMaximumTriplet(9,1,p.Row,20)
		
		self.assertEqual(p.countSolutions(test=True),'1:731928465629745138584163729312594876896317542457286391278631954163459287945872613','Failed Sudoku Variants Series (015) - Maximum Triplet Sudoku')
		
if __name__ == '__main__':
    unittest.main()