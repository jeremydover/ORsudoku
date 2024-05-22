import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Every Third Knight
	# Author: jeremydover and Raumplaner
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00091H
	# Constraints tested: setEntropicLine, setAntiKnight
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([111,284,518,723,957,975])
		p.setEntropicLine([12,13,14,15,16,26,25,35,36,46,56])
		p.setEntropicLine([17,18,19,29,39,38,37])
		p.setEntropicLine([24,34,44,45])
		p.setEntropicLine([31,41,32,42,33,43])
		p.setEntropicLine([57,47,58,48,59,49])
		p.setEntropicLine([75,74,84,85])
		p.setAntiKnight()
		
		self.assertEqual(p.countSolutions(test=True),'1:157249386682753941943681257275394168861527493394168725539416872728935614416872539','Failed Every Third Knight')
		
if __name__ == '__main__':
    unittest.main()