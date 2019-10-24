import os
import sys
import pytest
sys.path.append('../aima-python')
sys.path.append('../libs')
from problems import *
from generators import *
from heuristics import *
from generic_heuristics import *

''' -------------------this functions return a collection of states--------------------- '''
def random_states(size, quantity):
	return tuple([NPuzzleGenerator(size).generateValidInstance() for i in range(quantity)])

def goal_states():
	return [tuple([i for i in range(1, j)] + [0]) for j in [4, 9, 16, 25, 36, 49, 64]]
'''---------------------------------------------------------------------------------------'''

''' ---------------------comparing specific with general heuristics---------------------- '''
@pytest.mark.parametrize("state", random_states(8, 50))
def test_manhattan_specific_to_general(state):
	specific_heuristic_result = EightPuzzleHeuristics.manhattan(Node(state))
	general_heuristic_result = NPuzzleHeuristics(8).manhattan(Node(state))
	assert specific_heuristic_result == general_heuristic_result

@pytest.mark.parametrize("state", random_states(8, 50))
def test_misplaced_tiles_specific_to_general(state):
	specific_heuristic_result = EightPuzzleHeuristics.misplaced_tiles(Node(state))
	general_heuristic_result = NPuzzleHeuristics(8).misplaced_tiles(Node(state))
	assert specific_heuristic_result == general_heuristic_result

@pytest.mark.parametrize("state", random_states(8, 50))
def test_misplaced_tiles_specific_to_general(state):
	specific_heuristic_result = EightPuzzleHeuristics.gaschnig(Node(state))
	general_heuristic_result = NPuzzleHeuristics(8).gaschnig(Node(state))
	assert specific_heuristic_result == general_heuristic_result

@pytest.mark.parametrize("state", random_states(8, 50))
def test_misplaced_tiles_specific_to_general(state):
	specific_heuristic_result = EightPuzzleHeuristics.max_manhattan_gaschnig(Node(state))
	general_heuristic_result = NPuzzleHeuristics(8).max_manhattan_gaschnig(Node(state))
	assert specific_heuristic_result == general_heuristic_result
''' ------------------------------------------------------------------------------------- '''

''' ----------------testing general heuristics with multiple size puzzles---------------- '''
@pytest.mark.parametrize("state", goal_states())
def test_manhattan_goal_state_value(state):
	assert NPuzzleHeuristics(len(state)-1).manhattan(Node(state)) == 0

@pytest.mark.parametrize("state", goal_states())
def test_manhattan_goal_state_value(state):
	assert NPuzzleHeuristics(len(state)-1).misplaced_tiles(Node(state)) == 0

@pytest.mark.parametrize("state", goal_states())
def test_manhattan_goal_state_value(state):
	assert NPuzzleHeuristics(len(state)-1).gaschnig(Node(state)) == 0

@pytest.mark.parametrize("state", goal_states())
def test_manhattan_goal_state_value(state):
	assert NPuzzleHeuristics(len(state)-1).max_manhattan_gaschnig(Node(state)) == 0
''' ------------------------------------------------------------------------------------ '''

