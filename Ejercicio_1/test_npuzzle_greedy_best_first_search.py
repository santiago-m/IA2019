import os
import sys
sys.path.append('../aima-python')
sys.path.append('../libs')
from problems import *
from generators import *
from heuristics import *
from generic_heuristics import *
import pytest
import time
import statistics
from datetime import datetime

''' ---------------this variables are used to write the statistic results---------------- '''
global csv_file
global csv_info
global csv_header
global csv_body
''' Variables used to keep register of time and length of solutions '''
global length
global init_time
global end_time

global manhattan_lengths
global manhattan_times
global misplaced_lengths
global misplaced_times
global gaschnig_lengths
global gaschnig_times
global max_man_gasch_lengths
global max_man_gasch_times

global aux_lengths
global aux_times

global aux_size
global aux_iterations

''' Variables used to maintain the best result for each heuristic '''
global manhattan_best_result
global misplaced_best_result
global gaschnig_best_result
global max_man_gasch_best_result

manhattan_iterations = 50
misplaced_iterations = 50
gaschnig_iterations = 50
max_man_gasch_iterations = 50
''' ------------------------------------------------------------------------------------- '''

''' -------------------this functions return a collection of states---------------------- '''
def random_states(size, quantity):
	return (NPuzzleGenerator(size).generateValidInstance() for i in range(quantity))
'''-------------------------------------------------------------------------------------- '''

''' ------------------------------------------------------------------------------------- '''
@pytest.mark.timeout(5)
@pytest.mark.parametrize("state", random_states(8, manhattan_iterations))
def test_manhattan_heuristic(state):
	puzzle = NPuzzle(state)
	global init
	global end
	global length
	global aux_lengths
	global aux_times
	global aux_size
	global aux_iterations
	global manhattan_best_result

	aux_size = len(state)-1
	aux_iterations = manhattan_iterations
	init = time.time()
	solution = greedy_best_first_graph_search(puzzle, NPuzzleHeuristics(aux_size).manhattan).solution()
	end = time.time()
	length = len(solution)
	aux_lengths = manhattan_lengths
	aux_times = manhattan_times
	if (manhattan_best_result == None or length < len(manhattan_best_result[1])):
		manhattan_best_result = (puzzle.initial, solution)
	assert len(solution) == 0 if puzzle.goal_test(state) else len(solution) > 0

@pytest.mark.timeout(5)
@pytest.mark.parametrize("state", random_states(8, misplaced_iterations))
def test_misplaced_tiles_heuristic(state):
	puzzle = NPuzzle(state)
	global init
	global end
	global length
	global aux_lengths
	global aux_times
	global aux_size
	global aux_iterations
	global misplaced_best_result

	aux_size = len(state)-1
	aux_iterations = misplaced_iterations
	init = time.time()
	solution = greedy_best_first_graph_search(puzzle, NPuzzleHeuristics(aux_size).misplaced_tiles).solution()
	end = time.time()
	length = len(solution)
	aux_lengths = misplaced_lengths
	aux_times = misplaced_times
	if (misplaced_best_result == None or length < len(misplaced_best_result[1])):
		misplaced_best_result = (puzzle.initial, solution)
	assert len(solution) == 0 if puzzle.goal_test(state) else len(solution) > 0

@pytest.mark.timeout(5)
@pytest.mark.parametrize("state", random_states(8, gaschnig_iterations))
def test_gaschnig_heuristic(state):
	puzzle = NPuzzle(state)
	global init
	global end
	global length
	global aux_lengths
	global aux_times
	global aux_size
	global aux_iterations
	global gaschnig_best_result

	aux_size = len(state)-1
	aux_iterations = gaschnig_iterations
	init = time.time()
	solution = greedy_best_first_graph_search(puzzle, NPuzzleHeuristics(aux_size).gaschnig).solution()
	end = time.time()
	length = len(solution)
	aux_lengths = gaschnig_lengths
	aux_times = gaschnig_times
	if (gaschnig_best_result == None or length < len(gaschnig_best_result[1])):
		gaschnig_best_result = (puzzle.initial, solution)
	assert len(solution) == 0 if puzzle.goal_test(state) else len(solution) > 0

@pytest.mark.timeout(5)
@pytest.mark.parametrize("state", random_states(8, max_man_gasch_iterations))
def test_max_manhattan_gaschnig_heuristic(state):
	puzzle = NPuzzle(state)
	global init
	global end
	global length
	global aux_lengths
	global aux_times
	global aux_size
	global aux_iterations
	global max_man_gasch_best_result

	aux_size = len(state)-1
	aux_iterations = max_man_gasch_iterations
	init = time.time()
	solution = greedy_best_first_graph_search(puzzle, NPuzzleHeuristics(aux_size).max_manhattan_gaschnig).solution()
	end = time.time()
	length = len(solution)
	aux_lengths = max_man_gasch_lengths
	aux_times = max_man_gasch_times
	if (max_man_gasch_best_result == None or length < len(max_man_gasch_best_result[1])):
		max_man_gasch_best_result = (puzzle.initial, solution)
	assert len(solution) == 0 if puzzle.goal_test(state) else len(solution) > 0
