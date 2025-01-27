import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (371) - Sudoku Hangover
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009Y0
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,1,p.Row,20,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(3,1,p.Row,23,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(4,1,p.Row,29,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(7,1,p.Row,18,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(8,1,p.Row,14,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		
		p.setHangingSum(1,2,p.Col,31,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(1,5,p.Col,16,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(1,7,p.Col,39,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(1,8,p.Col,27,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		
		p.setHangingSum(2,9,p.Row,6,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(3,9,p.Row,16,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(6,9,p.Row,9,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(7,9,p.Row,23,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(9,9,p.Row,23,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		
		p.setHangingSum(9,2,p.Col,6,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(9,3,p.Col,17,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(9,5,p.Col,17,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
		p.setHangingSum(9,8,p.Col,16,[['All']],[('DigitSetReached',[2,4,6,8],2),('DigitSetReached',[1,3,5,7,9],2)],terminateOnFirst=False)
			
		self.assertEqual(p.countSolutions(test=True),'1:485213976376958142219746358198562734762134589534897621657421893821379465943685217','Failed Sudoku Variants Series (371) - Sudoku Hangover')
		
if __name__ == '__main__':
    unittest.main()