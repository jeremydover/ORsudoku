import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Dustpan (Disjoint parity sweeper sudoku)
	# Author: Qodec
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000D2H
	# Constraints tested: setSweeper, setDisjointGroups, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSweeper(1,1,[('MatchParity',1)])
		p.setSweeper(1,4,[('MatchParity',1)])
		p.setSweeper(1,7,[('MatchParity',1)])
		p.setSweeper(2,2,[('MatchParity',1)])
		p.setSweeper(4,1,[('MatchParity',1)])
		p.setSweeper(4,4,[('MatchParity',1)])
		p.setSweeper(4,7,[('MatchParity',1)])
		p.setSweeper(5,5,[('MatchParity',1)])
		p.setSweeper(7,1,[('MatchParity',1)])
		p.setSweeper(7,4,[('MatchParity',1)])
		p.setSweeper(7,7,[('MatchParity',1)])
		
		p.setDisjointGroups()
		p.setGivenArray([176,517])
		
		self.assertEqual(p.countSolutions(test=True),'1:378592641651374829924681375215867934796243518843159762189726453462935187537418296','Failed Dustpan (Disjoint parity sweeper sudoku)')
		
if __name__ == '__main__':
    unittest.main()