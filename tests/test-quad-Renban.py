import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Truth or Consequads
	# Author: Twototenth
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000A7G
	# Constraints tested: setRenbanLine,setQuadrupleArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setRenbanLine([11,12,13])
		p.setRenbanLine([16,25,35])
		p.setRenbanLine([17,28])
		p.setRenbanLine([19,29])
		p.setRenbanLine([21,31])
		p.setRenbanLine([34,45])
		p.setRenbanLine([41,52])
		p.setRenbanLine([43,53,63])
		p.setRenbanLine([46,57,67])
		p.setRenbanLine([54,64])
		p.setRenbanLine([61,62])
		p.setRenbanLine([72,73])
		p.setRenbanLine([74,75,76])
		p.setRenbanLine([77,68,79])
		p.setRenbanLine([85,96,87])
		p.setQuadrupleArray([2227,2636,4846,5535,8158,8337,881])
			
		self.assertEqual(p.findSolution(test=True),'345971286926438517871526349269847153137295864458163972712354698594682731683719425','Failed Truth or Consequads')
		
if __name__ == '__main__':
    unittest.main()