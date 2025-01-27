import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (338) - N-Sums Sudoku - Bigger
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0007K9
	# Constraints tested: setHangingSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setHangingSum(1,3,p.Col,29,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(1,4,p.Col,17,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(1,6,p.Col,41,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(1,8,p.Col,25,[['All']],[('Indexed',[1,2],'Largest')])
		
		p.setHangingSum(4,9,p.Row,31,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(5,9,p.Row,35,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(6,9,p.Row,45,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(7,9,p.Row,29,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(8,9,p.Row,30,[['All']],[('Indexed',[1,2],'Largest')])
		
		p.setHangingSum(9,2,p.Col,26,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(9,4,p.Col,29,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(9,6,p.Col,13,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(9,7,p.Col,21,[['All']],[('Indexed',[1,2],'Largest')])
		
		p.setHangingSum(2,1,p.Row,34,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(3,1,p.Row,11,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(4,1,p.Row,13,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(5,1,p.Row,35,[['All']],[('Indexed',[1,2],'Largest')])
		p.setHangingSum(6,1,p.Row,19,[['All']],[('Indexed',[1,2],'Largest')])
			
		self.assertEqual(p.countSolutions(test=True),'1:895467213471328956236915784328179645649853172157246839583792461964581327712634598','Failed Sudoku Variants Series (338) - N-Sums Sudoku - Bigger')
		
if __name__ == '__main__':
    unittest.main()