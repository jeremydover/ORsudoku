import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Grey Kropki
	# Author: Scruffamudda
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000DO3
	# Constraints tested: setKropkiGrayArray, setKropkiNegative
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setKropkiGrayArray([110,120,121,130,210,220,221,241,281,310,410,440,480,510,530,550,571,640,660,680,681,731,770,791,810,811,830,831,840,871,910])
		p.setKropkiNegative()
		
		self.assertEqual(p.countSolutions(test=True),'1:987641352245973186631825974458369721126587493379214865514796238762438519893152647','Failed Grey Kropki')
		
if __name__ == '__main__':
    unittest.main()