import unittest
from schroedingerSudoku import schroedingerCellSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: X-Sums: 37
	# Author: the_cogito
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000904
	# Constraints tested: schroedingerCellSudoku, setGivenArray, setXSum
	
	def test_puzzle(self):
		p = schroedingerCellSudoku(3)
		p.setGivenArray([454,541,565])
		p.setXSum(1,1,p.Col,7,sSum=True)
		p.setXSum(1,3,p.Col,32,sSum=True)
		p.setXSum(1,5,p.Col,31,sSum=True)
		p.setXSum(1,7,p.Col,38,sSum=True)
		p.setXSum(1,9,p.Col,5,sSum=True)
		
		p.setXSum(1,9,p.Row,12,sSum=True)
		p.setXSum(3,9,p.Row,24,sSum=True)
		p.setXSum(6,9,p.Row,37,sSum=True)
		p.setXSum(7,9,p.Row,45,sSum=True)
		p.setXSum(9,9,p.Row,37,sSum=True)
		
		p.setXSum(9,4,p.Col,0,sSum=True)
		p.setXSum(9,6,p.Col,10,sSum=True)
		
		p.setXSum(3,1,p.Row,32,sSum=True)
		p.setXSum(6,1,p.Row,37,sSum=True)
		p.setXSum(7,1,p.Row,45,sSum=True)
		p.setXSum(9,1,p.Row,37,sSum=True)
		
		self.assertEqual(p.countSolutions(test=True),'1:315970842027614953486532107563247081842105379701389426970821634138456290254093718000000060000008000090000000009000000000060000000000500000000005000700000600000000','Failed X-Sims: 37')
		
if __name__ == '__main__':
    unittest.main()
	

