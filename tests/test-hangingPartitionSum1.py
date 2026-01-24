import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Easy Peasy Sudoku Advent (08) - Sum Triplets
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000QF4
	# Constraints tested: setHangingPartitionSum, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingPartitionSum(1,1,p.Row,['Region'],['OneIs',p.EQ,19])
		p.setHangingPartitionSum(2,1,p.Row,['Region'],['OneIs',p.EQ,8])
		p.setHangingPartitionSum(3,1,p.Row,['Region'],['OneIs',p.EQ,9])
		p.setHangingPartitionSum(4,1,p.Row,['Region'],['OneIs',p.EQ,24])
		p.setHangingPartitionSum(5,1,p.Row,['Region'],['OneIs',p.EQ,19])
		p.setHangingPartitionSum(6,1,p.Row,['Region'],['OneIs',p.EQ,8])
		p.setHangingPartitionSum(7,1,p.Row,['Region'],['OneIs',p.EQ,11])
		p.setHangingPartitionSum(8,1,p.Row,['Region'],['OneIs',p.EQ,24])
		p.setHangingPartitionSum(9,1,p.Row,['Region'],['OneIs',p.EQ,9])
		
		p.setHangingPartitionSum(1,1,p.Col,['Region'],['OneIs',p.EQ,7])
		p.setHangingPartitionSum(1,2,p.Col,['Region'],['OneIs',p.EQ,18])
		p.setHangingPartitionSum(1,3,p.Col,['Region'],['OneIs',p.EQ,21])
		p.setHangingPartitionSum(1,4,p.Col,['Region'],['OneIs',p.EQ,6])
		p.setHangingPartitionSum(1,5,p.Col,['Region'],['OneIs',p.EQ,21])
		p.setHangingPartitionSum(1,6,p.Col,['Region'],['OneIs',p.EQ,10])
		p.setHangingPartitionSum(1,7,p.Col,['Region'],['OneIs',p.EQ,12])
		p.setHangingPartitionSum(1,8,p.Col,['Region'],['OneIs',p.EQ,19])
		p.setHangingPartitionSum(1,9,p.Col,['Region'],['OneIs',p.EQ,23])
		
		p.setGivenArray([243,332,423,687,778,865])
		
		self.assertEqual(p.countSolutions(test=True),'1:751298634896374251342156987135987426487562319269431578624713895978625143513849762','Failed Easy Peasy Sudoku Advent (08) - Sum Triplets')
		
if __name__ == '__main__':
    unittest.main()