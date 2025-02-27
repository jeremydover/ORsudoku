import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (004) - Position Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0001US
	# Constraints tested: setRankedCage, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRankedCage([11,12,13],[(2,3)])
		p.setRankedCage([21,22,23],[(1,3)])
		p.setRankedCage([31,32,33],[(1,3)])
		p.setRankedCage([41,42,43],[(1,3)])
		p.setRankedCage([51,52,53],[(2,3)])
		p.setRankedCage([61,62,63],[(2,3)])
		p.setRankedCage([71,72,73],[(3,3)])
		p.setRankedCage([81,82,83],[(2,3)])
		p.setRankedCage([91,92,93],[(3,3)])
		
		p.setRankedCage([91,81,71],[(3,3)])
		p.setRankedCage([92,82,72],[(2,3)])
		p.setRankedCage([93,83,73],[(1,3)])
		p.setRankedCage([94,84,74],[(2,3)])
		p.setRankedCage([95,85,75],[(1,3)])
		p.setRankedCage([96,86,76],[(3,3)])
		p.setRankedCage([97,87,77],[(2,3)])
		p.setRankedCage([98,88,78],[(2,3)])
		p.setRankedCage([99,89,79],[(2,3)])
		
		p.setRankedCage([99,98,97],[(2,3)])
		p.setRankedCage([89,88,87],[(2,3)])
		p.setRankedCage([79,78,77],[(2,3)])
		p.setRankedCage([69,68,67],[(3,3)])
		p.setRankedCage([59,58,57],[(3,3)])
		p.setRankedCage([49,48,47],[(1,3)])
		p.setRankedCage([39,38,37],[(1,3)])
		p.setRankedCage([29,28,27],[(3,3)])
		p.setRankedCage([19,18,17],[(3,3)])
		
		p.setRankedCage([19,29,39],[(1,3)])
		p.setRankedCage([18,28,38],[(3,3)])
		p.setRankedCage([17,27,37],[(1,3)])
		p.setRankedCage([16,26,36],[(2,3)])
		p.setRankedCage([15,25,35],[(2,3)])
		p.setRankedCage([14,24,34],[(1,3)])
		p.setRankedCage([13,23,33],[(1,3)])
		p.setRankedCage([12,22,32],[(2,3)])
		p.setRankedCage([11,21,31],[(3,3)])
	
		p.setGivenArray([242,266,332,376,422,486,628,683,738,773,848,863])
		
		self.assertEqual(p.countSolutions(test=True),'1:365714928874296513912385647423578169196432875587961432748629351251843796639157284','Failed Sudoku Variants Series (004) - Position Sudoku')
		
if __name__ == '__main__':
    unittest.main()