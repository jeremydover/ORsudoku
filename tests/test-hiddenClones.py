import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (327) - Hidden Clones Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0006TV
	# Constraints tested: setHiddenClones, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHiddenClones([22,23,32,33,34,43,44,45,54],2)
		p.setGivenArray([125,138,213,265,287,312,563,626,659,667,774,792,822,978])
		
		self.assertEqual(p.countSolutions(test=True),'1:958176324346825971217934685582461793791583246463297158179358462824619537635742819','Failed Sudoku Variants Series (327) - Hidden Clones Sudoku')
		
if __name__ == '__main__':
    unittest.main()