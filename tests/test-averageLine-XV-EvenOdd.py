import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Parallel Average Lines
	# Author: Nai Night
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000BUY
	# Constraints tested: setAverageLine, setXVArray, setGivenArray, setEvenOddArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setAverageLine([15,14,16])
		p.setAverageLine([25,24,26])
		p.setAverageLine([35,34,36])
		p.setAverageLine([31,21,41])
		p.setAverageLine([32,22,42])
		p.setAverageLine([33,23,43])
		p.setAverageLine([38,28,48])
		p.setAverageLine([39,29,49])
		p.setAverageLine([61,52,71])
		p.setAverageLine([68,58,78])
		p.setAverageLine([69,59,79])
		p.setAverageLine([75,74,76])
		p.setAverageLine([85,84,86])
		p.setAverageLine([95,94,96])
		p.setAverageLine([99,89,98])
		p.setXVArray([(1,4,p.Vert,p.V),(8,6,p.Vert,p.X)])
		p.setGivenArray([476,639])
		p.setEvenOddArray([(5,4,p.Odd),(6,7,p.Even),(7,7,p.Even),(9,1,p.Odd)])
		
		self.assertEqual(p.countSolutions(test=True),'1:587123946192468537463975128734852619816394275259617483375246891641789352928531764','Failed Parallel Average Lines')
		
if __name__ == '__main__':
    unittest.main()