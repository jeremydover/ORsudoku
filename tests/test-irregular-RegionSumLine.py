import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Irregional
	# Author: Riffclown
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0009JQ
	# Constraints tested: setRegion,setGivenArray,setRegionSumLine
	# Note: published puzzle has additional constraint that all region sum lines have same sum
	# We have no easy way to model this constraint, but it gives us a good multi-answer test case.
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3,irregular=True)
		p.setRegion([11,12,21,22,23,31,41,42,43])
		p.setRegion([13,14,15,16,24,25,26,36,37])
		p.setRegion([17,18,19,27,28,29,38,47,48])
		p.setRegion([32,33,34,35,45,55,65,66,67])
		p.setRegion([39,46,49,56,57,58,59,68,78])
		p.setRegion([44,51,52,53,54,61,62,64,74])
		p.setRegion([63,71,72,73,81,83,84,85,91])
		p.setRegion([69,75,76,77,79,86,87,88,89])
		p.setRegion([82,92,93,94,95,96,97,98,99])
		p.setGivenArray([266,729])
		p.setRegionSumLine([26,37,27,28])
		p.setRegionSumLine([24,34,35,45,56,46,47])
		p.setRegionSumLine([53,63,73])
		p.setRegionSumLine([65,66,76,85,94,93,92])
		p.setRegionSumLine([68,69,79])
		
		self.assertEqual(p.countSolutions(test=True),'2:813754962274896351589431276936215847158673429741962583497328615362587194625149738853974162931826475278431596746215839419653728387562941592748613164389257625197384','Failed Irregional')
		
if __name__ == '__main__':
    unittest.main()