import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Parindromes
	# Author: BremSter
	# Link: https://bremster.tiny.us/parindromes
	# Constraints tested: setCage (without value),setParindromeLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCage([14,24],10)
		p.setCage([16,26],12)
		p.setCage([17,27,37,36])
		p.setCage([22,32],10)
		p.setCage([28,38,39],9)
		p.setCage([42,52,51],10)
		p.setCage([44,54,64,53],20)
		p.setCage([46,56,66,55],20)
		p.setCage([47,48],11)
		p.setCage([57,58],10)
		p.setCage([67,68],11)
		p.setCage([74,84],10)
		p.setCage([76,77,87,97])
		p.setCage([79,89,99],15)
		p.setCage([82,92],11)
		p.setCage([94,95],12)
		p.setParindromeLine([11,12,13])
		p.setParindromeLine([14,25,36])
		p.setParindromeLine([22,31,41,51,61,71])
		p.setParindromeLine([26,16,17,18,19,29])
		p.setParindromeLine([39,48])
		p.setParindromeLine([32,43,53])
		p.setParindromeLine([47,58])
		p.setParindromeLine([55,65,74])
		p.setParindromeLine([57,68])
		p.setParindromeLine([67,78,79])
		p.setParindromeLine([82,93,84])
		p.setParindromeLine([86,96,97,98,99,89])
		
		self.assertEqual(p.countSolutions(test=True),'1:935718426721364958486295713348657291512839647697421385274183569153946872869572134','Failed Parindromes')
		
if __name__ == '__main__':
    unittest.main()