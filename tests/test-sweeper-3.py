import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Primesweeper: Strongbox
	# Author: grkles
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008GD
	# Constraints tested: setSweeper, setSweeperNegative, setVault, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSweeper(1,5,[('Primality',p.EQ,0)])
		for x in [(1,6),(1,8),(2,4),(3,3),(3,9),(4,8),(4,9),(5,4),(6,7),(6,8),(7,7),(9,2),(9,9)]:
			p.setSweeper(x[0],x[1])
		p.setSweeperNegative()
		
		for y in [[13,14,15,23],[18,19,29,38,39,47,48,49,56,57,65,66,67,75,76],[34,35,43,44,45,53,54,61,62,63,71,72,81]]:
			p.setVault(y)
			
		p.setGivenArray([336,778])
		
		self.assertEqual(p.countSolutions(test=True),'1:958731624123564987476928513587396142612457398349812756291643875764185239835279461','Failed Primesweeper: Strongbox')
		
if __name__ == '__main__':
    unittest.main()