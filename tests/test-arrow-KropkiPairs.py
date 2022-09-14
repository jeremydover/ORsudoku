import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Tidal Currents
	# Author: MavericksJD
	# Link: https://tinyurl.com/dz2r9ue4
	# Constraints tested: setArrow, setKropkiWhiteArray, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setKropkiWhiteArray([341,391,611,761])
		p.setGivenArray([198,318,792,914])
		p.setArrow([41,32,21,11])
		p.setArrow([22,13,14])
		p.setArrow([22,33,34,35])
		p.setArrow([16,25,24])
		p.setArrow([16,27,28])
		p.setArrow([38,48,57])
		p.setArrow([53,44,35])
		p.setArrow([54,64,55,46])
		p.setArrow([57,66,75])
		p.setArrow([69,78,89,99])
		p.setArrow([72,62,53])
		p.setArrow([94,83,82])
		p.setArrow([94,85,86])
		p.setArrow([88,77,76,75])
		p.setArrow([88,97,96])
		
		self.assertEqual(p.findSolution(test=True),'135497268297168345864235197948371526516829734723546819689713452372654981451982673','Failed Tidal Currents')
		
if __name__ == '__main__':
    unittest.main()