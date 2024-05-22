import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Somewhat
	# Author: zetamath
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000CT0
	# Constraints tested: setPuncturedCage,setGiven
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setPuncturedCage([11,12,13],5)
		p.setPuncturedCage([21,22,31],6)
		p.setPuncturedCage([23,24,33],5)
		p.setPuncturedCage([15,25,26],8)
		p.setPuncturedCage([17,18,19],11)
		p.setPuncturedCage([27,37,47],5)
		p.setPuncturedCage([28,29,39],8)
		p.setPuncturedCage([34,44,54],12)
		p.setPuncturedCage([35,45,55],6)
		p.setPuncturedCage([36,46,56],10)
		p.setPuncturedCage([38,48,49],5)
		p.setPuncturedCage([41,42,43],7)
		p.setPuncturedCage([51,61,62],8)
		p.setPuncturedCage([52,53,63],10)
		p.setPuncturedCage([57,67,68],9)
		p.setPuncturedCage([58,59,69],11)
		p.setPuncturedCage([64,65,66,74],10)
		p.setPuncturedCage([71,72,81],10)
		p.setPuncturedCage([73,83,93],7)
		p.setPuncturedCage([75,76,77],8)
		p.setPuncturedCage([78,79,88],8)
		p.setPuncturedCage([82,91,92],10)
		p.setPuncturedCage([94,95,96],6)
		p.setPuncturedCage([87,97,98],11)
		p.setGiven(538)
			
		self.assertEqual(p.countSolutions(test=True),'1:923865174584172693167349285259687341348921756716453928491238567635794812872516439','Failed Somewhat')
		
if __name__ == '__main__':
    unittest.main()