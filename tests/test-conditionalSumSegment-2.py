import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Field of View
	# Author: Matt Tressel
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000R9V
	# Constraints tested: setConditionalSumSegment
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setConditionalSumSegment([22,23,24,25,26,27,28,29],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([25,24,23,22,21],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([27,28,29],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([33,32,31],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([42,52,62,72,82,92],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([45,44,43,42,41],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([48,47,46,45,44,43,42,41],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([54,53,52,51],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([56,46,36,26,16],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([65,75,85,95],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([72,62,52,42,32,22,12],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([78,68,58,48,38,28,18],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([86,76,66,56,46,36,26,16],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([88,78,68,58,48,38,28,18],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		p.setConditionalSumSegment([93,92,91],'self',['Fixed',1],[('RelatedDigit',1,p.LE,1,-1)],[('RelatedDigit',1,p.GE,1,1,1)],includeTerminator=False,backward=False,includeSelf=False,forceTermination=False,failedTerminationBehavior='partial')
		
		self.assertEqual(p.countSolutions(test=True),'1:453276189681349752279815643934182576815697324726453918568921437192734865347568291','Failed Field of View')
		
if __name__ == '__main__':
    unittest.main()