import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Rockin' into the Night
	# Author: riffclown
	# Link: https://f-puzzles.com/?id=y5yjmbam
	# Constraints tested: setIndexColumn, setGammaEpsilon, setKropkiWhiteArray, setKropkiBlackArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setIndexColumn(1,True,[4,6])
		p.setIndexColumn(5,True,[2,4,6,9])
		p.setIndexColumn(9,True,[2,6,9])
		p.setGammaEpsilon()
		p.setKropkiWhiteArray([210,260,441,520,751,920])
		p.setKropkiBlackArray([171,251,281,620,660,661,731,861,870])
		
		self.assertEqual(p.findSolution(test=True),'384925671615437298972618435197254863538769124426183957243591786759846312861372549','Rockin into the Night')
		
if __name__ == '__main__':
    unittest.main()