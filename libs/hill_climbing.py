import sys
sys.path.append('../aima-python')
from search import *

def sideway_moves_hill_climbing(problem):
    """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Figure 4.2]"""
    current = Node(problem.initial)
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors, key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) < problem.value(current.state):
            break
        current = neighbor
    return current.state

def random_restart_hill_climbing(problem, iterations):
    best_state = None
    last_state = None
    for _ in range(0, iterations):
        last_state = hill_climbing(problem)
        if (best_state == None or problem.value(last_state) > problem.value(best_state)):
            best_state = last_state
    return best_state