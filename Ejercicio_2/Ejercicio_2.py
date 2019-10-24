import sys
sys.path.append('../aima-python')
sys.path.append('../libs')
from agents import *
from problems import *
from generators import *
from hill_climbing import *
from  heuristics import *
from generic_heuristics import *

#Exercise 2

results = open('./nqueen_solutions/solutions.data', 'w')

for i in range(1, 50):
	print('Size: {}...'.format(i))
	results.write('SIZE: {}\n'.format(i))
	tries = 1
	nqueenproblem = NQueens(i)
	# Hill Climbing
	for j in range(5):
		simple_hc = hill_climbing(nqueenproblem)
		if (not nqueenproblem.goal_test(simple_hc)):
			simple_hc = None
			tries += 1
		else:
			break
	results.write('After {} tries\n'.format(tries))
	if (simple_hc != None):
		results.write('\tHill Climbing: {}\n'.format(simple_hc))
	else:
		results.write('\tHill Climbing: Could not found a solution.\n')
	tries = 1

	# Hill Climbing with sideway moves
	for j in range(5):
		sideway_hc = sideway_moves_hill_climbing(nqueenproblem)
		if (not nqueenproblem.goal_test(sideway_hc)):
			sideway_hc = None
			tries += 1
		else:
			break
	results.write('After {} tries\n'.format(tries))
	if (sideway_hc != None):
		results.write('\tHill Climbing with sideway moves: {}\n'.format(sideway_hc))
	else:
		results.write('\tHill Climbing with sideway moves: Could not found a solution.\n')
	tries = 1

	# Hill Climbing with random restart
	for j in range(5):
		randrestart_hc = random_restart_hill_climbing(nqueenproblem, 100)
		if (not nqueenproblem.goal_test(randrestart_hc)):
			randrestart_hc = None
			tries += 1
		else:
			break
	results.write('After {} tries\n'.format(tries))
	if (randrestart_hc != None):
		results.write('\tHill Climbing with random restart: {}\n'.format(randrestart_hc))
	else:
		results.write('\tHill Climbing with random restart: Could not found a solution.\n')
	tries = 1

	# Simulated Annealing
	for j in range(5):
		sannealing = simulated_annealing(nqueenproblem)
		if (not nqueenproblem.goal_test(sannealing)):
			sannealing = None
			tries += 1
		else:
			break
	results.write('After {} tries\n'.format(tries))
	if (sannealing != None):
		results.write('\tSimulated Annealing: {}\n'.format(sannealing))
	else:
		results.write('\tSimulated Annealing: Could not found a solution.\n')

	results.write('\n\n')

results.close()
