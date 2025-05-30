import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (160) - Exclusion Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002J0
	# Constraints tested: setZone, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setZone([14,15,24,25],[],[8])
		p.setZone([18,19,28,29],[],[8])
		p.setZone([23,24,33,34],[],[5])
		p.setZone([27,28,37,38],[],[7])
		p.setZone([32,33,42,43],[],[3])
		p.setZone([36,37,46,47],[],[6])
		p.setZone([41,42,51,52],[],[2])
		p.setZone([45,46,55,56],[],[5])
		p.setZone([54,55,64,65],[],[4])
		p.setZone([58,59,68,69],[],[8])
		p.setZone([63,64,73,74],[],[3])
		p.setZone([67,68,77,78],[],[5])
		p.setZone([72,73,82,83],[],[2])
		p.setZone([76,77,86,87],[],[3])
		p.setZone([81,82,91,92],[],[1])
		p.setZone([85,86,95,96],[],[2])
		
		p.setGivenArray([129,192,216,262,334,353,449,482,495,538,576,627,751,847,886,919,946])
		
		self.assertEqual(p.countSolutions(test=True),'1:193568742687492153524137986316974825458321697279856314765219438831745269942683571','Failed Sudoku Variants Series (160) - Exclusion Sudoku')
		
if __name__ == '__main__':
    unittest.main()