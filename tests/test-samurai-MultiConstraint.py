import unittest
from multiSudoku import samuraiSudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Samurai Sudoku with Renban Groups
	# Author: zhergan
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=0000KD
	# Constraints tested: samuraiSudoku, setGivenArray, setRenbanLine
	
	def test_puzzle(self):
		p = samuraiSudoku(3)
		p.setMultiConstraint(1,'GivenArray',[161,184,213,238,366,382,477,493,546,555,568,615,639,727,748,856,926,957])
		p.setMultiConstraint(2,'GivenArray',[126,189,241,259,262,323,418,482,493,542,551,567,664,687,752,799,845,853,992])
		p.setMultiConstraint(3,'GivenArray',[169,362,486,495,518,535,688,692,763,968])
		p.setMultiConstraint(4,'GivenArray',[125,159,255,328,347,416,432,545,557,562,673,692,769,781,817,834,967,986])
		p.setMultiConstraint(5,'GivenArray',[193,241,253,354,398,468,486,543,551,562,613,681,697,722,849,857,861,926,985])
		p.setMultiConstraint(1,'RenbanLine',[31,22,33,24,15])
		p.setMultiConstraint(1,'RenbanLine',[69,78,87,96])
		p.setMultiConstraint(2,'RenbanLine',[15,16,17,28,39])
		p.setMultiConstraint(2,'RenbanLine',[61,72,83,94])
		p.setMultiConstraint(3,'RenbanLine',[45,54,55,56,65])
		p.setMultiConstraint(4,'RenbanLine',[16,27,38,49])
		p.setMultiConstraint(4,'RenbanLine',[71,82,93,84,75])
		p.setMultiConstraint(5,'RenbanLine',[14,23,32,41])
		p.setMultiConstraint(5,'RenbanLine',[76,87,88,89,99])
		
		self.assertEqual(p.countSolutions(test=True),'1:627531948348297615195486327486129753732658491519743862974815236853962174261374589165843297784192356239765841817659423453217968692384175571428639928536714346971582236489571174365928589172346492837165865214793317956482748523619623791854951648237251693748947851623386724951612938574439572186875416392568349217724165839193287465619287543854139726237546198142798365576312489398654217923465871485971632761823954','Failed Samurai Sudoku with Renban Groups')
		
if __name__ == '__main__':
    unittest.main()