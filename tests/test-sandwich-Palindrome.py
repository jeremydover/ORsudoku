import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Palindromic Sandwich
	# Author: Strosahl
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0004BN
	# Constraints tested: setSandwichSum,setGiven,setPalindromeLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setSandwichSum(1,2,p.Col,31)
		p.setSandwichSum(1,4,p.Col,23)
		p.setSandwichSum(1,6,p.Col,16)
		p.setSandwichSum(1,8,p.Col,32)
		p.setSandwichSum(1,9,p.Col,26)
		p.setSandwichSum(1,1,p.Row,10)
		p.setSandwichSum(4,1,p.Row,11)
		p.setSandwichSum(6,1,p.Row,26)
		p.setSandwichSum(7,1,p.Row,8)
		p.setSandwichSum(8,1,p.Row,29)
		p.setSandwichSum(9,1,p.Row,21)
		p.setGiven(559)
		p.setPalindromeLine([16,25,34,43,32,21])
		p.setPalindromeLine([18,27,36,47,58,69])
		p.setPalindromeLine([41,52,63,74,83,92])
		p.setPalindromeLine([94,85,76,67,78,89])
				
		self.assertEqual(p.countSolutions(test=True),'1:294618537867453291351279684432165978186397425975824163729531846618742359543986712','Failed Palindromic Sandwich')

if __name__ == '__main__':  
    unittest.main()