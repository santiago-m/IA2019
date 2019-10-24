import os
import ast

w = 70 # width of each cell

try:
  # if a filename is set as enviroment variable
  filename = os.environ.get('IA_DRAW_FILE')
  if (len(filename) > 0):
    movements = [line.rstrip('\n') for line in open(filename)]
    for i in range(len(movements)):
      movements[i] = ast.literal_eval(movements[i])
    board = movements[0]
# else sets the default board
except:
  # default board and list of movements
  board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
  movements = [board]

def setup():
  # Sets the size of canvas
  size(w*len(board),w*len(board[0]))

def draw():
  x,y = 0,0 # starting position
  for row in board:
    for col in row:
      # color the rect
      if col == 0:
        fill(255)
      else:
        fill(100)
      rect(x, y, w, w)
      # write number over rect
      fill(255)
      textSize(20)
      text(col, x + w/2 - 2, y + w/2 + 2)
      x = x + w  # move right
    y = y + w # move down
    x = 0 # rest to left edge

def mousePressed():
  global movements;
  global board;
  if (movements.index(board) == len(movements) - 1):
    exit()
  else:
    board = movements[movements.index(board) + 1]
  # integer division is good here!