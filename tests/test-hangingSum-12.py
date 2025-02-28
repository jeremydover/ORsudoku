import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Japanese Odd Sum Sudoku
	# Author: jeremydover
	# Link: https://puzzling.stackexchange.com/questions/111417/japanese-odd-sum-sudoku
	# Constraints tested: setHangingSum, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		# OK, there's a lot going on here, but it shows the power.
		
		# This first constraint determines that there is a fourth run of odd digits, since its sum is at least 1
		# Implicitly, this tells us there must be 1st, 2nd and 3rd runs as well
		p.setHangingSum(1,1,p.Col,1,[['ParityRun',('Property',p.EQ,1),4]],[['Last']],comparator=p.GE)
		
		# This second constraint shows that there is no fifth run of odd digits
		p.setHangingSum(1,1,p.Col,0,[['ParityRun',('Property',p.EQ,1),5]],[['Last']])
		
		# The second run sums to 21, implying existence of a first run.
		p.setHangingSum(1,2,p.Col,21,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		
		# This shows that there is a third run
		p.setHangingSum(1,2,p.Col,1,[['ParityRun',('Property',p.EQ,1),3]],[['Last']],comparator=p.GE)
		
		# This shows there is no fourth run.
		p.setHangingSum(1,2,p.Col,0,[['ParityRun',('Property',p.EQ,1),4]],[['Last']])
		
		# Note: we do not have to exclude the possibility of a third run, since the first two runs consume all odd digits
		p.setHangingSum(1,3,p.Col,13,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingSum(1,3,p.Col,12,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		
		# Here we get to use the 'last' selector, where we can show that the last run of odd digits sums to 9
		p.setHangingSum(1,5,p.Col,9,[['ParityRun',('Property',p.EQ,1),'Last']],[['Last']])
		
		p.setHangingSum(1,7,p.Col,17,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingSum(1,7,p.Col,8,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		p.setHangingSum(1,9,p.Col,9,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingSum(1,9,p.Col,6,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		p.setHangingSum(1,9,p.Col,10,[['ParityRun',('Property',p.EQ,1),3]],[['Last']])
		
		p.setHangingSum(3,1,p.Row,13,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingSum(3,1,p.Row,12,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		p.setHangingSum(4,1,p.Row,9,[['ParityRun',('Property',p.EQ,1),3]],[['Last']])
		p.setHangingSum(4,1,p.Row,0,[['ParityRun',('Property',p.EQ,1),4]],[['Last']])
		p.setHangingSum(5,1,p.Row,16,[['ParityRun',('Property',p.EQ,1),2]],[['Last']])
		p.setHangingSum(5,1,p.Row,1,[['ParityRun',('Property',p.EQ,1),3]],[['Last']],comparator=p.GE)
		p.setHangingSum(5,1,p.Row,0,[['ParityRun',('Property',p.EQ,1),4]],[['Last']])
		
		# We do not have to test for a second run, since the existence of a third implies it
		p.setHangingSum(6,1,p.Row,12,[['ParityRun',('Property',p.EQ,1),1]],[['Last']])
		p.setHangingSum(6,1,p.Row,1,[['ParityRun',('Property',p.EQ,1),3]],[['Last']],comparator=p.GE)
		p.setHangingSum(6,1,p.Row,0,[['ParityRun',('Property',p.EQ,1),4]],[['Last']])
		
		p.setHangingSum(8,1,p.Row,7,[['ParityRun',('Property',p.EQ,1),3]],[['Last']])
		p.setHangingSum(8,1,p.Row,1,[['ParityRun',('Property',p.EQ,1),4]],[['Last']],comparator=p.GE)
		p.setHangingSum(8,1,p.Row,0,[['ParityRun',('Property',p.EQ,1),5]],[['Last']])
		
		p.setGivenArray([154,228,284,488,544,682,822,886,952])
			
		self.assertEqual(p.countSolutions(test=True),'1:936745218785216349241938576167352984852479631394861725478693152529187463613524897','Failed Japanese Odd Sum SudokuJapanese Odd Sum Sudoku')
		
if __name__ == '__main__':
    unittest.main()