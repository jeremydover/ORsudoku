import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (331) - Sandwiched Sum Skyscrapers Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00073S
	# Constraints tested: setRaySum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRaySum(1,1,p.Col,24,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(1,2,p.Col,15,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(1,3,p.Col,15,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(1,4,p.Col,19,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(1,5,p.Col,19,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(1,6,p.Col,41,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(1,7,p.Col,16,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(1,8,p.Col,20,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(1,9,p.Col,17,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		
		p.setRaySum(1,1,p.Row,19,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(2,1,p.Row,20,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(3,1,p.Row,19,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(4,1,p.Row,17,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(5,1,p.Row,17,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(6,1,p.Row,16,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(7,1,p.Row,19,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(8,1,p.Row,23,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		p.setRaySum(9,1,p.Row,40,('DigitReached',1),[['Skyscrapers']],[('DigitReached',9)],forceTermination=False,includeSelf=False,failedTerminationBehavior='zero')
		
		self.assertEqual(p.countSolutions(test=True),'1:642581379138792645759364128426935781371846592895217463564128937213479856987653214','Failed Sudoku Variants Series (331) - Sandwiched Sum Skyscrapers Sudoku')
		
if __name__ == '__main__':
    unittest.main()