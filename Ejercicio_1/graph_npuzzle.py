import sys
sys.path.append('../aima-python')
sys.path.append('../libs')
from problems import *
import ast

if (len(sys.argv) != 3):
	print('This script must be used as follow:')
	print('\tpython graph_npuzzle [STATE] [STEPS]')
	print('\twhere:')
	print('\t\t[STATE] is an number array stringified')
	print('\t\t[STEPS] is an array composed of (UP, DOWN, RIGHT, LEFT) stringified')
else:
	state = ast.literal_eval(sys.argv[1])
	steps = ast.literal_eval(sys.argv[2])

	puzzle = NPuzzle(state)
	puzzle.play_solution(steps)