# Ginger
# by: theasylm
# Link: https://sudokupad.app/7nk8wks72c

from japaneseSumSudoku import japaneseSumSudoku
import sys
from colorama import Fore,Back

def main(boardSizeRoot):
	p = japaneseSumSudoku(3,3)
	p.setColorMap([(Fore.WHITE,Back.CYAN),(Fore.BLACK,Back.WHITE),(Fore.BLACK,Back.GREEN),(Fore.WHITE,Back.BLACK)])
	p.setJapaneseSum(1,1,p.Col,[(3,1),(5,2)])
	p.setJapaneseSum(1,2,p.Col,[(2,1),(4,1),(9,2)])
	p.setJapaneseSum(1,3,p.Col,[(10,1),(2,3),(13,2)])
	p.setJapaneseSum(1,4,p.Col,[(15,1),(4,2)])
	p.setJapaneseSum(1,5,p.Col,[(8,1),(2,2)])
	p.setJapaneseSum(1,6,p.Col,[(16,1),(9,3),(11,2)])
	p.setJapaneseSum(1,7,p.Col,[(10,1),(5,2)])
	p.setJapaneseSum(1,8,p.Col,[(3,1),(13,2)])
	p.setJapaneseSum(1,9,p.Col,[(9,3),(3,2)])
	p.setJapaneseSum(2,1,p.Row,[(2,1),(1,1)])
	p.setJapaneseSum(3,1,p.Row,[(3,1),(6,1)])
	p.setJapaneseSum(4,1,p.Row,[(31,1),(9,3)])
	p.setJapaneseSum(5,1,p.Row,[(24,1)])
	p.setJapaneseSum(6,1,p.Row,[(1,1),(3,1)])
	p.setJapaneseSum(7,1,p.Row,[(2,3),(9,3)])
	p.setJapaneseSum(8,1,p.Row,[(1,2),(8,2),(4,2),(7,2)])
	p.setJapaneseSum(9,1,p.Row,[(45,2)])
	
	p.countSolutions()	
if __name__ == '__main__':
	boardSizeRoot = 3
	if len(sys.argv) > 1:
		boardSizeRoot = int(sys.argv[1])
	main(boardSizeRoot)