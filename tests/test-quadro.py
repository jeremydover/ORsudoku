import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (107) - Quadro Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002CY
	# Constraints tested: setGivenArray, setQuadro
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setQuadro()
		p.setGivenArray([124,181,218,295,333,352,374,436,473,513,596,635,659,677,738,753,771,817,841,864,898,929,983])
		
		self.assertEqual(p.countSolutions(test=True),'1:247965813819473265563821479926547381374218956185396742458639127732154698691782534','Failed Sudoku Variants Series (107) - Quadro Sudoku')
		
if __name__ == '__main__':
    unittest.main()