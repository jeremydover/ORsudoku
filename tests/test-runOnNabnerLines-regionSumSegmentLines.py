import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Nabner Region Sums
	# Author: gdc
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000F1H
	# Constraints tested: setRunOnNabnerLine, setRegionSegmentSumLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRunOnNabnerLine([13,23,24,25,26,35])
		p.setRunOnNabnerLine([21,32])
		p.setRunOnNabnerLine([67,57,47,38,49,59])
		p.setRunOnNabnerLine([95,86,87,88,99])
		p.setRunOnNabnerLine([43,44,54,55,65,75,74,84,94,93,82,71,61,62,63,53,43,44,54])
		p.setRegionSegmentSumLine([13,23,24,25,26,35])
		p.setRegionSegmentSumLine([67,57,47,38,49,59])
		p.setRegionSegmentSumLine([95,86,87,88,99])
		p.setRegionSegmentSumLine([61,62,63,53,43,44,54,55,65,75,74,84,94,93,82,71])
		
		self.assertEqual(p.countSolutions(test=True),'1:527869431489315726613274895392481567758693142146527389931746258274958613865132974','Failed Nabner Region Sums')
		
if __name__ == '__main__':
    unittest.main()