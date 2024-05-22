import unittest
import ORsudoku
  
class TestPuzzle(unittest.TestCase):
	# Puzzle: Bullet Catch
	# Author: BremSter
	# Link: https://bremster.tiny.us/bulletcatch
	# Constraints tested: setArrow,setCage,setZone
	
	def test_puzzle(self):
		p = ORsudoku.sudoku(3)
		p.setArrow([11,22,33])
		p.setArrow([36,25,24])
		p.setArrow([19,28,37])
		p.setArrow([62,51,41])
		p.setArrow([62,53,43])
		p.setArrow([46,55,64])
		p.setArrow([69,68,67])
		p.setArrow([91,82,83])
		p.setArrow([74,75,84])
		p.setArrow([98,88,78,89])
		p.setCage([23,33,32],9)
		p.setCage([14,15,16],12)
		p.setCage([29,39],14)
		p.setCage([42,52],9)
		p.setCage([55,56,65,66],12)
		p.setCage([57,58],11)
		p.setCage([82,83],9)
		p.setCage([74,75],13)
		p.setCage([77,87],10)
		p.setZone([11,12,13],[1])
		p.setZone([14,15,16],[2])
		p.setZone([17,18,19],[3])
		p.setZone([41,42,43],[4])
		p.setZone([44,45,46],[5])
		p.setZone([47,48,49],[6])
		p.setZone([71,72,73],[7])
		p.setZone([74,75,76],[8])
		p.setZone([77,78,79],[9])
		
		self.assertEqual(p.countSolutions(test=True),'1:819624375563179248742538196324785961675912834198463527237856419481397652956241783','Failed Bullet Catch')
		
if __name__ == '__main__':
    unittest.main()