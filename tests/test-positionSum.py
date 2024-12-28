import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku - Position Sums (Leftover DSC2024)
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000L9S
	# Constraints tested: setPositionSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setPositionSum(1,3,p.Col,13,9)
		p.setPositionSum(1,4,p.Col,11,6)
		p.setPositionSum(1,6,p.Col,valueSum=7)
		p.setPositionSum(1,7,p.Col,4,10)
		p.setPositionSum(1,9,p.Col,17,3)
		
		p.setPositionSum(3,1,p.Row,15,8)
		p.setPositionSum(4,1,p.Row,5,12)
		p.setPositionSum(6,1,p.Row,valueSum=5)
		p.setPositionSum(7,1,p.Row,12,8)
		p.setPositionSum(9,1,p.Row,15,11)
		
		self.assertEqual(p.countSolutions(test=True),'1:125974368378265149694183725417826593263591874859347216931652487546718932782439651','Failed Sudoku - Position Sums (Leftover DSC2024)')
		
if __name__ == '__main__':
    unittest.main()