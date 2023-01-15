import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Psycho Killer 02
	# Author: Bremster
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0006TI
	# Constraints tested: setPsychoKillerCage, setCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setPsychoKillerCage([11],9)
		p.setPsychoKillerCage([19,29,39],3)
		p.setPsychoKillerCage([25,35],10)
		p.setPsychoKillerCage([38,47,48],24)
		p.setPsychoKillerCage([44,45,46],24)
		p.setPsychoKillerCage([79,89],9)
	
		p.setCage([12,21,22],10)
		p.setCage([32,33],9)
		p.setCage([15,16,17,18],12)
		p.setCage([41,42,43],24)
		p.setCage([54,63,64],17)
		p.setCage([55,65,75],11)
		p.setCage([57,58,67],18)
		p.setCage([59,68,69],12)
		p.setCage([74,84,94],9)
		p.setCage([85,95],15)
		p.setCage([86,87],12)
		
		self.assertEqual(p.findSolution(test=True),'475862139219735684836491572987213465341657298562948713758326941624189357193574826','Failed Psycho Killer 02')
		
if __name__ == '__main__':
    unittest.main()