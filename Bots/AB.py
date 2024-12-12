import copy
from pickle import GLOBAL
from typing import override
from dataclasses import dataclass
from typing import Generator
import numpy as np
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


@dataclass
class Move:
    start: tuple[int, int]
    end: tuple[int, int]

@dataclass
class ChessBoard:
    board: list[list[str]]

class ChessPiece:
    piece_name: str = ''
    piece_value: int = 0

    possible_moves: list[tuple[int, int]] = []
    board_placement_heuristic: list[list[int]] = []

    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str, color_on_top: str) -> Generator[Move, None, None]:
      raise NotImplementedError

    # {board : move, board : move}
    def get_resulting_boards(self, board: ChessBoard, x_position, y_position, color: str, color_on_top: str) -> Generator[tuple[ChessBoard, Move], None, None]:
        for possible_move in self.get_possible_moves(board, x_position, y_position, color, color_on_top):
            new_board = ChessBoard(copy.deepcopy(board.board))
            new_board.board[possible_move.start[0]][possible_move.start[1]] = ''
            new_board.board[possible_move.end[0]][possible_move.end[1]] = self.piece_name + color

            # # Change the last row pawns to queens
            # if possible_move.end[0] == 0 and color == 'w' and self.piece_name == 'p':
            #     new_board.board[possible_move.end[0]][possible_move.end[1]] = 'qw'
            # elif possible_move.end[0] == len(board.board) - 1 and color == 'b' and self.piece_name == 'p':
            #     new_board.board[possible_move.end[0]][possible_move.end[1]] = 'qp'

            yield new_board, possible_move


    def get_current_value(self,x_position: int, y_position: int) -> int:
        # return self.board_placement_heuristic[x_position][y_position] + self.piece_value
        return  self.piece_value

class LeapingPiece(ChessPiece):
    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str, color_on_top) -> Generator[Move, None, None]:
        direction: int = 1 if color == color_on_top else -1

        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1] * direction

            if x < 0 or x >= len(board.board) or y < 0 or y >= len(board.board[0]):
                continue
            if board.board[y][x] == '' or board.board[y][x][1] != color:
                yield Move((y_position, x_position), (y, x))

class SlidingPiece(ChessPiece):
    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str, color_on_top: str) -> Generator[Move, None, None]:
        direction: int = 1 if color == color_on_top else -1

        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1] * direction
            while 0 <= x < len(board.board) and 0 <= y < len(board.board[0]):
                if board.board[y][x] == '':
                    yield Move((y_position, x_position), (y, x))
                elif board.board[y][x][1] != color:
                    yield Move((y_position, x_position), (y, x))
                    break
                else:
                    break
                x += move[0]
                y += (move[1]) * direction

class King(LeapingPiece):
    piece_name = 'k'
    piece_value = 20000

    possible_moves = [(1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)]
    board_placement_heuristic_black_on_top = [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]
    ]

    board_placement_heuristic_white_on_top = np.flipud(board_placement_heuristic_black_on_top)

class Knight(LeapingPiece):
    piece_name = 'n'
    piece_value = 320

    possible_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    board_placement_heuristic_black_on_top = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,  0,  0,  0,  0, -20, -40],
        [-30,  0, 10, 15, 15, 10,  0, -30],
        [-30,  5, 15, 20, 20, 15,  5, -30],
        [-30,  0, 15, 20, 20, 15,  0, -30],
        [-30,  5, 10, 15, 15, 10,  5, -30],
        [-40, -20,  0,  5,  5,  0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

    board_placement_heuristic_white_on_top = np.flipud(board_placement_heuristic_black_on_top)

class Pawn(ChessPiece):
    piece_name = 'p'
    piece_value = 100

    possible_moves = [(0, 1)]
    board_placement_heuristic_black_on_top = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    board_placement_heuristic_white_on_top = np.flipud(board_placement_heuristic_black_on_top)

    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str, color_on_top: str) -> Generator[Move, None, None]:

        direction: int = 1 if color == color_on_top else -1

        # Regular moves
        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1] * direction
            print("Y: ", y)

            if x < 0 or x >= len(board.board) or y < 0 or y >= len(board.board[0]):
                continue
            if board.board[y][x] == '':
                print("Move: ", (y_position, x_position), (y, x))
                yield Move((y_position, x_position), (y, x))

        # Account for the possible eating moves
        for move in [(1, 1), (-1, 1)]:
            x: int = x_position + move[0]
            y: int = y_position + move[1] * direction

            if x < 0 or x >= len(board.board) or y < 0 or y >= len(board.board[0]):
                continue
            if board.board[y][x] != '' and board.board[y][x][1] != color:
                yield Move((y_position, x_position), (y, x))


