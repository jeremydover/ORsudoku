import unittest
from squishdoku import squishdoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: The Miracle Squishdoku
	# Author: blackjackfitz
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000G2H
	# Constraints tested: setKropkiArray, setXVArray, setAntiKnight
	
	def test_puzzle(self):
		p = squishdoku(3)
		p.setAntiKnight()
		p.setKropkiArray([(1,2,p.Vert,p.White),(4,3,p.Horz,p.White),(6,1,p.Horz,p.Black),(6,6,p.Vert,p.Black)])
		p.setXVArray([(1,7,p.Vert,p.X),(3,1,p.Horz,p.X),(5,6,p.Horz,p.X),(6,5,p.Vert,p.X),(7,2,p.Horz,p.X)])
			
		self.assertEqual(p.countSolutions(test=True),'1:1432578759846282671939143257375984648267196914325','Failed The Miracle Squishdoku')
		
if __name__ == '__main__':
    unittest.main()