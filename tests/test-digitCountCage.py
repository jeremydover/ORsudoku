import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (258) - Anti Windoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00030G
	# Constraints tested: setDigitCountCage, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([113,128,217,251,282,339,352,378,523,534,575,586,733,757,822,858,884])
		p.setDigitCountCage([22,23,24,32,33,34,42,43,44],4)
		p.setDigitCountCage([26,27,28,36,37,38,46,47,48],4)
		p.setDigitCountCage([62,63,64,72,73,74,82,83,84],4)
		p.setDigitCountCage([66,67,68,76,77,78,86,87,88],4)
			
		self.assertEqual(p.countSolutions(test=True),'1:382745619746918325519623874961452738234897561875361492153274986627589143498136257','Failed Sudoku Variants Series (258) - Anti Windoku')
		
if __name__ == '__main__':
    unittest.main()