"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

class GameException(Exception):
   pass

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counter = 0
    for row in board:
      counter += row.count(None)
    if counter % 2 == 1:
      return X
    else:
      return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for row_index, row in enumerate(board):
      for cell_index, cell in enumerate(row):
        if not cell:
           moves.add((row_index, cell_index))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not None:
      raise GameException('Illegal move, spot taken')
    else:
      new_board = copy.deepcopy(board)
      new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
  """
  Returns the winner of the game, if there is one.
  """
  winner = None
  winner = check_rows(board)
  if winner is not None:
     return winner
  winner = check_columns(board)
  if winner is not None:
     return winner
  winner = check_diagonals(board)
  return winner

def check_rows(board):
  for row in board:
    if row[0] == row[1] == row[2]:
      return row[0]
  return None
def check_columns(board):
  for x in range(3):
    if board[0][x] == board[1][x] == board[2][x]:
      return board[0][x]
  return None
def check_diagonals(board):
  if board[0][0] == board[1][1] == board[2][2]:
    return board[0][0]
  if board[0][2] == board[1][1] == board[2][0]:
     return board[0][2]
  return None

def terminal(board):
  """
  Returns True if game is over, False otherwise.
  """
  gameover = winner(board)
  if gameover is not None:
    return True
  for x in range(3):
    for y in range(3):
      if board[x][y] is None:
        return False
  return True


def utility(board):
  """
  Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
  """
  winning_player = winner(board)
  if winning_player == X:
    return 1
  if winning_player == O:
    return -1
  return 0


def minimax(board):
  """
  Returns the optimal action for the current player on the board.
  """
  if terminal(board):
    return None
  if player(board) == X:
    value = -math.inf
    best_move = None
    for action in actions(board):
      minimum = min_value(result(board, action))
      maximum = max(minimum, value)
      if maximum != value:
        value = maximum
        best_move = action
    return best_move
  if player(board) == O:
    value = math.inf
    best_move = None
    for action in actions(board):
      maximum = max_value(result(board, action))
      minimum = min(maximum, value)
      if minimum != value:
        value = minimum
        best_move = action
    return best_move
  return actions(board).pop()

def min_value(board):
  if terminal(board):
    return utility(board)
  value = math.inf
  best_action = None
  for action in actions(board):
    maximum = max_value(result(board, action))
    """"
    minimum = min(maximum, value)
    if minimum != value:
      value = minimum
      best_action = action
    """
    value = min(maximum, value)
  return value

def max_value(board):
  if terminal(board):
    return utility(board)
  value = -math.inf
  best_action = None
  for action in actions(board):
    minimum = min_value(result(board, action))
    """"
    maximum = max(minimum, value)
    if maximum != value:
      value = maximum
      best_action = action
    """
    value = max(minimum, value)
  return value