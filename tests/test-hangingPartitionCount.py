import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Parity Sandwich Party [Sandwich, Parity, a Kropki Dot]
	# Author: fractalJim
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000I74
	# Constraints tested: setSandwichSum,setHangingPartitionCount,setKropkiWhite
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSandwichSum(1,1,p.Col,2)
		p.setSandwichSum(1,2,p.Col,25)
		p.setSandwichSum(1,3,p.Col,8)
		p.setSandwichSum(1,5,p.Col,21)
		p.setSandwichSum(1,7,p.Col,4)
		p.setSandwichSum(1,9,p.Col,15)
		p.setSandwichSum(2,1,p.Row,17)
		p.setSandwichSum(4,1,p.Row,15)
		p.setSandwichSum(5,1,p.Row,11)
		p.setSandwichSum(8,1,p.Row,27)
		p.setSandwichSum(9,1,p.Row,5)
		
		p.setHangingPartitionCount(9,1,p.Col,['ParityRun'],['BiggestIs',4])
		p.setHangingPartitionCount(9,2,p.Col,['ParityRun'],['BiggestIs',4])
		p.setHangingPartitionCount(9,3,p.Col,['ParityRun'],['BiggestIs',4])
		p.setHangingPartitionCount(9,5,p.Col,['ParityRun'],['BiggestIs',2])
		p.setHangingPartitionCount(9,6,p.Col,['ParityRun'],['BiggestIs',2])
		p.setHangingPartitionCount(9,7,p.Col,['ParityRun'],['BiggestIs',2])
		p.setHangingPartitionCount(9,8,p.Col,['ParityRun'],['BiggestIs',2])
		
		p.setHangingPartitionCount(1,9,p.Row,['ParityRun'],['BiggestIs',5])
		p.setHangingPartitionCount(2,9,p.Row,['ParityRun'],['BiggestIs',4])
		p.setHangingPartitionCount(3,9,p.Row,['ParityRun'],['BiggestIs',3])
		p.setHangingPartitionCount(4,9,p.Row,['ParityRun'],['BiggestIs',5])
		p.setHangingPartitionCount(5,9,p.Row,['ParityRun'],['BiggestIs',1])
		p.setHangingPartitionCount(6,9,p.Row,['ParityRun'],['BiggestIs',3])
		p.setHangingPartitionCount(7,9,p.Row,['ParityRun'],['BiggestIs',4])
		p.setHangingPartitionCount(8,9,p.Row,['ParityRun'],['BiggestIs',4])
		
		p.setKropkiWhite(540)
		
		self.assertEqual(p.countSolutions(test=True),'1:437591826692483175158762439261375948945218367783946251329157684516824793874639512','Failed Parity Sandwich Party [Sandwich, Parity, a Kropki Dot]')
		
if __name__ == '__main__':
    unittest.main()