import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: SHHHH! Not 9
	# Author: Riffclown
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000AG0
	# Constraints tested: 0-8 digits, setCage, setGermanWhispersLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3,digitSet={0,1,2,3,4,5,6,7,8})
		p.setGermanWhispersLine([12,23,24,35,46,56,67,77,87,96,95,85,74,64,55,54])
		p.setGermanWhispersLine([17,27,26,36,47])
		p.setGermanWhispersLine([19,28,38,49,58])
		p.setGermanWhispersLine([33,42,52,63,62,51,41])
		p.setGermanWhispersLine([73,84,83,82])
		p.setGermanWhispersLine([69,68,78,89])
		p.setCage([11,12,13,22],13)
		p.setCage([15,16,25],10)
		p.setCage([18,19,28],14)
		p.setCage([24,34,44,43,42],10)
		p.setCage([27,37,38],4)
		p.setCage([36,46,47],6)
		p.setCage([63,64,74],7)
		p.setCage([66,67,68,76,86],10)
		p.setCage([72,73,83],4)
		p.setCage([78,87,88,89],12)
		p.setCage([82,92,91],13)
		p.setCage([85,95,94],10)
		
		self.assertEqual(p.countSolutions(test=True),'1:018735642347126085526480317603241578175608423482573106831052764750864231264317850','Failed SHHHH! Not 9')
		
if __name__ == '__main__':
    unittest.main()