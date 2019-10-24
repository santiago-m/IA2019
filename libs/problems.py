import sys
import os
import subprocess
sys.path.append('../aima-python')
from search import *
from arithmetic import *
import math

'''
  NQueens Problem
'''

class NQueens(Problem):
  """The problem of placing N queens on an NxN board with none attacking
  each other.  A state is represented as an N-element array, where
  a value of r in the c-th entry means there is a queen at column c,
  row r, and a value of -1 means that the c-th column has not been
  filled in yet.  We fill in columns left to right.
  >>> depth_first_tree_search(NQueensProblem(8))
  <Node (7, 3, 0, 2, 5, 1, 6, 4)>
  """

  def __init__(self, N):
    self.N = N
    self.initial = tuple([-1] * N)
    Problem.__init__(self, self.initial)

  def actions(self, state):
    """In the leftmost empty column, try all non-conflicting rows."""
    if state[-1] is not -1:
      return []  # All columns filled; no successors
    else:
      col = state.index(-1)
      return [row for row in range(self.N)
              if not self.conflicted(state, row, col)]

  def result(self, state, row):
    """Place the next queen at the given row."""
    col = state.index(-1)
    new = list(state[:])
    new[col] = row
    return tuple(new)

  def conflicted(self, state, row, col):
    """Would placing a queen at (row, col) conflict with anything?"""
    return any(self.conflict(row, col, state[c], c)
               for c in range(col))

  def conflict(self, row1, col1, row2, col2):
    """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
    return (row1 == row2 or  # same row
            col1 == col2 or  # same column
            row1 - col1 == row2 - col2 or  # same \ diagonal
            row1 + col1 == row2 + col2)  # same / diagonal

  def goal_test(self, state):
    """Check if all columns filled, no conflicts."""
    if state[-1] is -1:
      return False
    return not any(self.conflicted(state, state[col], col)
                   for col in range(len(state)))

  def h(self, node):
    """Return number of conflicting queens for a given node"""
    num_conflicts = 0
    for (r1, c1) in enumerate(node.state):
      for (r2, c2) in enumerate(node.state):
        if (r1, c1) != (r2, c2):
          num_conflicts += self.conflict(r1, c1, r2, c2)

    return num_conflicts

  def value(self, state):
    return self.N - state.count(-1)

  def plot_states(self, states):
    if (len(states) > 0):
      print(str(states))
      print("Plotting State...")
      os.environ['IA_NQUEEN_STATES'] = str(states)
      fnull = open(os.devnull, 'w')
      subprocess.call(['java', '-jar', '../processing/processing-py.jar', '../processing/draw-queens.py'])
      #subprocess.call(['java', '-jar', 'processing/processing-py.jar', 'processing/draw-queens.py'], stdout=fnull, stderr=fnull)
      fnull.close()

'''
  NPuzzle Problem
'''
class NPuzzle(Problem):
  ''' The problem of sliding tiles numbered from 1 to N on a MxM board where M = sqrt(N+1),
  where one of the squares is a blank. A state is represented as a tuple of length N+1,
  where element at index i represents the tile number  at index i (0 if it's an empty square) '''

  def __init__(self, initial, goal = ()):
    ''' Check if length is valid '''
    if (not is_perfectsquare(len(initial))):
      raise Exception('The length of states must be a perfect square')
    if (len(goal) > 0 and len(goal) != len(initial)):
      raise Exception('The length of the initial state must be equal to goal state\'s length')
    ''' If goal was not setted it's set '''
    if (len(goal) == 0):
      self.goal = [i for i in range(1, len(initial))]
      self.goal.append(0)
      self.goal = tuple(self.goal)
    else:
      self.goal = goal
    Problem.__init__(self, initial, self.goal)

  def find_blank_square(self, state):
    '''Return the index of the blank square in a given state'''
    return state.index(0)

  def actions(self, state):
    ''' Return the actions that can be executed in the given state.
    The result would be a list, since there are only four possible actions
    in any given state of the environment '''

    ''' set the limit according to N '''
    limit = int(math.sqrt(len(state)))
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    index_blank_square = self.find_blank_square(state)

    if index_blank_square % limit == 0:
      possible_actions.remove('LEFT')
    if index_blank_square < limit:
      possible_actions.remove('UP')
    if index_blank_square % limit == limit-1:
      possible_actions.remove('RIGHT')
    if index_blank_square >= len(state) - limit:
      possible_actions.remove('DOWN')

    return possible_actions

  def result(self, state, action):
    ''' Given state and action, return a new state that is the result of the action.
    Action is assumed to be a valid action in the state '''

    # blank is the index of the blank square
    blank = self.find_blank_square(state)
    new_state = list(state)

    ''' set the limit according to N '''
    limit = int(math.sqrt(len(state)))

    delta = {'UP': -limit, 'DOWN': limit, 'LEFT': -1, 'RIGHT': 1}
    neighbor = blank + delta[action]
    new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

    return tuple(new_state)

  def goal_test(self, state):
    ''' Given a state, return True if state is a goal state or False, otherwise '''
    return state == self.goal

  def check_solvability(self, state):
    ''' Checks if the given state is solvable '''
    inversion = 0
    for i in range(len(state)):
      for j in range(i + 1, len(state)):
        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
          inversion += 1

    return inversion % 2 == 0

  def h(self, node):
    ''' Return the heuristic value for a given state. Default heuristic function used is 
    h(n) = number of misplaced tiles '''

    return sum(s != g for (s, g) in zip(node.state, self.goal))

  def apply_step(self, state, step):
    res = list(state)
    if (self.actions(state).index(step) > -1):
      limit = int(math.sqrt(len(state)))
      old_index = self.find_blank_square(state)
      if (step == 'RIGHT'):
        new_state = old_index + 1
      elif (step == 'LEFT'):
        new_state = old_index - 1
      elif (step == 'UP'):
        new_state = old_index - limit
      elif (step == 'DOWN'):
        new_state = old_index + limit
      new_index_value = state[new_state]
      res[new_state] = 0
      res[old_index] = new_index_value

    return tuple(res)

  def play_solution(self, solution):
    movements = []
    aux_state = self.initial
    for step in solution:
      aux_state = self.apply_step(aux_state, step)
      movements.append(aux_state)

    ej1_first_res = open("./results/ej1_first_result.data", "w")
    limit = int(math.sqrt(len(self.initial)))
    for m in movements:
      formatted_state = []
      aux = 0
      for i in range(limit):
        formatted_state.append(m[aux:limit+aux])
        aux += limit
      ej1_first_res.write(str(formatted_state) + '\n')
    ej1_first_res.close()

    print("Plotting Solution...")
    os.environ['IA_DRAW_FILE'] = './results/ej1_first_result.data'
    fnull = open(os.devnull, 'w')
    subprocess.call(['java', '-jar', '../processing/processing-py.jar', '../processing/draw-puzzle.py'], stdout=fnull, stderr=fnull)
    fnull.close()