import random
import copy
import numpy as np
from typing import Generator, override
from Bots.AB_Data_Class import ChessBoard, Move


class ChessPiece:
    piece_name: str = ''
    piece_value: int = 0
    possible_moves: list[tuple[int, int]] = []
    board_placement_heuristic: list[list[int]] = []

    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str, color_on_top: str) -> Generator[Move, None, None]:
        raise NotImplementedError

    def get_resulting_boards(self, board: ChessBoard, x_position, y_position, color: str, color_on_top: str) -> Generator[tuple[ChessBoard, Move], None, None]:
        for possible_move in self.get_possible_moves(board, x_position, y_position, color, color_on_top):
            new_board = ChessBoard(copy.deepcopy(board.board))
            new_board.board[possible_move.start[0]][possible_move.start[1]] = ''
            if possible_move.promotion:
                new_board.board[possible_move.end[0]][possible_move.end[1]] = 'q'+ color
            else:
                new_board.board[possible_move.end[0]][possible_move.end[1]] = self.piece_name + color
            yield new_board, possible_move

    def get_current_value(self, x_position: int, y_position: int) -> int:
        return self.piece_value

class LeapingPiece(ChessPiece):
    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str, color_on_top) -> Generator[Move, None, None]:
        direction: int = 1 if color == color_on_top else -1
        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1] * direction
            if 0 <= x < len(board.board) and 0 <= y < len(board.board[0]) and (board.board[y][x] == '' or board.board[y][x][1] != color):
                yield Move((y_position, x_position), (y, x))

class SlidingPiece(ChessPiece):
    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str, color_on_top: str) -> Generator[Move, None, None]:
        direction: int = 1 if color == color_on_top else -1
        for move in self.possible_moves:
            x, y = x_position + move[0], y_position + move[1] * direction
            while 0 <= x < len(board.board) and 0 <= y < len(board.board[0]):
                if board.board[y][x] == '':
                    yield Move((y_position, x_position), (y, x))
                elif board.board[y][x][1] != color:
                    yield Move((y_position, x_position), (y, x))
                    break
                else:
                    break
                x += move[0]
                y += move[1] * direction

# Subclasses for pieces
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

    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_black_on_top)
    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_white_on_top)

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

    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_black_on_top)
    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_white_on_top)

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

    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_black_on_top)

    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, color: str, color_on_top: str) -> Generator[Move, None, None]:

        direction: int = 1 if color == color_on_top else -1
        promotion_row: int = 0 if direction == -1 else len(board.board) - 1

        # Regular moves
        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1] * direction

            if x < 0 or x >= len(board.board) or y < 0 or y >= len(board.board[0]):
                continue
            if board.board[y][x] == '':
                if y == promotion_row:
                    yield Move((y_position, x_position), (y, x), promotion=True)
                else:
                    yield Move((y_position, x_position), (y, x))

        # Account for the possible eating moves
        for move in [(1, 1), (-1, 1)]:
            x: int = x_position + move[0]
            y: int = y_position + move[1] * direction

            if x < 0 or x >= len(board.board) or y < 0 or y >= len(board.board[0]):
                continue
            if board.board[y][x] != '' and board.board[y][x][1] != color:
                if y == promotion_row:
                    yield Move((y_position, x_position), (y, x), promotion=True)
                else:
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

    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_black_on_top)
    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_white_on_top)

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

    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_black_on_top)
    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_white_on_top)
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

    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_black_on_top)
    board_placement_heuristic_white_on_top = np.rot90(board_placement_heuristic_white_on_top)

