# Ginger
# by: theasylm
# Link: https://sudokupad.app/7nk8wks72c

from japaneseSumSudoku import japaneseSumSudoku
import sys
from colorama import Fore,Back

def main(boardSizeRoot):
	p = japaneseSumSudoku(3,2)
	p.setColorMap([(Fore.WHITE,Back.BLACK),(Fore.WHITE,Back.BLUE),(Fore.BLACK,Back.RED)])
	p.setJapaneseSum(1,1,1,[(18,1)])
	p.setJapaneseSum(1,2,1,[(9,0),(3,0),(9,0),(8,0)])
	p.setJapaneseSum(1,3,1,[(3,0),(30,0),(3,0),(9,0)])
	p.setJapaneseSum(1,4,1,[(5,0),(40,0)])
	p.setJapaneseSum(1,5,1,[(45,2)])
	p.setJapaneseSum(1,6,1,[(9,0),(7,0),(6,0),(17,0)])
	p.setJapaneseSum(1,7,1,[(14,2),(11,2)])
	p.setJapaneseSum(1,8,1,[(14,2),(7,2)])
	p.setJapaneseSum(1,9,1,[(3,2)])
	p.setJapaneseSum(1,1,0,[(6,0),(6,0)])
	p.setJapaneseSum(2,1,0,[(6,0),(18,0)])
	p.setJapaneseSum(3,1,0,[(8,0),(18,0),(7,0),(3,0)])
	p.setJapaneseSum(4,1,0,[(5,0),(40,0)])
	p.setJapaneseSum(5,1,0,[(4,0),(23,0),(14,0)])
	p.setJapaneseSum(6,1,0,[(9,0),(14,0)])
	p.setJapaneseSum(7,1,0,[(9,0),(11,0)])
	p.setJapaneseSum(8,1,0,[(27,2)])
	p.setJapaneseSum(9,1,0,[(42,2)])
	p.setAntiKnight()
	
	p.countSolutions()	
if __name__ == '__main__':
	boardSizeRoot = 3
	if len(sys.argv) > 1:
		boardSizeRoot = int(sys.argv[1])
	main(boardSizeRoot)