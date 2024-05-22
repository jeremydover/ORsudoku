import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Long Con
	# Author: Raumplaner
	# Link: https://tinyurl.com/Quattroquadri-LongCon
	# Constraints tested: quattroQuadri, setEntropicLines, setKropkiArray
	
	def test_puzzle(self):
		p = ORsudoku.quattroQuadri(3)
		p.setEntropicLine([12,22,11,21,31])
		p.setEntropicLine([23,32,41,42,43,52,61,62,63,53,54,64,65,66,55,44,45,46,35])
		p.setEntropicLine([34,24,14,25,36,26,16])
		p.setKropkiArray([1201,1210,2300,3110,3200,5210,5410,5510])
		
		self.assertEqual(p.countSolutions(test=True),'1:936458142376587912419285863741275639','Failed Long Con')
		
if __name__ == '__main__':
    unittest.main()