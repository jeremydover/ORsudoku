import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Easy Peasy Sudoku Leftover (02) - Little Palindromes
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000RIV
	# Constraints tested: setPartialPalindromeLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setPartialPalindromeLine([14,23,32,41],[('Length',p.GE,3),('Sum',p.EQ,13)])
		p.setPartialPalindromeLine([15,24,33,42,51],[('Length',p.GE,3),('Sum',p.EQ,31)])
		p.setPartialPalindromeLine([49,38,27,16],[('Length',p.GE,3),('Sum',p.EQ,4)])
		p.setPartialPalindromeLine([59,48,37,26,15],[('Length',p.GE,3),('Sum',p.EQ,24)])
		p.setPartialPalindromeLine([69,58,47,36,25,14],[('Length',p.GE,3),('Sum',p.EQ,30)])
		p.setPartialPalindromeLine([79,68,57,46,35,24,13],[('Length',p.GE,3),('Sum',p.EQ,7)])
		p.setPartialPalindromeLine([96,87,78,69],[('Length',p.GE,3),('Sum',p.EQ,12)])
		p.setPartialPalindromeLine([95,86,77,68,59],[('Length',p.GE,3),('Sum',p.EQ,31)])
		p.setPartialPalindromeLine([94,85,76,67,58,49],[('Length',p.GE,3),('Sum',p.EQ,48)])
		
		self.assertEqual(p.countSolutions(test=True),'1:268941573145738269739256814572619348483572196691384752856427931324195687917863425','Failed Easy Peasy Sudoku Leftover (02) - Little Palindromes')
		
if __name__ == '__main__':
    unittest.main()