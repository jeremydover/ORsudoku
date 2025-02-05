import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Counting Different Sudoku
	# Author: Bill Murphy
	# https://sudokupad.app/nlyj56mmlx
	# Constraints tested: setConditionalCountLine, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setConditionalCountLine([14,25,36,47,58,69],3,[('DigitInstance',p.EQ,1)],[['Last']])
		p.setConditionalCountLine([16,27,38,49],2,[('DigitInstance',p.EQ,1)],[['Last']])
		p.setConditionalCountLine([49,58,67,76,85,94],3,[('DigitInstance',p.EQ,1)],[['Last']])
		p.setConditionalCountLine([69,78,87,96],2,[('DigitInstance',p.EQ,1)],[['Last']])
		p.setConditionalCountLine([96,85,74,63,52,41],3,[('DigitInstance',p.EQ,1)],[['Last']])
		p.setConditionalCountLine([94,83,72,61],2,[('DigitInstance',p.EQ,1)],[['Last']])
		p.setConditionalCountLine([61,52,43,34,25,16],3,[('DigitInstance',p.EQ,1)],[['Last']])
		p.setConditionalCountLine([41,32,23,14],2,[('DigitInstance',p.EQ,1)],[['Last']])
		
		p.setGivenArray([116,144,168,195,319,346,365,462,496,613,641,749,767,918,945,964,992])
			
		self.assertEqual(p.countSolutions(test=True),'1:623498175587231649941675283418752396762349851359186724134927568295863417876514932','Failed Counting Different Sudoku')
		
if __name__ == '__main__':
    unittest.main()