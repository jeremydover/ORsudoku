import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (122) - Point to Next
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002ED
	# Constraints tested: setConditionalInstanceLine, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		# OK, this one takes some explaining. The constraint, as written, is that each arrow points to a cell
		# whose value is one greater than the cell with the arrow. To model the arrows, we just create a list
		# of all the cells pointed to. In using the conditional instance line, we are not actually interested in
		# whether any particular value shows up before the end of the line; hence the value arrays are empty.
		# Rather what we are concerned with is "does the line terminate?", i.e., does the N+1 digit actually
		# occur on the line. If it does not, then no terminator Booleans can be true, and the model fails. If
		# it does, then the line does terminate, and we do a null check for values in the line, which trivially
		# passes. 
		
		p.setConditionalInstanceLine([33,32,31],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([34,24,14],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([35,25,15],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([36,26,16],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([37,27,17],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([43,42,41],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([45,55,65,75,85,95],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([47,48,49],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([53,52,51],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([54,55,56,57,58,59],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([56,55,54,53,52,51],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([57,58,59],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([63,62,61],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([65,55,45,35,25,15],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([67,68,69],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([73,83,93],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([74,84,94],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([75,85,95],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([76,86,96],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		p.setConditionalInstanceLine([77,78,79],[],[['All']],[('RelatedDigit',1,p.EQ,1,1,1)])
		
		p.setGivenArray([114,176,192,228,262,283,442,463,487,627,645,666,826,847,881,917,934,995])
		
		self.assertEqual(p.countSolutions(test=True),'1:437159682586472931291368547645213879312897456978546123153624798869735214724981365','Failed Sudoku Variants Series (122) - Point to Next')
		
if __name__ == '__main__':
    unittest.main()