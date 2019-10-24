import math
from arithmetic import *

class NPuzzleHeuristics:

  def __init__(self, size):
    if (not is_perfectsquare(size + 1)):
      raise Exception('El número ingresado no es válido. Debe quedar libre un único cuadrado en el tablero')
    self.N = size
    self.goal = [i for i in range(1, self.N + 1)]
    self.goal.append(0)

  def linear(self, node):
    return sum([1 if node.state[i] != self.goal[i] else 0 for i in range(self.N)])

  def manhattan(self, node):
    columns = int(math.sqrt(len(self.goal)))
    rows = columns
    state = node.state
    index_goal = {}
    index = []
    for i in range(0, rows):
      for j in range(0, columns):
        if (i * rows + j < self.N):
          index_goal[i * rows + j + 1] = [i, j]
        else:
          index_goal[0] = [i, j]
        index.append([i, j])
    index_state = {}
    x, y = 0, 0

    for i in range(len(state)):
      index_state[state[i]] = index[i]

    mhd = 0

    for i in range(self.N):
      for j in range(2):
        mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

    return mhd

  def sqrt_manhattan(self, node):
    columns = int(math.sqrt(len(self.goal)))
    rows = columns
    state = node.state
    index_goal = {}
    index = []
    for i in range(0, rows):
      for j in range(0, columns):
        if (i * rows + j < self.N):
          index_goal[i * rows + j + 1] = [i, j]
        else:
          index_goal[0] = [i, j]
        index.append([i, j])
    index_state = {}
    x, y = 0, 0

    for i in range(len(state)):
      index_state[state[i]] = index[i]

    mhd = 0

    for i in range(self.N):
      for j in range(2):
        mhd = (index_goal[i][j] - index_state[i][j])**2 + mhd

    return math.sqrt(mhd)

  def max_heuristic(self, node):
    score1 = self.manhattan(node)
    score2 = self.linear(node)
    return max(score1, score2)

  def misplaced_tiles(self, node):
    displaced = 0
    state = node.state
    for i in range(0, len(state)):
      if (state[i] - self.goal[i] != 0):
        displaced += 1
    return displaced

  def gaschnig(self, node):
    movements = 0
    state = list(node.state)
    while (state != self.goal):
      current_blank_index = state.index(0)
      if (current_blank_index == self.N):
        first_wrong = [i for i, j in zip(state, self.goal) if i != j][0]
        first_wrong_index =  state.index(first_wrong)
        state[current_blank_index] = first_wrong
        state[first_wrong_index] = 0
      else:
        correct_tile = current_blank_index + 1
        correct_tile_index = state.index(correct_tile)
        state[current_blank_index] = correct_tile
        state[correct_tile_index] = 0
      movements += 1
    return movements 

  def max_manhattan_gaschnig(self, node):
    score1 = self.manhattan(node)
    score2 = self.gaschnig(node)
    return max(score1, score2)