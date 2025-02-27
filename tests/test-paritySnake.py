import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (018) - Odd Labyrinth
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0001XO
	# Constraints tested: setParitySnake, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setParitySnake(1,1,9,9,p.Odd)
		p.setGivenArray([126,165,217,238,296,346,353,422,448,476,551,636,662,685,752,767,813,874,892,943,981])
		
		self.assertEqual(p.countSolutions(test=True),'2:164275389738194526295638174427853691583916247916742853651427938379581462842369715164275389738194526295638174427853691583916247916742853651427938379581462842369715','Failed Sudoku Variants Series (018) - Odd Labyrinth')
		
if __name__ == '__main__':
    unittest.main()