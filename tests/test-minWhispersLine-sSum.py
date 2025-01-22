import unittest
from schroedingerSudoku import schroedingerCellSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: American Whispers
	# Author: the_cogito and Memristor
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=00096I
	# Constraints tested: schroedingerCellSudoku, setMinWhisperLine, setGivenArray
	
	def test_puzzle(self):
		p = schroedingerCellSudoku(3)
		p.setGivenArray([157,221,392,994])
		p.setMinWhispersLine([23,24,25],8,sSum=True)
		p.setMinWhispersLine([24,34],8,sSum=True)
		p.setMinWhispersLine([24,35],8,sSum=True)
		p.setMinWhispersLine([27,28,29,38],8,sSum=True)
		p.setMinWhispersLine([41,42,52,41],8,sSum=True)
		p.setMinWhispersLine([46,57,66,55,46],8,sSum=True)
		p.setMinWhispersLine([65,76],8,sSum=True)
		p.setMinWhispersLine([68,79,88,77,68],8,sSum=True)
		p.setMinWhispersLine([77,87],8,sSum=True)
		p.setMinWhispersLine([79,89],8,sSum=True)
		p.setMinWhispersLine([78,88,98],8,sSum=True)
		p.setMinWhispersLine([88,97],8,sSum=True)
		p.setMinWhispersLine([82,93],8,sSum=True)
		p.setMinWhispersLine([74,84,94,83],8,sSum=True)
		
		self.assertEqual(p.countSolutions(test=True),'1:280179345713524809469308712875430621102796483634251097947862150321045968056917234000000006000600000500000000090000000000000500000080000000003000000000070008000000','Failed American Whispers')
		
if __name__ == '__main__':
    unittest.main()
	

