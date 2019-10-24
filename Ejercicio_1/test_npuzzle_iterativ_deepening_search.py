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

global length
global init_time
global end_time

global lengths
global times

global size
global iterations

iterations = 50
''' ------------------------------------------------------------------------------------- '''

''' -------------------this functions return a collection of states---------------------- '''
def random_states(size, quantity):
	return (NPuzzleGenerator(size).generateValidInstance() for i in range(quantity))
'''-------------------------------------------------------------------------------------- '''

''' ------------------------------------------------------------------------------------- '''
@pytest.mark.timeout(5)
@pytest.mark.parametrize("state", random_states(3, iterations))
def test_search(state):
	puzzle = NPuzzle(state)
	global init
	global end
	global length
	global lengths
	global times
	global size
	global iterations

	size = len(state)-1
	init = time.time()
	solution = iterative_deepening_search(puzzle).solution()
	end = time.time()
	length = len(solution)
	assert len(solution) == 0 if puzzle.goal_test(state) else len(solution) > 0
''' ------------------------------------------------------------------------------------- '''

@pytest.fixture(scope="module", autouse=True)
def around_module(request):
	global csv_file
	global csv_info
	global csv_header
	global size
	global iterations

	lengths = []
	times = []
	yield

	min_lengths = '-' if len(lengths) == 0 else str(min(lengths))
	max_lengths = '-' if len(lengths) == 0 else str(max(lengths))
	mean_lengths = '-' if len(lengths) == 0 else str(statistics.mean(lengths))
	median_lengths = '-' if len(lengths) == 0 else str(statistics.median(lengths))
	modes_manhanttan_lengths = '-' if len(lengths) == 0 else str([modes[0] for modes in statistics._counts(lengths)])

	min_times = '-' if len(times) == 0 else str(min(times))
	max_times = '-' if len(times) == 0 else str(max(times))
	mean_times = '-' if len(times) == 0 else str(statistics.mean(times))
	median_times = '-' if len(times) == 0 else str(statistics.median(times))
	modes_manhanttan_times = '-' if len(times) == 0 else str([modes[0] for modes in statistics._counts(times)])


	csv_info = 'NPuzzle Problem.,size = ' + str(aux_size) + '\n\n'
	csv_header = 'Algorithm,Heuristic,Iterations,,Length_Min,Length_Max,Length_Mean,Length_Median,Length_Modes,,Time_Min,Time_Max,Time_Mean,Time_Median,Time_Modes,,Timed_Up\n'
	csv_file = open('./stats/{}-{}.csv'.format(request.module.__name__, str(now)), 'w')
	csv_file.write(csv_info)
	csv_file.write(csv_header)
	csv_row = '{},{},{},,{},{},{},{},"{}",,{},{},{},{},"{}",,{}\n'.format('Iterative Deepening Search', '-', iterations, min_lengths, max_lengths, mean_lengths, median_lengths, modes_manhanttan_lengths, min_times, max_times, mean_times, median_times, modes_manhanttan_times, iterations - len(lengths))
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