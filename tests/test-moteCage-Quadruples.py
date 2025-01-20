import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: The MOTE in Quad's Eye
	# Author: jeremydover
	# https://sudokupad.app/2twdt893iu
	# Constraints tested: setMOTECage, setQuadruple
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setMOTECage([11,12,13,21,31])
		p.setMOTECage([17,18,19,29,39])
		p.setMOTECage([91,92,93,71,81])
		p.setMOTECage([97,98,99,79,89])
		p.setMOTECage([45,46,55,64,65])
		p.setMOTECage([57,67,68,69])
		p.setMOTECage([41,42,43,53])
		p.setMOTECage([85,86,95,96])
		p.setMOTECage([38,48])
	
		p.setQuadruple(2213)
		p.setQuadruple(2735)
		p.setQuadruple(7235)
		p.setQuadruple(7757)
		p.setQuadruple(432359)
		p.setQuadruple(563589)
		p.setQuadruple(641348)
		p.setQuadruple(352569)
		p.setQuadruple(48278)
		p.setQuadruple(8869)
	
		self.assertEqual(p.countSolutions(test=True),'1:594683127263714589781952634815369472649275318327148965952836741138497256476521893','Failed The MOTE in Quad\'s Eye')
		
if __name__ == '__main__':
    unittest.main()