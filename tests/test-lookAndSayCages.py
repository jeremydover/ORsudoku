import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Look-and-Say Killer 3
	# Author: djorr
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000AG9
	# Constraints tested: setLookAndSayCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setLookAndSayCage([11,22,33,44,55,66,77,88,99],"23")
		p.setLookAndSayCage([13,24,35,46,57,68,79],"38")
		p.setLookAndSayCage([13,22,31],"12")
		p.setLookAndSayCage([16,25,34,43,52,61],"24")
		p.setLookAndSayCage([19,28,37,46,55,64,73,82,91],"24")
		p.setLookAndSayCage([21,32,43,54,65,76,87,98],"37")
		p.setLookAndSayCage([31,42,53,64,75,86,97],"14")
		p.setLookAndSayCage([41,52,63,74,85,96],"27")
		p.setLookAndSayCage([51,62,73,84,95],"15")
		p.setLookAndSayCage([49,58,67,76,85,94],"25")
		p.setLookAndSayCage([59,68,77,86,95],"15")
		p.setLookAndSayCage([14,15,25],"12")
		p.setLookAndSayCage([17,18,19,29],"12")
		p.setLookAndSayCage([21,22,31],"13")
		p.setLookAndSayCage([26,36],"13")
		p.setLookAndSayCage([33,34,43],"26")
		p.setLookAndSayCage([45,54,55],"14")
		p.setLookAndSayCage([47,48,49,59],"14")
		p.setLookAndSayCage([57,67],"11")
		p.setLookAndSayCage([61,62],"11")
		p.setLookAndSayCage([68,69],"12")
		p.setLookAndSayCage([71,81,91],"17")
		p.setLookAndSayCage([73,83],"15")
		p.setLookAndSayCage([76,86],"16")
		p.setLookAndSayCage([78,79],"16")
		p.setLookAndSayCage([84,94,95],"14")
		p.setLookAndSayCage([89,98,99],"12")
			
		self.assertEqual(p.countSolutions(test=True),'1:658194237349827651271653894926318745583742169417965328794231586835476912162589473','Failed Look-and-Say Killer 3')
		
if __name__ == '__main__':
    unittest.main()