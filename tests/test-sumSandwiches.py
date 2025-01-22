import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (075) - Sum Sandwich
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00028S
	# Constraints tested: setSumSandwich, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSumSandwich(1,1,p.Col,[7],neg=True)
		p.setSumSandwich(1,2,p.Col,[9],neg=True)
		p.setSumSandwich(1,3,p.Col,[7],neg=True)
		p.setSumSandwich(1,4,p.Col,[],neg=True)
		p.setSumSandwich(1,5,p.Col,[7],neg=True)
		p.setSumSandwich(1,6,p.Col,[],neg=True)
		p.setSumSandwich(1,7,p.Col,[4],neg=True)
		p.setSumSandwich(1,8,p.Col,[],neg=True)
		p.setSumSandwich(1,9,p.Col,[],neg=True)
		p.setSumSandwich(1,1,p.Row,[],neg=True)
		p.setSumSandwich(2,1,p.Row,[3],neg=True)
		p.setSumSandwich(3,1,p.Row,[4],neg=True)
		p.setSumSandwich(4,1,p.Row,[5],neg=True)
		p.setSumSandwich(5,1,p.Row,[6],neg=True)
		p.setSumSandwich(6,1,p.Row,[7],neg=True)
		p.setSumSandwich(7,1,p.Row,[8],neg=True)
		p.setSumSandwich(8,1,p.Row,[9],neg=True)
		p.setSumSandwich(9,1,p.Row,[],neg=True)
		p.setGivenArray([144,193,226,268,365,418,484,625,632,845,888,911])
			
		self.assertEqual(p.countSolutions(test=True),'1:589467213761328954234195876817253649943716528652984731425839167396571482178642395','Failed Sudoku Variants Series (075) - Sum Sandwich')
		
if __name__ == '__main__':
    unittest.main()