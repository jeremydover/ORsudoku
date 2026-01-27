import unittest
from ORsudoku import sudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Outside Dominos
	# Author: palpot
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000MAS
	# Constraints tested: setXSum (variable exterior clues), setKropkiArray, setXVArray
	
	def test_puzzle(self):
		p = sudoku(3)
		p.setXSum(1,1,p.Col,'')
		p.setXSum(1,2,p.Col,'')
		p.setXSum(1,5,p.Col,'')
		p.setXSum(1,6,p.Col,'')
		p.setXSum(1,7,p.Col,'')
		p.setXSum(1,9,p.Row,'')
		p.setXSum(2,9,p.Row,'')
		p.setXSum(3,9,p.Row,'')
		p.setXSum(4,9,p.Row,'')
		p.setXSum(5,9,p.Row,'')
		p.setXSum(6,9,p.Row,'')
		p.setXSum(7,9,p.Row,'')
		p.setXSum(8,9,p.Row,'')
		p.setXSum(9,2,p.Col,'')
		p.setXSum(9,3,p.Col,'')
		p.setXSum(9,5,p.Col,'')
		p.setXSum(9,6,p.Col,'')
		p.setXSum(9,7,p.Col,'')
		p.setXSum(9,8,p.Col,'')
		p.setKropkiArray([(0,1,p.Horz,p.White),(0,5,p.Horz,p.Black),(0,6,p.Horz,p.White),(2,10,p.Vert,p.Black),(3,10,p.Vert,p.White),(4,10,p.Vert,p.White),(5,10,p.Vert,p.White),(6,10,p.Vert,p.Black),(7,10,p.Vert,p.White),(10,2,p.Horz,p.White),(10,5,p.Horz,p.Black),(1,3,p.Vert,p.White),(7,5,p.Horz,p.Black)])
		p.setXVArray([(1,10,p.Vert,p.X),(3,6,p.Horz,p.V),(4,8,p.Vert,p.X),(10,7,p.Horz,p.X)])
			
		self.assertEqual(p.countSolutions(test=True),'1:762954381541368972398721465154682793623597814987413256219836547435179628876245139','Failed Outside Dominos')
		
if __name__ == '__main__':
    unittest.main()