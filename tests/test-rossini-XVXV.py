import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: La Scala
	# Author: Virtual & Grkles
	# Link: https://tinyurl.com/934sahx3
	# Constraints tested: setRossini, setRossiniNegative, setXVXVArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setXVXVArray([(1,2,p.Vert,p.X),(1,8,p.Vert,p.X),(2,1,p.Horz,p.X),(2,3,p.Vert,p.V),(2,7,p.Vert,p.X),(2,8,p.Horz,p.X),(3,2,p.Vert,p.V),(3,3,p.Horz,p.V),(3,6,p.Horz,p.V),(3,8,p.Vert,p.V),(5,1,p.Horz,p.X),(5,2,p.Vert,p.X),(5,4,p.Horz,p.X),(5,6,p.Horz,p.X),(5,8,p.Horz,p.X),(5,8,p.Vert,p.X),(6,3,p.Vert,p.V),(6,7,p.Vert,p.X),(7,3,p.Horz,p.X),(7,4,p.Vert,p.X),(7,6,p.Horz,p.X),(7,6,p.Vert,p.X)])
		p.setRossini(1,1,p.Down)
		p.setRossini(1,2,p.Up)
		p.setRossini(1,5,p.Down)
		p.setRossini(1,8,p.Up)
		p.setRossini(2,1,p.Right)
		p.setRossini(2,9,p.Left)
		p.setRossini(8,1,p.Left)
		p.setRossini(7,9,p.Left)
		p.setRossini(9,4,p.Up)
		p.setRossini(9,5,p.Down)
		p.setRossini(9,6,p.Up)
		p.setRossiniNegative()
		
		self.assertEqual(p.findSolution(test=True),'182647395379152864546983217713268549465379182298415673957826431621734958834591726','Failed La Scala')
		
if __name__ == '__main__':
    unittest.main()