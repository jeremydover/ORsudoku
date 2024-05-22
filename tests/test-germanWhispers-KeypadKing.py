import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Keys to the Kingdom
	# Author: jeremydover
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00096A
	# Constraints tested: setGermanWhispersLine, setKeypadKingLine, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([255,317,472,633,957])
		p.setGermanWhispersLine([12,23,32,21,12])
		p.setGermanWhispersLine([14,15,16])
		p.setGermanWhispersLine([34,35,36])
		p.setGermanWhispersLine([44,53])
		p.setGermanWhispersLine([45,55,65,75])
		p.setGermanWhispersLine([46,57])
		p.setGermanWhispersLine([74,84])
		p.setGermanWhispersLine([77,87,98,89,79,88])
		p.setKeypadKingLine([14,24,34])
		p.setKeypadKingLine([24,15,26])
		p.setKeypadKingLine([16,26,36])
		p.setKeypadKingLine([38,28,27,18,29,28])
		p.setKeypadKingLine([42,53])
		p.setKeypadKingLine([57,48,39,49,59,69])
		p.setKeypadKingLine([59,58])
		p.setKeypadKingLine([59,68])
		p.setKeypadKingLine([72,82,92])
		p.setKeypadKingLine([81,82,83])
		p.setKeypadKingLine([74,64,54,55,56,66,76,86,96,85,86])
		p.setKeypadKingLine([85,84,94,85])
		p.setKeypadKingLine([64,65,66])
		p.setKeypadKingLine([77,88])
		
		self.assertEqual(p.countSolutions(test=True),'1:694827153231654789785391642518739264972486315463512897857963421326145978149278536','Failed Keys to the Kingdom')
		
if __name__ == '__main__':
    unittest.main()