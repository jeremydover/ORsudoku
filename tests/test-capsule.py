import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Odd/Even Capsule
	# Author: Hu Meng Ting
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00047K
	# Constraints tested: setgivenArray, setCapsule
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([139,177,196,226,247,258,265,373,466,535,579,644,738,845,852,867,884,912,937,975])
		p.setCapsule([31,41])
		p.setCapsule([32,42])
		p.setCapsule([35,45])
		p.setCapsule([38,48])
		p.setCapsule([39,49])
		p.setCapsule([61,71])
		p.setCapsule([62,72])
		p.setCapsule([65,75])
		p.setCapsule([68,78])
		p.setCapsule([69,79])
			
		self.assertEqual(p.findSolution(test=True),'519234786362785491784961325491376258675812934823459167958143672136527849247698513','Failed Odd/Even Capsule')
		
if __name__ == '__main__':
    unittest.main()