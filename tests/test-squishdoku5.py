import unittest
from squishdoku import squishdoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Mr. Squishface
	# Author: ThePedallingPianist
	# Link: https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000G6X
	# Constraints tested: squishdoku, setXVXArray, setKropkiBlackArray, setIndexColumn
	
	def test_puzzle(self):
		p = squishdoku(3)
		p.setGivenArray([345])
		p.setXVXArray([411,441,471])
		p.setKropkiBlackArray([221,261])
		p.setIndexColumn(1,inlist1=[5,6,7])
		p.setIndexColumn(2,inlist1=[2,3,7])
		p.setIndexColumn(3,inlist1=[7])
		p.setIndexColumn(4,inlist1=[4,5,7])
		p.setIndexColumn(5,inlist1=[7])
		p.setIndexColumn(6,inlist1=[2,3,7])
		p.setIndexColumn(7,inlist1=[5,6,7])
			
		self.assertEqual(p.countSolutions(test=True),'1:5138429849276572651389543276138795449216876754312','Failed Mr. Squishface')
		
if __name__ == '__main__':
    unittest.main()