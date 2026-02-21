import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (459) - Distance Sums
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000RBO
	# Constraints tested: setConditionalSumSegment, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setConditionalSumSegment([99,88,77,66,55,44,33,22,11,12,13,14,15,16,17,18,19],'self',['Fixed',9],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([91,82,73,64,55,46,37,28,19,29,39,49,59,69,79,89,99],'self',['Fixed',9],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([71,62,53,44,35,26,36,46,56,66,76,86,96],'self',['Fixed',6],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([31,32,33,34,35,36,37,38,47,56,65,74,83,92],'self',['Fixed',8],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([15,25,35,45,46,47,48,49],'self',['Fixed',4],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([16,27,38,49,58,67,76,85,94],'self',['Fixed',4],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([95,85,75,65,55,66,77,88,99],'self',['Fixed',5],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([16,25,34,43,52,61,62,63,64,65,66,67,68,69],'self',['Fixed',6],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([31,42,53,64,75,86,85,84,83,82,81],'self',['Fixed',6],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([11,22,33,44,55,66,77,88,78,68,58,48,38,28,18],'self',['Fixed',8],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([81,82,83,84,85,86,87,88,89,79,69,59,49,39,29,19],'self',['Fixed',9],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([11,21,31,41,51,61,71,81,91,92,93,94,95,96,97,98,99],'self',['Fixed',9],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setConditionalSumSegment([31,42,53,64,75,86,97,87,77,67,57,47,37,27,17],'self',['Fixed',7],[('Location','Distance',1)],[['Last']],includeSelf=False)
		p.setGivenArray([468,649])
		
		self.assertEqual(p.countSolutions(test=True),'1:679352418385714692421689357947528163263147985518963724856471239134295876792836541','Failed Sudoku Variants Series (459) - Distance Sums')
		
if __name__ == '__main__':
    unittest.main()