import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (329) - Lucky Charms Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0006Y9
	# Constraints tested: setSweeper, setSweeperNegative, setCloneRegion
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSweeper(1,6,[('RelatedDigit',1,p.LE,1,1),('RelatedDigit',1,p.GE,1,-1)],includeSelf=False)
		p.setSweeper(1,9)
		p.setSweeper(2,5)
		p.setSweeper(2,8)
		p.setSweeper(3,7)
		p.setSweeper(4,1)
		p.setSweeper(4,4)
		p.setSweeper(4,5)
		p.setSweeper(5,5)
		p.setSweeper(5,6)
		p.setSweeper(6,2)
		p.setSweeper(6,8)
		p.setSweeper(7,5)
		p.setSweeperNegative()
		
		p.setCloneRegion([[16],[28],[55]])
		p.setCloneRegion([[19],[25]])
		p.setCloneRegion([[41],[56],[68],[75]])
		p.setCloneRegion([[45],[62]])
		
		self.assertEqual(p.countSolutions(test=True),'1:986371542475928613213546789329457861748613295651892437564739128197284356832165974','Failed Sudoku Variants Series (329) - Lucky Charms Sudoku')
		
if __name__ == '__main__':
    unittest.main()