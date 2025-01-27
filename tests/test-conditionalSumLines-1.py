import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (342) - Little Parity Killer Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0007X4
	# Constraints tested: setConditionalSumLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setConditionalSumLine([12,21],6,[['Uniparity']],[('Fixed',2)])
		p.setConditionalSumLine([13,22,31],10,[['Uniparity']],[('Fixed',3)])
		p.setConditionalSumLine([18,27,36,45,54,63,72,81],33,[['Uniparity']],[('Fixed',8)])
		p.setConditionalSumLine([29,18],9,[['Uniparity']],[('Fixed',2)])
		p.setConditionalSumLine([39,28,17],9,[['Uniparity']],[('Fixed',3)])
		p.setConditionalSumLine([49,38,27,16],19,[['Uniparity']],[('Fixed',4)])
		p.setConditionalSumLine([69,58,47,36,25,14],22,[['Uniparity']],[('Fixed',6)])
		p.setConditionalSumLine([98,89],8,[['Uniparity']],[('Fixed',2)])
		p.setConditionalSumLine([97,88,79],6,[['Uniparity']],[('Fixed',3)])
		p.setConditionalSumLine([92,83,74,65,56,47,38,29],60,[['Uniparity']],[('Fixed',8)])
		p.setConditionalSumLine([81,92],3,[['Uniparity']],[('Fixed',2)])
		p.setConditionalSumLine([71,82,93],5,[['Uniparity']],[('Fixed',3)])
		p.setConditionalSumLine([61,72,83,94],14,[['Uniparity']],[('Fixed',4)])
		p.setConditionalSumLine([41,52,63,74,85,96],26,[['Uniparity']],[('Fixed',6)])
		
		self.assertEqual(p.countSolutions(test=True),'1:962137584781542639345689271213478965894365127657291843578923416429716358136854792','Failed Sudoku Variants Series (342) - Little Parity Killer Sudoku')
		
if __name__ == '__main__':
    unittest.main()