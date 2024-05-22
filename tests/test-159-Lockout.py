import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Duress Code
	# Author: Twototenth
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008RP
	# Constraints tested: setIndexColumn,setLockoutLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setIndexColumn(1)
		p.setIndexColumn(5)
		p.setIndexColumn(9)
		p.setLockoutLine([12,13,23,33,32])
		p.setLockoutLine([17,16,26])
		p.setLockoutLine([27,37,47,57,67,77])
		p.setLockoutLine([43,53,44,54])
		p.setLockoutLine([62,72,82,83,73,63])
		p.setLockoutLine([78,88,98,97])
			
		self.assertEqual(p.countSolutions(test=True),'1:457129386936478521218653947894365712562917834173284659789542163321896475645731298','Failed Duress Code')
		
if __name__ == '__main__':
    unittest.main()