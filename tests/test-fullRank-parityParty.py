import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: I don't see how that's a party
	# Author: AnalyticalNinja
	# Link: https://sudokupad.app/30wgwii3si
	# Constraints tested: setGivenArray, setParityParty, setFullRank
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([123,674])
		p.setFullRank(1,7,p.Col,1)
		p.setFullRank(9,4,p.Col,15)
		p.setFullRank(2,1,p.Row,33)
		p.setFullRank(5,1,p.Row,29)
		p.setFullRank(6,1,p.Row,25)
		p.setFullRank(3,9,p.Row,17)
		p.setFullRank(7,9,p.Row,5)
		p.setParityParty(1,7,p.Col,1)
		p.setParityParty(9,4,p.Col,15)
		p.setParityParty(2,1,p.Row,33)
		p.setParityParty(5,1,p.Row,29)
		p.setParityParty(6,1,p.Row,25)
		p.setParityParty(3,9,p.Row,17)
		p.setParityParty(7,9,p.Row,5)
		
		self.assertEqual(p.countSolutions(test=True),'1:432765189957318246168942375325174698846293751719856423674581932593627814281439567','Failed I don\'t see how that\'s a party')
		
if __name__ == '__main__':
    unittest.main()