import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Run-on-nabneR
	# Author: gdc
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000EZL
	# Constraints tested: setXVArray, setRunOnNabnerLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRunOnNabnerLine([51,41,31,21,11,12,13,14])
		p.setRunOnNabnerLine([16,17,18,19,29,39,49,59])
		p.setRunOnNabnerLine([23,22,32])
		p.setRunOnNabnerLine([27,28,38])
		p.setRunOnNabnerLine([81,91,92,93])
		p.setRunOnNabnerLine([97,87,88,98,99,89])
		p.setRunOnNabnerLine([33,34,35,36,37,47,57,67,77,76,86,85,84,74,73,63,53,43,33,34,35])
		p.setXVArray([(3,4,p.Horz,p.V),(6,7,p.Horz,p.V),(7,6,p.Horz,p.X)])
		
		self.assertEqual(p.countSolutions(test=True),'1:317582469984376251526149783748253196293614578651897324835761942462935817179428635','Failed Run-on-nabneR')
		
if __name__ == '__main__':
    unittest.main()