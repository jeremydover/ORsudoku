import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Oceans Rise, Empires Fall
	# Author: BremSter
	# Link: https://bremster.tiny.us/oceansrise
	# Constraints tested: setThermo, setKropkiArray, setXVArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setThermo([31,32])
		p.setThermo([32,42,52])
		p.setThermo([82,72,62])
		p.setThermo([73,63,53,43,33])
		p.setThermo([34,44,54,64,74])
		p.setThermo([35,25,15])
		p.setThermo([65,55,45])
		p.setThermo([95,85,75])
		p.setThermo([76,66,56,46,36])
		p.setThermo([37,47,57,67,77])
		p.setThermo([58,48,38])
		p.setThermo([68,78,88])
		p.setThermo([29,39])
		p.setKropkiArray([(2,3,p.Horz,p.White),(2,6,p.Horz,p.Black),(3,1,p.Horz,p.White),(3,8,p.Horz,p.White),(4,3,p.Horz,p.Black),(4,6,p.Horz,p.Black),(5,2,p.Horz,p.Black),(5,2,p.Vert,p.White),(5,3,p.Horz,p.White),(5,6,p.Horz,p.White),(5,7,p.Horz,p.Black),(5,8,p.Vert,p.White),(6,3,p.Horz,p.Black),(6,6,p.Horz,p.Black)])
		p.setXVArray([(3,3,p.Horz,p.X),(3,6,p.Horz,p.X),(7,3,p.Horz,p.X),(7,6,p.Horz,p.X)])
		
		self.assertEqual(p.countSolutions(test=True),'1:627183594915476382348259176276398451184527639593614827752861943831942765469735218','Failed Oceans Rise, Empires Fall')
		
if __name__ == '__main__':
    unittest.main()