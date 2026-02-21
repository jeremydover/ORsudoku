import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (454) - Little Thermometers
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000QTO
	# Constraints tested: setPartitionSumLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setPartitionSumLine([13,22,31],['AscendingRun'],['OneSuitablyLongIs',p.EQ,21,3])
		p.setPartitionSumLine([15,24,33,42,51],['AscendingRun'],['OneSuitablyLongIs',p.EQ,16,3])
		p.setPartitionSumLine([16,25,34,43,52,61],['AscendingRun'],['OneSuitablyLongIs',p.EQ,20,3])
		p.setPartitionSumLine([39,28,17],['AscendingRun'],['OneSuitablyLongIs',p.EQ,13,3])
		p.setPartitionSumLine([49,38,27,16],['AscendingRun'],['OneSuitablyLongIs',p.EQ,7,3])
		p.setPartitionSumLine([95,86,77,68,59],['AscendingRun'],['OneSuitablyLongIs',p.EQ,15,3])
		p.setPartitionSumLine([94,85,76,67,58,49],['AscendingRun'],['OneSuitablyLongIs',p.EQ,34,3])
		p.setPartitionSumLine([61,72,83,94],['AscendingRun'],['OneSuitablyLongIs',p.EQ,25,3])
		p.setPartitionSumLine([71,82,93],['AscendingRun'],['OneSuitablyLongIs',p.EQ,17,3])
		
		self.assertEqual(p.countSolutions(test=True),'1:835214697671398245924567813586472139792631584413859762359786421267143958148925376','Failed Sudoku Variants Series (454) - Little Thermometers')
		
if __name__ == '__main__':
    unittest.main()