import os
import ast

w = 25 # width of each cell

try:
  # if a filename is set as enviroment variable
  states = os.environ.get('IA_NQUEEN_STATES')
  if (len(states) > 0):
    states = ast.literal_eval(states)
# else sets the default board
except:
  # default board
  states = [('Example', [0, 1, 2, 3, 4, 5, 6, 7, 8])]

state = states[0]
board = [[0 for j in range(len(state[1]))] for i in range(len(state[1]))]
for i in range(len(state[1])):
  board[i][state[1][i]] = 1
print(board)

def setup():
  # Sets the size of canvas
  size(w*len(board),w*len(board[0]))

def draw():
  global state
  fill(0)
  rect(0, 0, w*len(board), w)
  fill(255)
  textSize(30)
  text(state[0], 0, w/2)
  x,y = 0,w # starting position
  for row in board:
    for col in row:
      # color the rect
      if col == 1:
        fill(255, 0, 0)
      else:
        fill(255)
      rect(x, y, w, w)
      if (col == 0):
        # write number over rect
        fill(255)
        textSize(30)
        text('Q', x + w/2 - 2, y + w/2 + 2)
      x = x + w  # move right
    y = y + w # move down
    x = 0 # rest to left edge

def mousePressed():
  global states
  global state
  global board
  if (states.index(state) == len(states) - 1):
    exit()
  else:
    state = states[states.index(state) + 1]
    board = [[0 for j in range(len(state[1]))] for i in range(len(state[1]))]
    for i in range(len(state[1])):
      board[i][state[1][i]] = 1