class Rock(SlidingPiece):
    piece_name = 'r'
    piece_value = 500

    possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    board_placement_heuristic_black_on_top = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5, 0,  0,  0,  0,  0,  0, -5],
        [-5, 0,  0,  0,  0,  0,  0, -5],
        [-5, 0,  0,  0,  0,  0,  0, -5],
        [-5, 0,  0,  0,  0,  0,  0, -5],
        [-5, 0,  0,  0,  0,  0,  0, -5],
        [0, 0,  0,  5,  5,  0,  0,  0]
    ]

    board_placement_heuristic_white_on_top = np.flipud(board_placement_heuristic_black_on_top)


class Bishop(SlidingPiece):
    piece_name = 'b'
    piece_value = 330

    possible_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    board_placement_heuristic_black_on_top = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,  0,  0,  0,  0,  0,  0, -10],
        [-10,  0,  5, 10, 10,  5,  0, -10],
        [-10,  5,  5, 10, 10,  5,  5, -10],
        [-10,  0, 10, 10, 10, 10,  0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10,  5,  0,  0,  0,  0,  5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

    board_placement_heuristic_white_on_top = np.flipud(board_placement_heuristic_black_on_top)


class Queen(SlidingPiece):
    piece_name = 'q'
    piece_value = 900

    possible_moves = [(1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)]
    board_placement_heuristic_black_on_top = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0,  0,  0,  0,  0,  0, -10],
        [-10, 0,  5,  5,  5,  5,  0, -10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,   0,  5,  5,  5,  5,  0, -5],
        [-10, 5,  5,  5,  5,  5,  0, -10],
        [-10, 0,  5,  0,  0,  0,  0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    board_placement_heuristic_white_on_top = np.flipud(board_placement_heuristic_black_on_top)

class Board:

    piece_dictionary = {'k': King(), 'n': Knight(), 'p': Pawn(), 'r': Rock(), 'b': Bishop(), 'q': Queen()}

    color_on_top: str
    def __init__(self, color_on_top: str):
        self.color_on_top = color_on_top


    def get_current_value(self, board:ChessBoard) -> int:
        res = 0

        for y in range(len(board.board)):
            for x in range(len(board.board[0])):
                square = board.board[y][x]
                if square != "":
                    square_piece = square[0]
                    square_color = square[1]
                    if square_color == 'w':
                        res += self.piece_dictionary[square_piece].get_current_value(x, y)
                    else:
                        res -= self.piece_dictionary[square_piece].get_current_value(x, y)
        print(board.board)
        print("Value: ", res)
        return res

    def get_possible_boards(self,board:ChessBoard, color: str) -> list[tuple[ChessBoard, Move]]:

        res: list[tuple[ChessBoard, Move]] = []
        for y in range(len(board.board)):
            for x in range(len(board.board[0])):
                square = board.board[y][x]
                if square != "":
                    square_piece = square[0]
                    square_color = square[1]
                    if square_color == color:
                        res += self.piece_dictionary[square_piece].get_resulting_boards(board, x, y, color, self.color_on_top)
        return res

def chess_bot(player_sequence, actual_board, time_budget, **kwargs):

    chess_board: ChessBoard = ChessBoard(actual_board)
    board_class: Board = Board(player_sequence[1])
    best_move: Move = Move((0, 0), (0, 0))

    
    def minmax(board: ChessBoard,depth: int, color:str, maximize: bool = True) -> float:
        nonlocal board_class
        nonlocal best_move

        opponent_color: str = 'w' if color == 'b' else 'b'
        if depth == 0:
            return board_class.get_current_value(board)
        if maximize:
            max_value: float = float('-inf')
            for board, move in board_class.get_possible_boards(board,color):
                value = minmax(board,depth - 1, opponent_color, False)
                if value > max_value:
                    max_value = value
                    best_move = move
            return max_value
        else:
            min_value = float('inf')
            for board, move in board_class.get_possible_boards(board,color):
                value = minmax(board,depth - 1, opponent_color, True)
                min_value = min(min_value, value)
            return min_value

    print("Starting min max")

    minmax(chess_board,1, player_sequence[1])

    return best_move.start, best_move.end

#   Example how to register the function
register_chess_bot("AB_BOT", chess_bot)


