import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (071) - Equal Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00028A
	# Constraints tested: setConditionalSumLine, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		for l in [[22,23,32],[15,24,25,26],[27,28,38],[42,51,52,62],[45,54,55,56,65],[48,58,59,68],[72,82,83],[84,85,86,95],[78,87,88]]:
			cage = p.model.NewIntVar(0,9*len(l),'')
			p.setConditionalSumLine(l,cage,[('Parity',p.EQ,0)],[['Last']])
			p.setConditionalSumLine(l,cage,[('Parity',p.EQ,1)],[['Last']])
	
		p.setGivenArray([115,164,196,332,368,411,439,466,647,676,695,748,775,918,945,993])
			
		self.assertEqual(p.countSolutions(test=True),'1:598134726741652389632978451159386247476295138283741695967823514315469872824517963','Failed Sudoku Variants Series (071) - Equal Sudoku')
		
if __name__ == '__main__':
    unittest.main()