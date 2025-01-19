import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (069) - Shaken Clones
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00027T
	# Constraints tested: setGivenArray, setShakenCloneRegion
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([114,193,255,292,381,456,479,519,545,568,594,634,657,723,812,853,911,995])
		p.setShakenCloneRegion([[13,22,23,31,32],[64,73,74,82,83]])
		p.setShakenCloneRegion([[14,15,24,34,35],[65,66,75,85,86]])
		p.setShakenCloneRegion([[16,17,26,27,36],[67,68,77,78,87]])
		p.setShakenCloneRegion([[18,28,37,38,47],[69,79,88,89,98]])
		
		self.assertEqual(p.countSolutions(test=True),'1:472891563891356472653742819517463928926518734384279651739185246265934187148627395','Failed Sudoku Variants Series (069) - Shaken Clones')
		
if __name__ == '__main__':
    unittest.main()