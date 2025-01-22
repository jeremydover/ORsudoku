import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Dutch Sudoku Championship 2022 Leftover - Remote Kropki Sudoku
	# Author: Richard Stolk
	# Link: hhttps://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000AAP
	# Constraints tested: setRemoteKropkiArray
	# Note: original puzzle notes a negative constraint, but solution is unique without
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRemoteKropkiArray([1130,1331,1311,1420,1610,1720,1711,1910,2430,2711,2810,3111,3230,3701,3731,3820,4230,4330,4520,4511,4800,5520,5801,5910,6200,6300,6520,6820,7321,7300,7420,7700,7921,8430,8921,9620,9600,9700,9800,9820])
			
		self.assertEqual(p.countSolutions(test=True),'1:713296485285471639649853271536148927971625843824739156492367518167582394358914762','Failed Dutch Sudoku Championship 2022 Leftover - Remote Kropki Sudoku')
		
if __name__ == '__main__':
    unittest.main()