import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (174) - Japanese Even-Odd Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002KS
	# Constraints tested: setHangingCount, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingCount(1,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),1]],[['Last']])
		p.setHangingCount(1,1,p.Row,2,[['ParityRun',('Property',p.EQ,0),2]],[['Last']])
		p.setHangingCount(1,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),3]],[['Last']])
		p.setHangingCount(2,1,p.Row,2,[['ParityRun',('Property',p.EQ,0),1]],[['Last']])
		p.setHangingCount(2,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),2]],[['Last']])
		p.setHangingCount(2,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),3]],[['Last']])
		p.setHangingCount(4,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),1]],[['Last']])
		p.setHangingCount(4,1,p.Row,2,[['ParityRun',('Property',p.EQ,0),2]],[['Last']])
		p.setHangingCount(4,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),3]],[['Last']])
		p.setHangingCount(6,1,p.Row,2,[['ParityRun',('Property',p.EQ,0),1]],[['Last']])
		p.setHangingCount(6,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),2]],[['Last']])
		p.setHangingCount(6,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),3]],[['Last']])
		p.setHangingCount(8,1,p.Row,2,[['ParityRun',('Property',p.EQ,0),1]],[['Last']])
		p.setHangingCount(8,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),2]],[['Last']])
		p.setHangingCount(8,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),3]],[['Last']])
		p.setHangingCount(9,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),1]],[['Last']])
		p.setHangingCount(9,1,p.Row,1,[['ParityRun',('Property',p.EQ,0),2]],[['Last']])
		p.setHangingCount(9,1,p.Row,2,[['ParityRun',('Property',p.EQ,0),3]],[['Last']])
		
		p.setHangingCount(1,1,p.Col,3,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingCount(1,1,p.Col,2,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		p.setHangingCount(1,3,p.Col,2,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingCount(1,3,p.Col,1,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		p.setHangingCount(1,3,p.Col,2,[['ParityRun',('Property',p.EQ,1),3]],[['Last']])
		p.setHangingCount(1,4,p.Col,1,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingCount(1,4,p.Col,1,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		p.setHangingCount(1,4,p.Col,2,[['ParityRun',('Property',p.EQ,1),3]],[['Last']])
		p.setHangingCount(1,4,p.Col,1,[['ParityRun',('Property',p.EQ,1),4]],[['Last']])
		p.setHangingCount(1,6,p.Col,2,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingCount(1,6,p.Col,2,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		p.setHangingCount(1,6,p.Col,1,[['ParityRun',('Property',p.EQ,1),3]],[['Last']])
		p.setHangingCount(1,7,p.Col,2,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingCount(1,7,p.Col,1,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		p.setHangingCount(1,7,p.Col,1,[['ParityRun',('Property',p.EQ,1),3]],[['Last']])
		p.setHangingCount(1,7,p.Col,1,[['ParityRun',('Property',p.EQ,1),4]],[['Last']])
		p.setHangingCount(1,9,p.Col,1,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingCount(1,9,p.Col,1,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		p.setHangingCount(1,9,p.Col,3,[['ParityRun',('Property',p.EQ,1),3]],[['Last']])
	
		p.setGivenArray([133,147,392,435,448,494,557,614,661,673,711,963,972])
			
		self.assertEqual(p.countSolutions(test=True),'1:653742918241698537798135642325869174916374825487521396169287453532416789874953261','Failed Sudoku Variants Series (174) - Japanese Even-Odd Sudoku')
		
if __name__ == '__main__':
    unittest.main()