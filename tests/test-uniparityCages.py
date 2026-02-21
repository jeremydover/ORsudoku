import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: 2/2/25: Never Odd Or Even
	# Author: clover!
	# Link: https://www.gmpuzzles.com/blog/2026/02/all-odd-or-even-sudoku-by-clover/
	# Constraints tested: setUniparityCage,setGivenArray
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setGivenArray([182,213,265,335,354,367,379,423,432,531,573,674,685,738,742,755,771,846,898,921])
		p.setUniparityCage([22,31,32])
		p.setUniparityCage([14,24])
		p.setUniparityCage([17,27,28])
		p.setUniparityCage([61,62])
		p.setUniparityCage([45,54,55,56,65])
		p.setUniparityCage([48,49])
		p.setUniparityCage([82,83,93])
		p.setUniparityCage([86,96])
		p.setUniparityCage([78,79,88])
		
		self.assertEqual(p.countSolutions(test=True),'1:197368524384925716625147983532416897841579362976832451768254139453691278219783645','Failed 2/2/25: Never Odd Or Even')
		
if __name__ == '__main__':
    unittest.main()