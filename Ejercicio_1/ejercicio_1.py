import os
import sys
import statistics
sys.path.append('../aima-python')
sys.path.append('../libs')
from generators import *
from data_collector import *

def index_of(list, element):
	try:
		return list.index(element)
	except:
		return -1

def generate_csv(size, iterations, timeout, data):

	algorithms = data.keys()

	puzzle_info = 'NPuzzle Problem,size = {}, iterations = {}, timeout = {}s\n\n'.format(size, iterations, timeout)
	csv_header = 'Algorithm,Heuristic,,Length_Min,Length_Max,Length_Mean,Length_Median,Length_Modes,,Time_Min,Time_Max,Time_Mean,Time_Median,Time_Modes,,Success,Timed_Up\n'

	csv_file = open('./stats/{}Puzzle_{}Iterations.csv'.format(size, iterations), 'w')
	csv_file.write(puzzle_info + csv_header)
	for algorithm in algorithms:
		csv_file.write('{}'.format(algorithm))
		algorithm_heuristics = data.get(algorithm)
		for heuristic_data in algorithm_heuristics:
			success_indexes = [i for i in range(len(heuristic_data[2])) if heuristic_data[2][i] != -1]
			row_data = (heuristic_data[0], [len(s) for s in heuristic_data[1] if index_of(success_indexes, index_of(heuristic_data[1], s)) > -1], [t for t in heuristic_data[2] if index_of(success_indexes, index_of(heuristic_data[2], t)) > -1])
			success_amount = len(row_data[2])
			error_amount = iterations - success_amount
			row_text = ',{},,{},{},{},{},"{}",,{},{},{},{},"{}",,{},{}\n'.format(row_data[0], '-' if len(row_data[1]) == 0 else min(row_data[1]), '-' if len(row_data[1]) == 0 else max(row_data[1]), '-' if len(row_data[1]) == 0 else statistics.mean(row_data[1]), '-' if len(row_data[1]) == 0 else statistics.median(row_data[1]), '-' if len(row_data[1]) == 0 else [modes[0] for modes in statistics._counts(row_data[1])], '-' if len(row_data[2]) == 0 else min(row_data[2]), '-' if len(row_data[2]) == 0 else max(row_data[2]), '-' if len(row_data[2]) == 0 else statistics.mean(row_data[2]), '-' if len(row_data[2]) == 0 else statistics.median(row_data[2]), '-' if len(row_data[2]) == 0 else [modes[0] for modes in statistics._counts(row_data[2])], success_amount, error_amount)
			csv_file.write(row_text)
	csv_file.close()

def help():
	print('Usage:')
	print('\tpython3 ejercicio_1.py (-s [SIZE])? (-i [ITERATIONS])? (-t [TIME_OUT])? (--plot-best)?')
	print('\n')
	print('\t-s [SIZE]\t\t\tSets the size of the puzzle (8, 15, ...). Default is 8')
	print('\t-i [ITERATIONS]\t\tSets the number of iterations to run the algorithms. Default is 100')
	print('\t-t [TIME_OUT]\t\tSets the number of seconds to run each algorithm for an instance of the problem. Default is 10')
	print('\t--plot-best\t\t\tUse this flag if you want to plot solutions of all algorithms. Default is False')
	print('\n')
	print('\tThe results are saved in the "stats" folder')

def control_args():
	arguments_passed = False
	# Control over the arguments
	try:
		if (sys.argv.index('--help') > -1):
			arguments_passed = True
			return None
	except:
		pass

	try:
		size = int(sys.argv[sys.argv.index('-s')+1])
		arguments_passed = True
	except:
		size = 8

	try:
		iterations = int(sys.argv[sys.argv.index('-i')+1])
		arguments_passed = True
	except:
		iterations = 100

	try:
		time_out = int(sys.argv[sys.argv.index('-t')+1])
		arguments_passed = True
	except:
		time_out = 10

	try:
		if (sys.argv.index('--plot-solutions') > -1):
			show_solutions = True
			arguments_passed = True
		else:
			show_solutions = False
	except:
		show_solutions = False

	if (not arguments_passed):
		if (len(sys.argv) > 1):
			print('Unrecognized argument detected.')
		print('Use --help flag to see all possible configurations.')

	return (size, iterations, time_out, show_solutions)

def main():
	args = control_args()
	if (args == None):
		help()
	else:
		size = args[0]
		iterations = args[1]
		time_out = args[2]
		show_solutions = args[3]

		# The instances are created
		puzzles = []
		for i in range(iterations):
			#Generating a random instance of the problem
			initial_state = NPuzzleGenerator(size).generateValidInstance()
			puzzles.append(NPuzzle(initial_state))
		
		data_greedy_best_first = DataCollector.collect_greedy_best_first(puzzles, size, iterations, time_out)
		data_best_first_tree = DataCollector.collect_best_first_tree(puzzles, size, iterations, time_out)

		data_astar = DataCollector.collect_astar_search(puzzles, size, iterations, time_out)
		data_astar_tree = DataCollector.collect_astar_tree_search(puzzles, size, iterations, time_out)

		data_iterative = DataCollector.collect_iterative_deepening(puzzles, size, iterations, time_out)
		data_iterative_graph = DataCollector.collect_iterative_deepening_graph(puzzles, size, iterations, time_out)

		generate_csv(size, iterations, time_out, {'Greedy Best First Search': data_greedy_best_first, 'Best First Tree Search': data_best_first_tree, 'A* Search': data_astar, 'A* Tree Search': data_astar_tree, 'Iterative Deepening Search': (data_iterative, ), 'Iterative Deepening Graph Search': (data_iterative_graph, )})

if __name__ == '__main__':
    main()