import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (199) - Neighbours Sudoku
	# Author: Richard Stolk
	# https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002OZ
	# Constraints tested: setInOrder, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setInOrder(1,1,p.Col,[6,4],adjacent=True)
		p.setInOrder(1,2,p.Col,[2,8],adjacent=True)
		p.setInOrder(1,3,p.Col,[1,9],adjacent=True)
		p.setInOrder(1,4,p.Col,[6,4],adjacent=True)
		p.setInOrder(1,5,p.Col,[3,7],adjacent=True)
		p.setInOrder(1,6,p.Col,[1,9],adjacent=True)
		p.setInOrder(1,7,p.Col,[2,8],adjacent=True)
		p.setInOrder(1,8,p.Col,[1,9],adjacent=True)
		p.setInOrder(1,9,p.Col,[7,3],adjacent=True)
		
		p.setInOrder(1,1,p.Row,[1,2],adjacent=True)
		p.setInOrder(2,1,p.Row,[3,4],adjacent=True)
		p.setInOrder(3,1,p.Row,[5,6],adjacent=True)
		p.setInOrder(4,1,p.Row,[7,8],adjacent=True)
		p.setInOrder(5,1,p.Row,[9,1],adjacent=True)
		p.setInOrder(6,1,p.Row,[2,3],adjacent=True)
		p.setInOrder(7,1,p.Row,[4,5],adjacent=True)
		p.setInOrder(8,1,p.Row,[6,7],adjacent=True)
		p.setInOrder(9,1,p.Row,[8,9],adjacent=True)
	
		p.setGivenArray([115,136,267,312,441,592,624,951])
		
		self.assertEqual(p.countSolutions(test=True),'1:576384129134297685298561734362149578917856342845723961621938457489675213753412896','Failed Sudoku Variants Series (199) - Neighbours Sudoku')
		
if __name__ == '__main__':
    unittest.main()