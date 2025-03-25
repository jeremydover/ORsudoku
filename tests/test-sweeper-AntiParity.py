import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (252) - Odd-Even Stars Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002Z5
	# Constraints tested: setSweeper, setSweeperNegative, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSweeper(1,2,[('DoNotMatchParity',1)],includeSelf=False,orthogonalOnly=True,allInsteadOfValue=True)
		p.setSweeper(1,3)
		p.setSweeper(1,4)
		p.setSweeper(1,7)
		p.setSweeper(4,5)
		p.setSweeper(4,6)
		p.setSweeper(5,1)
		p.setSweeper(7,7)
		p.setSweeper(8,2)
		p.setSweeperNegative()
		
		p.setGivenArray([334,341,383,433,481,576,595,652,757,843,951,979,992])
			
		self.assertEqual(p.countSolutions(test=True),'1:961853274352746198874192536283567419147938625695421387416279853529384761738615942','Failed Sudoku Variants Series (252) - Odd-Even Stars Sudoku')
		
if __name__ == '__main__':
    unittest.main()