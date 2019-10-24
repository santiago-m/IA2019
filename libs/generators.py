from random import randint
from problems import *

class NQueensGenerator:
  def __init__(self, N):
    self.queens = N

  def generateInstance(self):
    tmp = []
    for i in range (0, self.queens):
      tmp.append(randint(1, self.queens))
    return tuple(tmp)

class NPuzzleGenerator:
  def __init__(self, N):
    self.tiles = N

  def generateValidInstance(self):
  	tmp = [i for i in range(self.tiles + 1)]
  	aux_problem = NPuzzle(tmp)
  	while True:
  		random.shuffle(tmp)
  		if (aux_problem.check_solvability(tmp)):
  			return tuple(tmp)

