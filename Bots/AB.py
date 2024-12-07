from pickle import GLOBAL
from typing import override
from dataclasses import dataclass

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

    # possible_moves = [(x,y), (x,y), ...]
    possible_moves: list[tuple[int]] = []
    board_placement_heuristic: list[list[int]] = []

    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str) -> list[Move]:
      raise NotImplementedError

    # {board : move, board : move}
    def get_resulting_boards(self, board: ChessBoard, x_position, y_position, color) -> list[tuple[ChessBoard, Move]]:
        for possible_move in self.get_possible_moves(board, x_position, y_position, color):
            new_board = ChessBoard(board.board)
            new_board.board[x_position][y_position] = ''
            new_board.board[possible_move.end[0]][possible_move.end[1]] = color + self.piece_name

            # Change the last row pawns to queens
            if possible_move.end[0] == 0 and color == 'w' and self.piece_name == 'p':
                new_board.board[possible_move.end[0]][possible_move.end[1]] = 'wq'
            elif possible_move.end[0] == len(board.board) - 1 and color == 'b' and self.piece_name == 'p':
                new_board.board[possible_move.end[0]][possible_move.end[1]] = 'bq'

            yield new_board, possible_move


    def get_current_value(self,x_position: int, y_position: int) -> int:
        return self.board_placement_heuristic[x_position][y_position] + self.piece_value

class LeapingPiece(ChessPiece):
    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str) -> list[Move]:
        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1]

            if x < 0 or x >= len(board.board) or y < 0 or y >= len(board.board[0]):
                continue
            if board.board[y][x] == '' or board.board[y][x][1] != color:
                yield Move((y_position, x_position), (y, x))

class SlidingPiece(ChessPiece):
    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str) -> list[Move]:
        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1]
            while 0 <= x < len(board.board) and 0 <= y < len(board.board[0]):
                if board.board[y][x] == '':
                    yield Move((y_position, x_position), (y, x))
                elif board.board[y][x][1] != color:
                    yield Move((y_position, x_position), (y, x))
                    break
                else:
                    break
                x += move[0]
                y += move[1]

class King(LeapingPiece):
    piece_name = 'k'
    piece_value = 20000

    possible_moves = [(1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)]
    board_placement_heuristic = [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]
    ]

class Knight(LeapingPiece):
    piece_name = 'n'
    piece_value = 320

    possible_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    board_placement_heuristic = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,  0,  0,  0,  0, -20, -40],
        [-30,  0, 10, 15, 15, 10,  0, -30],
        [-30,  5, 15, 20, 20, 15,  5, -30],
        [-30,  0, 15, 20, 20, 15,  0, -30],
        [-30,  5, 10, 15, 15, 10,  5, -30],
        [-40, -20,  0,  5,  5,  0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]


class Pawn(ChessPiece):
    piece_name = 'p'
    piece_value = 100

    possible_moves = [(0, 1)]
    board_placement_heuristic = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str) -> list[Move]:

        # Regular moves
        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1]

            if x < 0 or x >= len(board.board) or y < 0 or y >= len(board.board[0]):
                continue
            if board.board[y][x] == '':
                yield Move((y_position, x_position), (y, x))

        # Account for the possible eating moves
        for move in [(1, 1), (-1, 1)]:
            x: int = x_position + move[0]
            y: int = y_position + move[1]

            if x < 0 or x >= len(board.board) or y < 0 or y >= len(board.board[0]):
                continue
            if board.board[y][x] != '' and board.board[y][x][1] != color:
                yield Move((y_position, x_position), (y, x))


class Rock(SlidingPiece):
    piece_name = 'r'
    piece_value = 500

    possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    board_placement_heuristic = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5, 0,  0,  0,  0,  0,  0, -5],
        [-5, 0,  0,  0,  0,  0,  0, -5],
        [-5, 0,  0,  0,  0,  0,  0, -5],
        [-5, 0,  0,  0,  0,  0,  0, -5],
        [-5, 0,  0,  0,  0,  0,  0, -5],
        [0, 0,  0,  5,  5,  0,  0,  0]
    ]

class Bishop(SlidingPiece):
    piece_name = 'b'
    piece_value = 330

    possible_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    board_placement_heuristic = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,  0,  0,  0,  0,  0,  0, -10],
        [-10,  0,  5, 10, 10,  5,  0, -10],
        [-10,  5,  5, 10, 10,  5,  5, -10],
        [-10,  0, 10, 10, 10, 10,  0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10,  5,  0,  0,  0,  0,  5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

class Queen(SlidingPiece):
    piece_name = 'q'
    piece_value = 900

    possible_moves = [(1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)]
    board_placement_heuristic = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0,  0,  0,  0,  0,  0, -10],
        [-10, 0,  5,  5,  5,  5,  0, -10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,   0,  5,  5,  5,  5,  0, -5],
        [-10, 5,  5,  5,  5,  5,  0, -10],
        [-10, 0,  5,  0,  0,  0,  0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

class Board:

    piece_dictionary = {'k': King(), 'n': Knight(), 'p': Pawn(), 'r': Rock(), 'b': Bishop(), 'q': Queen()}

    def get_current_value(self, board: ChessBoard, color: str) -> int:
        res = 0

        for y in range(len(board.board)):
            for x in range(len(board.board[0])):
                square = board.board[y][x]
                if square != "":
                    square_piece = square[0]
                    square_color = square[1]
                    if square_color == color:
                        res += self.piece_dictionary[square_piece].get_current_value(x, y)
                    else:
                        res -= self.piece_dictionary[square_piece].get_current_value(x, y)
        return res

    def get_possible_boards(self, board: ChessBoard, color: str) -> list[tuple[ChessBoard, Move]]:

        res: list[tuple[ChessBoard, Move]] = []
        for y in range(len(board.board)):
            for x in range(len(board.board[0])):
                square = board.board[y][x]
                if square != "":
                    square_piece = square[0]
                    square_color = square[1]
                    if square_color == color:
                        res += self.piece_dictionary[square_piece].get_resulting_boards(board, x, y, color)
        return res

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


