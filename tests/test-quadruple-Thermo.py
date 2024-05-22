import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Three Degrees of Freedom
	# Author: jeremydover
	# Link: https://tinyurl.com/56chyumw
	# Constraints tested: setQuadruple, setThermo
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setThermo([11,12,13,23,33])
		p.setThermo([19,18,17,27,37])
		p.setQuadruple(21356)
		p.setQuadruple(28479)
		p.setThermo([91,82,73,63,52,41])
		p.setThermo([99,88,77,67,58,49])
		p.setQuadruple(68356)
		p.setQuadruple(61479)
		p.setQuadruple(84356)
		p.setQuadruple(45479)
		p.setThermo([96,86,76])
		p.setThermo([24,25,34])
		
		self.assertEqual(p.countSolutions(test=True),'1:147896532328451697659723814813675249762349185495182763974218356531967428286534971','Failed Three Degrees of Freedom')
		
if __name__ == '__main__':
    unittest.main()