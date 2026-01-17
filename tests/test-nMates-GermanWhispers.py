import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: You'll Know It When You See It
	# Author: EPH
	# Link: https://sudokupad.app/uvwqjyjjud
	# Constraints tested: setNMates, setGermanWhispers
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setNMates([(1,1,p.Down),(1,3,p.Down),(1,4,p.Left),(1,6,p.Left),(1,8,p.Down),(2,9,p.Left),(6,1,p.Up),(7,2,p.Up),(8,2,p.Up),(8,2,p.Right),(8,6,p.Up),(8,7,p.Up),(9,1,p.Up),(9,5,p.Up)])
		p.setGermanWhispersLine([11,12,13,14,15,16])
		p.setGermanWhispersLine([34,35,36,37,38,39])
		p.setGermanWhispersLine([61,62,63,64,65,66])
		p.setGermanWhispersLine([86,87,88,89])
		
		self.assertEqual(p.countSolutions(test=True),'1:728391465931654827456728391865432719174965238293817654517283946349576182682149573',"Failed You'll Know It When You See It")
		
if __name__ == '__main__':
    unittest.main()