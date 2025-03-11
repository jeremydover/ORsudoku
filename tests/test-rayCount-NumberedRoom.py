import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Numbered Sandwich Counts
	# Author: RockyRoer
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000AOH
	# Constraints tested: setNumberedRoom, setRayCount
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setNumberedRoom(1,1,p.Row,5)
		p.setRayCount(1,1,p.Row,5,('DigitReached',1),[['All']],[('DigitReached',9)],includeTerminator=False,forceTermination=False,failedTerminationBehavior='zero',includeSelf=False)
		p.setNumberedRoom(1,9,p.Col,6)
		p.setRayCount(1,9,p.Col,6,('DigitReached',1),[['All']],[('DigitReached',9)],includeTerminator=False,forceTermination=False,failedTerminationBehavior='zero',includeSelf=False)
		
		for x in [(1,1,p.Col),(1,2,p.Col),(1,3,p.Col),(1,6,p.Col),(1,8,p.Col),(1,9,p.Row),(7,9,p.Row),(9,9,p.Row),(9,6,p.Col),(9,1,p.Col),(7,1,p.Row),(5,1,p.Row),(4,1,p.Row),(3,1,p.Row),(2,1,p.Row)]:
			var = p.model.NewIntVar(1,9,'')
			p.setNumberedRoom(x[0],x[1],x[2],var)
			p.setRayCount(x[0],x[1],x[2],var,('DigitReached',1),[['All']],[('DigitReached',9)],includeTerminator=False,forceTermination=False,failedTerminationBehavior='zero',includeSelf=False)
		
		self.assertEqual(p.countSolutions(test=True),'1:716824593823965741594731286451382967938647125672159834249573618165498372387216459','Failed Numbered Sandwich Counts')
		
if __name__ == '__main__':
    unittest.main()