import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Negative Romans are Oddly Even
	# Author: MavericksJD
	# Link: https://link.sudokupad.app/polar-negromansareoddlyeven
	# Constraints tested: setGivenArray, setOddEvenArray, setXVArray, setXVNegative
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([184,193,215,357,539,573,755,896,919,926])
		p.setOddEvenArray([221,281,330,370,551,730,770,821,881])
		p.setXVArray([(2,3,p.Horz,p.X),(3,6,p.Vert,p.X),(4,6,p.Horz,p.X),(6,3,p.Horz,p.X),(6,4,p.Vert,p.X),(8,6,p.Horz,p.X)])
		p.setXVNegative()
		
		self.assertEqual(p.countSolutions(test=True),'1:781526943592843671634971258357269184849715362126438597218657439475392816963184725','Failed Negative Romans are Oddly Even')
		
if __name__ == '__main__':
    unittest.main()