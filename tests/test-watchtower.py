import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (376) - Sudoku Watchtowers
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000A3J
	# Constraints tested: setConditionalCountCross, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		myList = [(1,3),(1,4),(2,2),(2,3),(2,4),(2,6),(2,7),(2,8),(3,2),(3,4),(4,1),(4,5),(4,9),(5,5),(5,8),(6,1),(6,2),(6,4),(6,5),(6,8),(7,1),(7,5),(7,6),(7,9),(8,8),(8,9),(9,3),(9,5)]
		for x in [(i,j) for i in range(1,10) for j in range(1,10)]:
			if x in myList:
				p.setConditionalCountCross(x[0],x[1],'self',[['All']],[['RelatedDigit',1,p.GE,1,1,1]],includeTerminator=False,forceTermination=False)
			else:
				p.setConditionalCountCross(x[0],x[1],p.cellValues[x[0]-1][x[1]-1],[['All']],[['RelatedDigit',1,p.GE,1,1,1]],includeTerminator=False,forceTermination=False,comparator=p.NE)
	
		p.setGivenArray([114,199,233,287,376,479,546,563,634,737,824,877,918,992])
	
		self.assertEqual(p.countSolutions(test=True),'1:472165839653298174918437625736842951589613247124759386367521498245986713891374562','Failed Sudoku Variants Series (376) - Sudoku Watchtowers')
		
if __name__ == '__main__':
    unittest.main()