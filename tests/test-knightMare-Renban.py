import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Something Amiss (Knightmare)
	# Author: Riffclown
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000CHZ
	# Constraints tested: setKnightMare,setRenbanLine,setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setKnightMare()
		p.setRenbanLine([22,33,43,52,61])
		p.setRenbanLine([25,36,37,28])
		p.setRenbanLine([35,45,55])
		p.setRenbanLine([38,47,56,65,74])
		p.setRenbanLine([92,83,84,95])
		p.setGivenArray([116,174,246,343,399,515,637,666,685,825,861,884,948,962])
		
		self.assertEqual(p.findSolution(test=True),'631298475942657138785314269813425796564739821297186354126543987358971642479862513','Failed Something Amiss (Knightmare)')
		
if __name__ == '__main__':
    unittest.main()