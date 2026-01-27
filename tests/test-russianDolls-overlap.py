import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Overlapping Matryoshka
	# Author: timotab
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000P83
	# Constraints tested: setRussianDollSum,setOdd,setEven
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRussianDollSum(1,7,p.Col,7,'lex')
		p.setRussianDollSum(1,8,p.Col,17,'lex')
		p.setRussianDollSum(1,9,p.Col,[9,17,5,3],'lex')
		p.setRussianDollSum(1,1,p.Row,[3,17],'lex')
		p.setRussianDollSum(2,1,p.Row,[8,8],'lex')
		p.setRussianDollSum(6,1,p.Row,7,'lex')
		p.setRussianDollSum(7,1,p.Row,[15,9,5,4],'lex')
		p.setRussianDollSum(8,1,p.Row,[9,7,9],'lex')
		p.setRussianDollSum(9,1,p.Row,5,'lex')
		p.setOdd(84)
		p.setEven(59)
		
		self.assertEqual(p.countSolutions(test=True),'1:231876495958342176746519238315298764879634512462751983687925341594163827123487659','Failed Overlapping Matryoshka')
		
if __name__ == '__main__':
    unittest.main()