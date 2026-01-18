import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (450) - Unique killer cages
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000Q40
	# Constraints tested: setCage, setDigitComparison
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCage([31,41],6)
		p.setCage([76,77],6)
		p.setDigitComparison([31,41],[76,77],p.EQ,0)
		p.setCage([33,43],8)
		p.setCage([96,97],8)
		p.setDigitComparison([33,43],[96,97],p.EQ,0)
		p.setCage([11,21],10)
		p.setCage([98,99],10)
		p.setDigitComparison([11,21],[98,99],p.EQ,0)
		p.setCage([61,71],12)
		p.setCage([93,94],12)
		p.setDigitComparison([61,71],[93,94],p.EQ,0)
		
		p.setCage([14,15,24],10)
		p.setCage([18,19,29],10)
		p.setCage([54,55,65],10)
		p.setCage([59,68,69],10)
		p.setDigitComparison([14,15,24],[18,19,29],p.LE,2)
		p.setDigitComparison([14,15,24],[54,55,65],p.LE,2)
		p.setDigitComparison([14,15,24],[59,68,69],p.LE,2)
		p.setDigitComparison([54,55,65],[18,19,29],p.LE,2)
		p.setDigitComparison([59,68,69],[18,19,29],p.LE,2)
		p.setDigitComparison([59,68,69],[54,55,65],p.LE,2)
		p.setCage([36,37,47],11)
		p.setCage([45,46,56],11)
		p.setCage([63,64,74],11)
		p.setCage([72,73,83],11)
		p.setCage([81,82,92],11)
		p.setDigitComparison([36,37,47],[45,46,56],p.LE,2)
		p.setDigitComparison([36,37,47],[63,64,74],p.LE,2)
		p.setDigitComparison([36,37,47],[72,73,83],p.LE,2)
		p.setDigitComparison([36,37,47],[81,82,92],p.LE,2)
		p.setDigitComparison([45,46,56],[63,64,74],p.LE,2)
		p.setDigitComparison([45,46,56],[72,73,83],p.LE,2)
		p.setDigitComparison([45,46,56],[81,82,92],p.LE,2)
		p.setDigitComparison([63,64,74],[72,73,83],p.LE,2)
		p.setDigitComparison([63,64,74],[81,82,92],p.LE,2)
		p.setDigitComparison([72,73,83],[81,82,92],p.LE,2)
	
		p.setCage([27,28,38],12)
		
		self.assertEqual(p.countSolutions(test=True),'1:364518927798426351125973648583761294916254873472839516837192465241685739659347182','Failed Sudoku Variants Series (450) - Unique killer cages')
		
if __name__ == '__main__':
    unittest.main()