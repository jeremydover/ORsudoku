import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: XV - XV = 0
	# Author: jeremydover
	# Link: https://tinyurl.com/3hwcdyn2
	# Constraints tested: setGivenArray, setOddEvenArray, setXVArray, setXVNegative
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCage([11,12,21,22],10)
		p.setCage([33,34,43,44],20)
		p.setCage([66,67,76,77],15)
		p.setCage([88,89,98,99],30)
		p.setCage([45,54,55,56,65],25)
		p.setCage([19,29,39],20)
		p.setCage([71,81,91],17)
		p.setXVXVArray([(4,6,p.Horz,p.X),(6,3,p.Horz,p.V),(9,3,p.Horz,p.X),(1,6,p.Horz,p.V),(4,1,p.Vert,p.X),(5,9,p.Vert,p.V),(1,6,p.Horz,p.V),(9,3,p.Horz,p.X),(3,8,p.Vert,p.X),(4,2,p.Horz,p.V),(4,7,p.Vert,p.X),(5,8,p.Vert,p.X),(5,3,p.Vert,p.X),(5,7,p.Horz,p.X)])
		p.setXVXVNegative()
		
		self.assertEqual(p.countSolutions(test=True),'1:136247859245986317798513624623479185471358962859621743984762531567134298312895476','Failed XV - XV = 0')
		
if __name__ == '__main__':
    unittest.main()