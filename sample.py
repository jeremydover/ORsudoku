# Sample Puzzle for ORSudoku.py
# Implements the puzzle fragment from https://f-puzzles.com/?id=2mxo5ny3
# Should have 10 feasible solutions

import ORsudoku
import sys

def main(boardSizeRoot):
	# This version uses full syntax for clarity
	p = ORsudoku.sudoku(boardSizeRoot)
	p.setXSudokuMain()
	p.setEvenOddArray([(1,5,p.Odd),(5,1,p.Even),(5,9,p.Even),(9,5,p.Odd)])
	p.setGivenArray([(1,2,3),(4,5,6),(7,8,9)])
	p.setKropkiBlack((1,7,p.Vert))
	p.setXVArray([(3,2,p.Horz,p.X),(7,7,p.Vert,p.V)])
	p.setCage([(8,1),(8,2),(9,1),(9,2)],20)
	p.setLittleKiller(1,9,2,8,45)
	p.setSandwichSum(6,1,p.Row,18)
	p.setQuadruple((4,3,1,1,2))
	p.setArrow([(3,9),(2,9),(2,8)])
	p.setThermo([(7,2),(6,2),(5,2),(4,2)])
	p.setPalindromeLine([(8,5),(9,6),(8,6),(9,7),(8,7),(7,7)])
	p.setBetweenLine([(4,8),(5,8),(6,8),(7,9)])
	
	# To find a single solution, which may or may not be unique
	p.findSolution()

	# If you're pretty close to a unique solution, you can try this, but need to be careful
	p.countSolutions()

	print()
	print('Now for p1...')

	# This is the same model, using shortcuts
	p1 = ORsudoku.sudoku(boardSizeRoot)
	p1.setXSudokuMain()
	p1.setEvenOddArray([151,510,590,951])
	p1.setGivenArray([123,456,789])
	p1.setKropkiBlack(171)
	p1.setXVArray([3201,7710])
	p1.setCage([81,82,91,92],20)
	p1.setLittleKiller(1,9,2,8,45)
	p1.setSandwichSum(6,1,p.Row,18)
	p1.setQuadruple(43112)
	p1.setArrow([39,29,28])
	p1.setThermo([72,62,52,42])
	p1.setPalindromeLine([85,96,86,97,87,77])
	p1.setBetweenLine([48,58,68,79])
	
	# If you love output
	p1.countSolutions(printAll=True)
		
if __name__ == '__main__':
  # By default, solve the 9x9 problem.
  boardSizeRoot = 3
  if len(sys.argv) > 1:
    boardSizeRoot = int(sys.argv[1])
  main(boardSizeRoot)