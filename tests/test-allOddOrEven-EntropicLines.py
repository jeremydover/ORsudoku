import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Entroparity
	# Author: clover!
	# https://sudokupad.app/2xq0az12ee
	# Constraints tested: setAllOddOrEven, setGivenArray, setEntropicLine
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		lines=[[15,14,13,23,22,32,31,41,51],[25,24,34,33,43,42,52],[27,37,38,48],[44,45],[58,68,67,77,76,86,85],[59,69,79,78,88,87,97,96,95],[62,72,73,83],[65,66]]
		for x in lines:
			p.setEntropicLine(x)
			p.setAllOddOrEven(x)
		p.setGivenArray([187,252,396,436,511,555,593,674,716,858,929])
		
		self.assertEqual(p.countSolutions(test=True),'1:463591278859627341712834596586243917124759683937168425675412839341986752298375164','Failed Entroparity')
		
if __name__ == '__main__':
    unittest.main()