import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Spotting the 8 ball
	# Author: Riffclown
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000A08
	# Constraints tested: setGivenArray,setNeighborSumArray,setKropkiWhiteArraysetArrow
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setNeighborSumArray([13,17,53,57,64,66,75,91,99])
		p.setArrow([22,11,12])
		p.setArrow([25,35,45])
		p.setArrow([28,19,18])
		p.setArrow([68,78,88])
		p.setArrow([82,72,62])
		p.setGivenArray([558,696])
		p.setKropkiWhiteArray([381,621,950])
		
		self.assertEqual(p.countSolutions(test=True),'1:519463827264758391873219564981645273637182945452937186748391652196524738325876419','Failed Spotting the 8 ball')
		
if __name__ == '__main__':
    unittest.main()