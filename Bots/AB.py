from pickle import GLOBAL
from typing import override

#
#   Example function to be implemented for
#       Single important function is next_best
#           color: a single character str indicating the color represented by this bot ('w' for white)
#           board: a 2d matrix containing strings as a descriptors of the board '' means empty location "XC" means a piece represented by X of the color C is present there
#           budget: time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs, ys moving to xd, yd
#

from PyQt6 import QtCore

#   Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot
our_player_sequence = "w"

class ChessPiece:
    piece_name: str = ''
    piece_value: int = 0

    # possible_moves = [(x,y), (x,y), ...]
    possible_moves: list[tuple[int]] = []
    board_placement_heuristic: list[list[int]] = []

    def get_possible_moves(self, board: list[list[str]], x_position: int, y_position: int, color: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
      raise NotImplementedError

    # {board : move, board : move}
    def get_resulting_boards(self, board, x_position, y_position, color) -> dict[list[list[str]], tuple]:
        res = {}
        for possible_move in self.get_possible_moves(board, x_position, y_position, color):
              new_board = [row.copy() for row in board]
              new_board[x_position][y_position] = ''
              new_board[possible_move[1][0]][possible_move[1][1]] = color + self.char_name
              res[new_board] = possible_move
        return res


    def get_current_value(self,x_position, y_position) -> float:
        return self.board_placement_heuristic[x_position][y_position] + self.piece_value

class LeapingPiece(ChessPiece):
    @override
    def get_possible_moves(self, board: list[list[str]], x_position: int, y_position: int, color: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1]

            if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
                continue
            if board[y][x] == '' or board[y][x][1] != color:
                yield (y_position, x_position), (y, x)

class SlidingPiece(ChessPiece):
    @override
    def get_possible_moves(self, board: list[list[str]], x_position: int, y_position: int, color: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1]
            while 0 <= x < len(board) and 0 <= y < len(board[0]):
                if board[y][x] == '':
                    yield (y_position, x_position), (y, x)
                elif board[y][x][1] != color:
                    yield (y_position, x_position), (y, x)
                    break
                else:
                    break
                x += move[0]
                y += move[1]

class King(LeapingPiece):
    piece_name = 'k'
    piece_value = 100

    possible_moves = [(1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)]
    board_placement_heuristic = [
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-2, -3, -3, -4, -4, -3, -3, -2],
        [-1, -2, -2, -3, -3, -2, -2, -1],
        [2, 2, 0, 0, 0, 0, 2, 2],
        [2, 3, 1, 0, 0, 1, 3, 2]
    ]

class Knight(LeapingPiece):
    piece_name = 'n'
    piece_value = 3

    possible_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    board_placement_heuristic = []


class Pawn(ChessPiece):
    piece_name = 'p'
    piece_value = 1

    possible_moves = [(0, 1)]
    board_placement_heuristic = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 2, 3, 3, 2, 1, 1],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [1, -1, -2, 0, 0, -2, -1, 1],
        [1, 2, 2, -2, -2, 2, 2, 1],
        [1, 1, 1, -3, -3, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    @override
    def get_possible_moves(self, board: list[list[str]], x_position: int, y_position: int, color: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:

        # Regular moves
        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1]

            if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
                continue
            if board[y][x] == '':
                yield (y_position, x_position), (y, x)

        # Account for the possible eating moves
        for move in [(1, 1), (-1, 1)]:
            x: int = x_position + move[0]
            y: int = y_position + move[1]

            if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
                continue
            if board[y][x] != '' and board[y][x][1] != color:
                yield (y_position, x_position), (y, x)


class Rock(SlidingPiece):
    piece_name = 'r'
    piece_value = 3

    possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    board_placement_heuristic = []

class Bishop(SlidingPiece):
    piece_name = 'b'
    piece_value = 3

    possible_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    board_placement_heuristic = []

class Queen(SlidingPiece):
    piece_name = 'q'
    piece_value = 9

    possible_moves = [(1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)]
    board_placement_heuristic = []


piece_dictionary = {}

#   Simply move the pawns forward and tries to capture as soon as possible
def chess_bot(player_sequence, board, time_budget, **kwargs):
    if player_sequence[0]== our_player_sequence :
        return minimax(board,4)[1]


    return (0,0), (0,0)
def minimax(board, depth) -> tuple[float, tuple[tuple[int, int],tuple[int, int]]]:
    if  depth == 0: #todo ajouter: or la game est fini
        return evaluate(board)

    best = -10000
    mv = (0,0), (0,0)
    #todo il faut prendre en compte que le meilleur coup de l'adversia
    for move in board.moves():#listmove
        board = simule_move(board,move)
        res = minimax(board, depth - 1)
        val = res[0]
        mv = res[1]
        if val > best:
            best = val
            mv = move

    return best, mv

def evaluate (board)  -> float:
    res = 0.0
    for x in board:
        for y in x:
            if y != "":
                if y[0] == "w":
                    res += piece_dictionary[x[0]].get_current_value(board.index(x),x.index(y))
                else:
                    res -= piece_dictionary[x[0]].get_current_value(board.index(x),x.index(y))
    return res

def simule_move(board,move) :
    tmp = board[move[0]]
    board[move[0][0]][move[0][1]] = ""
    board[move[1][0]][move[1][1]] = tmp
    return board


#   Example how to register the function
register_chess_bot("AB_BOT", chess_bot)


