import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Classic Kropki Sudoku
	# Author: justnow
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00050K
	# Constraints tested: setKropkiArray,setKropkiNegative,setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setKropkiArray([1700,2401,3501,3511,4910,5101,6501,7210,7411,7700,8400,8811,9800])
		p.setKropkiNegative()
		p.setGivenArray([441,792,944])
				
		self.assertEqual(p.findSolution(test=True),'746915328318247596952863741685139274427586913193724685869371452274658139531492867','Failed Classic Kropki Sudoku')

if __name__ == '__main__':  
    unittest.main()