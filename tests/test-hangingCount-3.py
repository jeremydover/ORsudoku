import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Sudoku Variants Series (235) - Outside Parity Sudoku
	# Author: Richard Stolk
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0002UE
	# Constraints tested: setHangingCount, setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		# See test-hangingCount-2 for an explanation of why the clue values are one less than 
		# those given in the puzzle.
		
		p.setHangingCount(1,2,p.Col,1,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(1,3,p.Col,1,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(1,4,p.Col,2,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(1,6,p.Col,1,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(1,7,p.Col,1,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(1,8,p.Col,0,[['ParityAll']],[('ParityChangeReached',1)])
		
		p.setHangingCount(2,9,p.Row,0,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(3,9,p.Row,0,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(5,9,p.Row,0,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(9,9,p.Row,0,[['ParityAll']],[('ParityChangeReached',1)])
		
		p.setHangingCount(9,2,p.Col,0,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(9,3,p.Col,0,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(9,7,p.Col,0,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(9,8,p.Col,2,[['ParityAll']],[('ParityChangeReached',1)])
		
		p.setHangingCount(2,1,p.Row,1,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(3,1,p.Row,0,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(5,1,p.Row,0,[['ParityAll']],[('ParityChangeReached',1)])
		p.setHangingCount(9,1,p.Row,0,[['ParityAll']],[('ParityChangeReached',1)])
		
		p.setGivenArray([114,157,193,259,412,498,531,574,641,658,663,716,733,777,799,825,882,949,966])
			
		self.assertEqual(p.countSolutions(test=True),'1:496871253312495867785632194239764518871259436564183972623518749958347621147926385','Failed Sudoku Variants Series (235) - Outside Parity Sudoku')
		
if __name__ == '__main__':
    unittest.main()