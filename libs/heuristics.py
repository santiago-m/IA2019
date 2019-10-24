import math

class EightPuzzleHeuristics:
  goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

  @staticmethod
  def linear(node):
    return sum([1 if node.state[i] != EightPuzzleHeuristics.goal[i] else 0 for i in range(8)])

  @staticmethod
  def manhattan(node):
    state = node.state
    index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    x, y = 0, 0

    for i in range(len(state)):
      print(len(state))
      print(state[i])
      index_state[state[i]] = index[i]

    mhd = 0

    for i in range(8):
      for j in range(2):
        mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

    return mhd

  @staticmethod
  def sqrt_manhattan(node):
    state = node.state
    index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    x, y = 0, 0

    for i in range(len(state)):
      index_state[state[i]] = index[i]

    mhd = 0

    for i in range(8):
      for j in range(2):
        mhd = (index_goal[i][j] - index_state[i][j])**2 + mhd

    return math.sqrt(mhd)

  @staticmethod
  def max_heuristic(node):
    score1 = EightPuzzleHeuristics.manhattan(node)
    score2 = EightPuzzleHeuristics.linear(node)
    return max(score1, score2)

  @staticmethod
  def misplaced_tiles(node):
    displaced = 0
    state = node.state
    for i in range(0, len(state)):
      if (state[i] - EightPuzzleHeuristics.goal[i] != 0):
        displaced += 1
    return displaced

  @staticmethod
  def gaschnig(node):
    movements = 0
    state = list(node.state)
    while (state != EightPuzzleHeuristics.goal):
      current_blank_index = state.index(0)
      if (current_blank_index == 8):
        first_wrong = [i for i, j in zip(state, EightPuzzleHeuristics.goal) if i != j][0]
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

  @staticmethod
  def max_manhattan_gaschnig(node):
    score1 = EightPuzzleHeuristics.manhattan(node)
    score2 = EightPuzzleHeuristics.gaschnig(node)
    return max(score1, score2)