''' ------------------------------------------------------------------------------------- '''

@pytest.fixture(scope="module", autouse=True)
def around_module(request):
	global csv_file
	global csv_info
	global csv_header
	global manhattan_lengths
	global manhattan_times
	global misplaced_lengths
	global misplaced_times
	global gaschnig_lengths
	global gaschnig_times
	global max_man_gasch_lengths
	global max_man_gasch_times
	global aux_size
	global aux_iterations
	global manhattan_iterations
	global gaschnig_iterations
	global misplaced_iterations

	global manhattan_best_result
	global misplaced_best_result
	global gaschnig_best_result
	global max_man_gasch_best_result

	manhattan_lengths = []
	manhattan_times = []
	misplaced_lengths = []
	misplaced_times = []
	gaschnig_lengths = []
	gaschnig_times = []
	max_man_gasch_lengths = []
	max_man_gasch_times = []

	manhattan_best_result = None
	misplaced_best_result = None
	gaschnig_best_result = None
	max_man_gasch_best_result = None

	yield
	''' manhattan aux vars '''
	min_manhattan_lengths = '-' if len(manhattan_lengths) == 0 else str(min(manhattan_lengths))
	max_manhattan_lengths = '-' if len(manhattan_lengths) == 0 else str(max(manhattan_lengths))
	mean_manhattan_lengths = '-' if len(manhattan_lengths) == 0 else str(statistics.mean(manhattan_lengths))
	median_manhattan_lengths = '-' if len(manhattan_lengths) == 0 else str(statistics.median(manhattan_lengths))
	modes_manhanttan_lengths = '-' if len(manhattan_lengths) == 0 else str([modes[0] for modes in statistics._counts(manhattan_lengths)])

	min_manhattan_times = '-' if len(manhattan_times) == 0 else str(min(manhattan_times))
	max_manhattan_times = '-' if len(manhattan_times) == 0 else str(max(manhattan_times))
	mean_manhattan_times = '-' if len(manhattan_times) == 0 else str(statistics.mean(manhattan_times))
	median_manhattan_times = '-' if len(manhattan_times) == 0 else str(statistics.median(manhattan_times))
	modes_manhanttan_times = '-' if len(manhattan_times) == 0 else str([modes[0] for modes in statistics._counts(manhattan_times)])

	''' misplaced tiles aux vars '''
	min_misplaced_lengths = '-' if len(misplaced_lengths) == 0 else str(min(misplaced_lengths))
	max_misplaced_lengths = '-' if len(misplaced_lengths) == 0 else str(max(misplaced_lengths))
	mean_misplaced_lengths = '-' if len(misplaced_lengths) == 0 else str(statistics.mean(misplaced_lengths))
	median_misplaced_lengths = '-' if len(misplaced_lengths) == 0 else str(statistics.median(misplaced_lengths))
	modes_manhanttan_lengths = '-' if len(misplaced_lengths) == 0 else str([modes[0] for modes in statistics._counts(misplaced_lengths)])

	min_misplaced_times = '-' if len(misplaced_times) == 0 else str(min(misplaced_times))
	max_misplaced_times = '-' if len(misplaced_times) == 0 else str(max(misplaced_times))
	mean_misplaced_times = '-' if len(misplaced_times) == 0 else str(statistics.mean(misplaced_times))
	median_misplaced_times = '-' if len(misplaced_times) == 0 else str(statistics.median(misplaced_times))
	modes_manhanttan_times = '-' if len(misplaced_times) == 0 else str([modes[0] for modes in statistics._counts(misplaced_times)])

	''' gaschnig aux vars '''
	min_gaschnig_lengths = '-' if len(gaschnig_lengths) == 0 else str(min(gaschnig_lengths))
	max_gaschnig_lengths = '-' if len(gaschnig_lengths) == 0 else str(max(gaschnig_lengths))
	mean_gaschnig_lengths = '-' if len(gaschnig_lengths) == 0 else str(statistics.mean(gaschnig_lengths))
	median_gaschnig_lengths = '-' if len(gaschnig_lengths) == 0 else str(statistics.median(gaschnig_lengths))
	modes_manhanttan_lengths = '-' if len(gaschnig_lengths) == 0 else str([modes[0] for modes in statistics._counts(gaschnig_lengths)])

	min_gaschnig_times = '-' if len(gaschnig_times) == 0 else str(min(gaschnig_times))
	max_gaschnig_times = '-' if len(gaschnig_times) == 0 else str(max(gaschnig_times))
	mean_gaschnig_times = '-' if len(gaschnig_times) == 0 else str(statistics.mean(gaschnig_times))
	median_gaschnig_times = '-' if len(gaschnig_times) == 0 else str(statistics.median(gaschnig_times))
	modes_manhanttan_times = '-' if len(gaschnig_times) == 0 else str([modes[0] for modes in statistics._counts(gaschnig_times)])

	''' max_manhattan_gaschnig aux vars '''
	min_max_man_gasch_lengths = '-' if len(max_man_gasch_lengths) == 0 else str(min(max_man_gasch_lengths))
	max_max_man_gasch_lengths = '-' if len(max_man_gasch_lengths) == 0 else str(max(max_man_gasch_lengths))
	mean_max_man_gasch_lengths = '-' if len(max_man_gasch_lengths) == 0 else str(statistics.mean(max_man_gasch_lengths))
	median_max_man_gasch_lengths = '-' if len(max_man_gasch_lengths) == 0 else str(statistics.median(max_man_gasch_lengths))
	modes_manhanttan_lengths = '-' if len(max_man_gasch_lengths) == 0 else str([modes[0] for modes in statistics._counts(max_man_gasch_lengths)])

	min_max_man_gasch_times = '-' if len(max_man_gasch_times) == 0 else str(min(max_man_gasch_times))
	max_max_man_gasch_times = '-' if len(max_man_gasch_times) == 0 else str(max(max_man_gasch_times))
	mean_max_man_gasch_times = '-' if len(max_man_gasch_times) == 0 else str(statistics.mean(max_man_gasch_times))
	median_max_man_gasch_times = '-' if len(max_man_gasch_times) == 0 else str(statistics.median(max_man_gasch_times))
	modes_manhanttan_times = '-' if len(max_man_gasch_times) == 0 else str([modes[0] for modes in statistics._counts(max_man_gasch_times)])


	if (manhattan_best_result == None):
		manhattan_best_result = []
	if (misplaced_best_result == None):
		misplaced_best_result = []
	if (gaschnig_best_result == None):
		gaschnig_best_result = []
	if (max_man_gasch_best_result == None):
		max_man_gasch_best_result = []

	csv_info = 'NPuzzle Problem.,size = ' + str(aux_size) + '\n\n'
	csv_header = 'Algorithm,Heuristic,Iterations,,Length_Min,Length_Max,Length_Mean,Length_Median,Length_Modes,,Time_Min,Time_Max,Time_Mean,Time_Median,Time_Modes,,Timed_Up,,Best_Result\n'

	now = datetime.now()
	
	csv_file = open('./stats/{}-{}.csv'.format(request.module.__name__, str(now)), 'w')
	csv_file.write(csv_info)
	csv_file.write(csv_header)

	''' manhattan row '''
	csv_row = '{},{},{},,{},{},{},{},"{}",,{},{},{},{},"{}",,{},,"{}"\n'.format('Greedy Best First Search', 'Manhattan', manhattan_iterations, min_manhattan_lengths, max_manhattan_lengths, mean_manhattan_lengths, median_manhattan_lengths, modes_manhanttan_lengths, min_manhattan_times, max_manhattan_times, mean_manhattan_times, median_manhattan_times, modes_manhanttan_times, manhattan_iterations - len(manhattan_lengths), manhattan_best_result)
	csv_file.write(csv_row)
	
	''' misplaced tiles row '''
	csv_row = '{},{},{},,{},{},{},{},"{}",,{},{},{},{},"{}",,{},,"{}"\n'.format('', 'Misplaced Tiles', misplaced_iterations, min_misplaced_lengths, max_misplaced_lengths, mean_misplaced_lengths, median_misplaced_lengths, modes_manhanttan_lengths, min_misplaced_times, max_misplaced_times, mean_misplaced_times, median_misplaced_times, modes_manhanttan_times, misplaced_iterations - len(misplaced_lengths), misplaced_best_result)
	csv_file.write(csv_row)

	''' gaschnig row '''
	csv_row = '{},{},{},,{},{},{},{},"{}",,{},{},{},{},"{}",,{},,"{}"\n'.format('', 'Gaschnig', gaschnig_iterations, min_gaschnig_lengths, max_gaschnig_lengths, mean_gaschnig_lengths, median_gaschnig_lengths, modes_manhanttan_lengths, min_gaschnig_times, max_gaschnig_times, mean_gaschnig_times, median_gaschnig_times, modes_manhanttan_times, gaschnig_iterations - len(gaschnig_lengths), gaschnig_best_result)
	csv_file.write(csv_row)

	''' max_manhattan_gaschnig row '''
	csv_row = '{},{},{},,{},{},{},{},"{}",,{},{},{},{},"{}",,{},,"{}"\n'.format('', 'Max_Manhattan_Gaschnig', max_man_gasch_iterations, min_max_man_gasch_lengths, max_max_man_gasch_lengths, mean_max_man_gasch_lengths, median_max_man_gasch_lengths, modes_manhanttan_lengths, min_max_man_gasch_times, max_max_man_gasch_times, mean_max_man_gasch_times, median_max_man_gasch_times, modes_manhanttan_times, max_man_gasch_iterations - len(max_man_gasch_lengths), max_man_gasch_best_result)
	csv_file.write(csv_row)

	csv_file.close()

@pytest.fixture(scope="function", autouse=True)
def around_function(request):
	global init
	global end
	global length
	length = 0
	init = 0
	end = 0
	yield
	if (length > 0):
		aux_times.append(round(end - init, 4))
		aux_lengths.append(length)