import unittest
from multiSudoku import *
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Event Horizon
	# Author: Pwinn (rhymes with Quinn)
	# Link: https://sudokupad.app/75hiatdehl
	# Constraints tested: soheiSudoku, setMultiConstraint, setXSudokuMain, setCage, setThermo, setRenbanLine, setGravityCage
	
	def test_puzzle(self):
		p = soheiSudoku(3)
		p.setMultiConstraint(1,'XSudokuMain',[])
		p.setMultiConstraint(1,'Cage',[[13,14],13])
		p.setMultiConstraint(1,'Cage',[[16,17],15])
		p.setMultiConstraint(1,'Cage',[[21,22],15])
		p.setMultiConstraint(1,'Cage',[[28,29,38],22])
		p.setMultiConstraint(1,'Cage',[[34,35,36],18])
		p.setMultiConstraint(1,'Cage',[[45,55,65],16])
		p.setMultiConstraint(1,'Cage',[[52,53],14])
		p.setMultiConstraint(1,'Cage',[[57,58],7])
		p.setMultiConstraint(1,'Cage',[[66,76,86],7])
		p.setMultiConstraint(1,'Cage',[[68,69,78,79],10])
		p.setMultiConstraint(1,'Cage',[[82,83,84],13])
		
		p.setMultiConstraint(2,'Thermo',[[39,49,59]])
		p.setMultiConstraint(2,'Thermo',[[44,55,64,73]])
		p.setMultiConstraint(2,'Thermo',[[52,43,34,25,14,23,32,41]])
		p.setMultiConstraint(2,'Thermo',[[69,68,58]])
		p.setMultiConstraint(2,'Thermo',[[86,75,84,83,82]])
		p.setMultiConstraint(2,'Thermo',[[87,77,67,57,47,37,27]])
		p.setMultiConstraint(2,'Thermo',[[99,98,97,96,95,94]])
		
		p.setMultiConstraint(3,'RenbanLine',[[11,21,22,23,33]])
		p.setMultiConstraint(3,'RenbanLine',[[14,15,16,17]])
		p.setMultiConstraint(3,'RenbanLine',[[19,29,39,38,37]])
		p.setMultiConstraint(3,'RenbanLine',[[24,34,44,54,53,52,42,32]])
		p.setMultiConstraint(3,'RenbanLine',[[27,26,35]])
		p.setMultiConstraint(3,'RenbanLine',[[46,45,55,65,64]])
		p.setMultiConstraint(3,'RenbanLine',[[47,48,58]])
		p.setMultiConstraint(3,'RenbanLine',[[49,59,69,79,89,99]])
		p.setMultiConstraint(3,'RenbanLine',[[57,67,68]])
		p.setMultiConstraint(3,'RenbanLine',[[92,82,73,83,93]])
		p.setMultiConstraint(3,'RenbanLine',[[94,84,85,96]])
		p.setMultiConstraint(3,'RenbanLine',[[87,77,88,98]])
		
		p.setMultiConstraint(4,'GravityCage',[[13,14],p.Right,p.Down])
		p.setMultiConstraint(4,'GravityCage',[[16,26],p.Right,p.Down])
		p.setMultiConstraint(4,'GravityCage',[[25,35,45,55],p.Right,p.Down])
		p.setMultiConstraint(4,'GravityCage',[[36,37,46,47,56,57],p.Right,p.Down])
		p.setMultiConstraint(4,'GravityCage',[[41,42,43,51,52,53,61,62,63],p.Right,p.Down])
		p.setMultiConstraint(4,'GravityCage',[[71,81],p.Right,p.Down])
		p.setMultiConstraint(4,'GravityCage',[[82,92,93],p.Right,p.Down])
		p.setMultiConstraint(4,'GravityCage',[[73,74,83,84],p.Right,p.Down])
		p.setMultiConstraint(4,'GravityCage',[[85,95],p.Right,p.Down])
		p.setMultiConstraint(4,'GravityCage',[[78,79,88,89,98,99],p.Right,p.Down])
		
		self.assertEqual(p.countSolutions(test=True),'1:534918726697243185281765493312459678468137259759682341176594832923871564845326917394528176856741923271396845932465718418273569765819432649152387587634291123987654832567419564891237917432658459613872623748591781259346145986723376125984298374165387926145291458376654371298123784659468295731579613482742569813916837524835142967','Failed Event Horizon')
		
if __name__ == '__main__':
    unittest.main()