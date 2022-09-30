import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Schrödinger's Arrows
	# Author: starwarigami
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0008ST
	# Constraints tested: schroedingerCellSudoku, setArrow, setLittleKiller
	
	def test_puzzle(self):
		p = ORsudoku.schroedingerCellSudoku(3)
		p.setLittleKiller(1,1,2,2,84)
		p.setLittleKiller(1,2,2,1,3)
		p.setLittleKiller(1,8,2,9,5)
		p.setLittleKiller(1,9,2,8,89)
		p.setLittleKiller(6,9,7,8,14)
		p.setLittleKiller(8,9,9,8,11)
		p.setArrow([11,21,22,12],sSum=True)
		p.setArrow([28,29,19,18],sSum=True)
		p.setArrow([36,35,34],sSum=True)
		p.setArrow([37,46,56],sSum=True)
		p.setArrow([43,53,63],sSum=True)
		p.setArrow([67,57,47],sSum=True)
		p.setArrow([74,75,76],sSum=True)
		p.setArrow([82,81,91,92],sSum=True)
		p.setArrow([99,89,88,98],sSum=True)
		
		self.assertEqual(p.findSolution(test=True),'5*7*3426801909217356*8*4168540*9*723821*9*63547045708*9*26316037142*8*953164*8*5790227*8*5901346940326157*8*','Failed Schroedinger\'s Arrows')
		
if __name__ == '__main__':
    unittest.main()