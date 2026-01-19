import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Kroopki Dots
	# Author: Michael Lefkowitz
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000GTM
	# Constraints tested: setKroopkiArray, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setKroopkiArray([(1,3,p.Horz,p.White,p.White),(1,5,p.Vert,p.White,p.White),(2,3,p.Vert,p.Black,p.White),(2,7,p.Vert,p.White,p.Black),(3,1,p.Horz,p.Black,p.Black),(3,4,p.Horz,p.White,p.White),(3,5,p.Horz,p.White,p.White),(3,8,p.Horz,p.Black,p.Black),(4,5,p.Vert,p.White,p.Black),(5,3,p.Vert,p.White,p.Black),(5,4,p.Horz,p.Black,p.White),(5,5,p.Vert,p.White,p.Black),(6,1,p.Horz,p.Black,p.Black),(6,8,p.Horz,p.Black,p.Black),(7,1,p.Horz,p.White,p.White),(7,3,p.Horz,p.Black,p.White),(7,7,p.Vert,p.White,p.White),(7,8,p.Vert,p.White,p.White),(8,4,p.Vert,p.White,p.Black),(8,5,p.Vert,p.White,p.White),(8,8,p.Vert,p.Black,p.White),(9,2,p.Horz,p.White,p.White),(9,6,p.Horz,p.White,p.White)])
		p.setGivenArray([222,287,583,824,886])
		
		self.assertEqual(p.countSolutions(test=True),'1:756482193928163475413975682634291758179854236285637914862519347341728569597346821','Failed Kroopki Dots')
		
if __name__ == '__main__':
    unittest.main()