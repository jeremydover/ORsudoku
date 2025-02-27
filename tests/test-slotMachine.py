import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (087) - Slot Machine
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002A7
	# Constraints tested: setSlotMachine, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSlotMachine()
		p.setGivenArray([166,179,219,312,331,432,446,493,547,562,615,664,676,777,799,896,936,944])
		
		self.assertEqual(p.countSolutions(test=True),'1:437516982985327164261849375872651493694732518513984627328165749149273856756498231','Failed Sudoku Variants Series (087) - Slot Machine')
		
if __name__ == '__main__':
    unittest.main()