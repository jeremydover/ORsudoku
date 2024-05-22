import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Gallery
	# Author: BremSter & Maggie
	# Link: https://link.sudokupad.app/polar-gallery
	# Constraints tested: setEvenOddArray, setOutside
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setOddEvenArray([151,220,260,281,331,341,431,480,511,551,591,620,671,761,771,821,840,880,951])
		p.setOutside(1,2,p.Col,[3,9])
		p.setOutside(1,5,p.Col,[7,8])
		p.setOutside(1,6,p.Col,[4])
		p.setOutside(1,8,p.Col,[2,6])
		p.setOutside(2,1,p.Row,[1,5])
		p.setOutside(2,9,p.Row,[4,8])
		p.setOutside(4,1,p.Row,[4])
		p.setOutside(5,1,p.Row,[1,2])
		p.setOutside(5,9,p.Row,[5])
		p.setOutside(6,9,p.Row,[7])
		p.setOutside(8,1,p.Row,[2,8])
		p.setOutside(8,9,p.Row,[1,3])
		p.setOutside(9,2,p.Col,[4,6])
		p.setOutside(9,4,p.Col,[3])
		p.setOutside(9,5,p.Col,[9])
		p.setOutside(9,8,p.Col,[5,7])
		
		self.assertEqual(p.countSolutions(test=True),'1:894253167521976438637184529459761283712438695386529714163847952278695341945312876','Failed Gallery')
		
if __name__ == '__main__':
    unittest.main()