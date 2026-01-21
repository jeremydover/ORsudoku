import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (424) - Oil and Water
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000NE8
	# Constraints tested: setCage, setOilAndWaterCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		y = [([12,21,22],22),([14,24],12),([15,25],11),([23,32,33,34,43],27),([27,28,38],19),([36,37,46,47],20),([39,49,59],15),([44,45,54],7),([51,61,71],14),([56,65,66],18),([63,64,73,74],26),([67,76,77,78,87],26),([72,82,83],20),([85,95],11),([86,96],9),([88,89,98],9)]
		for x in y:
			p.setCage(x[0],x[1])
			p.setParityStratifiedCage(x[0])
			
		self.assertEqual(p.countSolutions(test=True),'1:561782349792534681348619752957243168834196275216875493483927516175368924629451837','Failed Sudoku Variants Series (424) - Oil and Water')
		
if __name__ == '__main__':
    unittest.main()