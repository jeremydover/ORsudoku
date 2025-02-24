import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (293) - Sudoku Switch
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0004NM
	# Constraints tested: setHangingCount, setCage
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setCage([13,14,23,24],21)
		p.setCage([16,17,26,27],17)
		p.setCage([31,32,41,42],13)
		p.setCage([33,34,43,44],28)
		p.setCage([36,37,46,47],29)
		p.setCage([38,39,48,49],16)
		p.setCage([53,54,63,64],18)
		p.setCage([56,57,66,67],13)
		p.setCage([61,62,71,72],23)
		p.setCage([68,69,78,79],20)
		p.setCage([73,74,83,84],15)
		p.setCage([76,77,86,87],23)
		
		p.setHangingCount(1,1,p.Col,1,[('ParityChange','before')],[['Last']])
		p.setHangingCount(1,2,p.Col,5,[('ParityChange','before')],[['Last']])
		p.setHangingCount(1,3,p.Col,5,[('ParityChange','before')],[['Last']])
		p.setHangingCount(1,4,p.Col,6,[('ParityChange','before')],[['Last']])
		p.setHangingCount(1,6,p.Col,2,[('ParityChange','before')],[['Last']])
		p.setHangingCount(1,7,p.Col,7,[('ParityChange','before')],[['Last']])
		p.setHangingCount(1,8,p.Col,6,[('ParityChange','before')],[['Last']])
		p.setHangingCount(1,9,p.Col,6,[('ParityChange','before')],[['Last']])
		
		p.setHangingCount(1,1,p.Row,6,[('ParityChange','before')],[['Last']])
		p.setHangingCount(3,1,p.Row,7,[('ParityChange','before')],[['Last']])
		p.setHangingCount(4,1,p.Row,2,[('ParityChange','before')],[['Last']])
		p.setHangingCount(6,1,p.Row,3,[('ParityChange','before')],[['Last']])
		p.setHangingCount(7,1,p.Row,6,[('ParityChange','before')],[['Last']])
		p.setHangingCount(9,1,p.Row,5,[('ParityChange','before')],[['Last']])
			
		self.assertEqual(p.countSolutions(test=True),'1:874192356639754821215638947468917532521863479397245168742389615956421783183576294','Failed Sudoku Variants Series (293) - Sudoku Switch')
		
if __name__ == '__main__':
    unittest.main()