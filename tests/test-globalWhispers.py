import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: World Wide Whispers
	# Author: jeremydover
	# Constraints tested: setGivenArray, setGlobalWhispers
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([115,158,173,194,214,226,245,261,331,462,517,556,591,619,743,792,865,924])
		p.setGlobalWhispers()
		self.assertEqual(p.findSolution(test=True),'597286314462531879831947625385712496724869531916453287158394762673125948249678153','Failed World Wide Whispers')
		
if __name__ == '__main__':
    unittest.main()