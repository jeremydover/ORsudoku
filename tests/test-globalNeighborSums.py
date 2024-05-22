import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Pair-Up Sudoku
	# Author: clover!
	# Link: https://discord.com/channels/709370620642852885/875124233846554694/1192089047288516608
	# Constraints tested: setGivenArray, setGlobalNeighborSum
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGlobalNeighborSum(sums=[5,10],exceptions=[5])
		p.setGivenArray([118,149,165,216,317,361,398,459,493,511,547,566,592,614,658,719,742,796,897,945,968,999])
		
		self.assertEqual(p.countSolutions(test=True),'1:821935764649827351735461928582194673193756482467382195918273546254619837376548219','Failed Pair-Up Sudoku')
		
if __name__ == '__main__':
    unittest.main()