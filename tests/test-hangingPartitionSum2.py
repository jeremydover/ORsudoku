import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Daedalus Parity
	# Author: jeremydover
	# Link: https://sudokupad.app/0p7v504kai
	# Constraints tested: setHangingPartitionSum, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingPartitionSum(1,1,p.Col,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(1,2,p.Col,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(1,3,p.Col,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(1,4,p.Col,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(1,5,p.Col,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(1,6,p.Col,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(1,7,p.Col,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(1,8,p.Col,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(1,9,p.Col,['ParityRun'],['AllAre',p.LE,9])
		
		p.setHangingPartitionSum(1,1,p.Row,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(2,1,p.Row,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(3,1,p.Row,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(4,1,p.Row,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(5,1,p.Row,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(6,1,p.Row,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(7,1,p.Row,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(8,1,p.Row,['ParityRun'],['AllAre',p.LE,9])
		p.setHangingPartitionSum(9,1,p.Row,['ParityRun'],['AllAre',p.LE,9])
		
		p.setGivenArray([258,559,855,437,796,526,373,595])
		
		self.assertEqual(p.countSolutions(test=True),'1:983476512215389674674512389527163498361894725498725163749231856132658947856947231','Failed Daedalus Parity')
		
if __name__ == '__main__':
    unittest.main()