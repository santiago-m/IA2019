import sys
sys.path.append('../aima-python')
sys.path.append('../libs')
from problems import *
import ast

if (len(sys.argv) < 2):
	print('This script must be used as follow:')
	print('\tpython graph_npuzzle [(title, <BOARD>)]')
	print('\twhere:')
	print('\t\ttitle is a name to show for the state')
	print('\t\t<BOARD> is a state of the board as a consecutives number array starting at zero, and stringified')
	print('\t\t(title, <Board>) is a stringified tuple that includes one title and one board')
	print('\t\t[(title, <Board>)] implies that multiple states are allowed')
else:
	states = [(s[0], ast.literal_eval(s[1])) for s in [ast.literal_eval(arg) for arg in sys.argv[1:]]]
	NQueens(len(states[0][1])).plot_states(states)