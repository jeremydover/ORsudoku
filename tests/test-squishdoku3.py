import unittest
from squishdoku import squishdoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Squishpers
	# Author: marty_sears
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000G3M
	# Constraints tested: squishdoku, setCountingCircles, setGermanWhispersLine, setKropkiBlack, setXVVArray
	
	def test_puzzle(self):
		p = squishdoku(3)
		p.setCountingCircles([21,23,25,27,32,34,36,41,43,45,47,52,54,56,61,63,65,67,72,74,76])
		p.setGermanWhispersLine([16,15,24,35,44,53,64,73,72])
		p.setGermanWhispersLine([33,22,31,42])
		p.setGermanWhispersLine([46,57,66,55])
		p.setKropkiBlack(341)
		p.setXVVArray([221,650])
			
		self.assertEqual(p.countSolutions(test=True),'1:4583297126753473941686158342842675957394169615823','Failed Squishpers')
		
if __name__ == '__main__':
    unittest.main()