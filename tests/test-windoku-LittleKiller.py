import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Little Killer Windoku
	# Author: Phistomefel
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0003B6
	# Constraints tested: setWindoku, setLittleKiller
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setWindoku()
		p.setLittleKiller(1,3,2,2,13)
		p.setLittleKiller(1,9,2,8,18)
		p.setLittleKiller(2,1,3,2,17)
		p.setLittleKiller(9,2,8,3,66)
				
		self.assertEqual(p.countSolutions(test=True),'1:586192473147385629329647185651873942832419567974256831463921758718534296295768314','Failed Little Killer Windoku')

if __name__ == '__main__':  
    unittest.main()