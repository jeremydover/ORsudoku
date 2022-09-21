import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: MRE Swap
	# Author: jeremydover
	# Link: https://f-puzzles.com/?id=2fskwoh6
	# Link: https://tinyurl.com/4b3c867p
	# Constraints tested: setSandwichSum, setBattlefield
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setBattlefield(1,1,p.Row,36)
		p.setSandwichSum(1,1,p.Row,0)
		p.setBattlefield(2,1,p.Row,36)
		p.setSandwichSum(2,1,p.Row,24)
		p.setSandwichSum(3,1,p.Row,5)
		p.setBattlefield(3,1,p.Row,3)
		p.setSandwichSum(4,1,p.Row,17)
		p.setBattlefield(4,1,p.Row,19)
		p.setSandwichSum(5,1,p.Row,3)
		p.setBattlefield(5,1,p.Row,3)
		p.setSandwichSum(7,1,p.Row,0)
		p.setBattlefield(7,1,p.Row,0)
		p.setSandwichSum(8,1,p.Row,14)
		p.setBattlefield(8,1,p.Row,19)
		p.setSandwichSum(1,2,p.Col,35)
		p.setBattlefield(1,2,p.Col,1)
		p.setSandwichSum(1,3,p.Col,11)
		p.setBattlefield(1,3,p.Col,11)
		p.setSandwichSum(1,4,p.Col,19)
		p.setBattlefield(1,4,p.Col,15)
		p.setSandwichSum(1,6,p.Col,14)
		p.setBattlefield(1,6,p.Col,24)
		p.setSandwichSum(1,8,p.Col,29)
		p.setBattlefield(1,8,p.Col,38)										
		
		self.assertEqual(p.findSolution(test=True),'915374628263985741478621593542716839139258467687439152354197286821563974796842315','Failed MRE Swap')
		
if __name__ == '__main__':
    unittest.main()