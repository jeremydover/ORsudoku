import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Parity Fun 8
	# Author: galium_odoratum
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000QX1
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,1,p.Col,35,[('AfterInstance',1,['Parity',p.EQ,1]),('BeforeInstance','last',['Parity',p.EQ,1])],[['Last']])
		p.setHangingSum(2,1,p.Row,15,[('AfterInstance',1,['Parity',p.EQ,1]),('BeforeInstance','last',['Parity',p.EQ,1])],[['Last']])
		
		p.setHangingSum(1,4,p.Col,27,[('AfterInstance',1,['Parity',p.EQ,0]),('BeforeInstance','last',['Parity',p.EQ,0])],[['Last']])
		p.setHangingSum(1,9,p.Col,39,[('AfterInstance',1,['Parity',p.EQ,0]),('BeforeInstance','last',['Parity',p.EQ,0])],[['Last']])
		p.setHangingSum(3,1,p.Row,9,[('AfterInstance',1,['Parity',p.EQ,0]),('BeforeInstance','last',['Parity',p.EQ,0])],[['Last']])
		
		for x in [(1,2,p.Col,13),(1,3,p.Col,15),(1,5,p.Col,11),(1,6,p.Col,9),(1,7,p.Col,23),(1,1,p.Row,8),(6,1,p.Row,11),(7,1,p.Row,24),(9,1,p.Row,38),(9,6,p.Col,10)]:
			switch = p.model.NewBoolVar('AmbiguityBoolean')
			p.setHangingSum(x[0],x[1],x[2],x[3],[('AfterInstance',1,['Parity',p.EQ,1]),('BeforeInstance','last',['Parity',p.EQ,1])],[['Last']],OEI=[switch])
			p.setHangingSum(x[0],x[1],x[2],x[3],[('AfterInstance',1,['Parity',p.EQ,0]),('BeforeInstance','last',['Parity',p.EQ,0])],[['Last']],OEI=[switch.Not()])
			
		self.assertEqual(p.countSolutions(test=True),'1:953178624824956137716234895438762519571489263692513748369825471287341956145697382','Failed Parity Fun 8')
		
if __name__ == '__main__':
    unittest.main()