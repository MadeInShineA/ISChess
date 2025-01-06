import random
import copy
import numpy as np
from typing import Generator, override
from Bots.AB_Data_Class import ChessBoard, Move


class ChessPiece:
    """

    Attributes: 
        piece_name: The Char representing the piece's name
        piece_value: The chosen piece value
        possible_moves: A list of the possible moves the piece can do in [x_delta, y_delta]
                        [0, 0] being the bottom left corner of the board
    """
    piece_name: str = ''
    piece_value: int = 0
    possible_moves: list[tuple[int, int]] = []

    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, player_color: str, color_on_top: str) -> Generator[Move, None, None]:
        """

        Args:
            board: The current chess board
            x_position: The current x position of the piece
            y_position: The current y position of the piece
            player_color: The current player's color
            color_on_top: The color of the player on the top side of the board (this is used to provide the direction of the moving piece)

        Yields: A Generator of all the possible moves a piece can do given it's current position
                 and which player has to play
            
        """
        # Raises an error if it's not implemented inside child classes
        raise NotImplementedError

    def get_resulting_boards(self, board: ChessBoard, x_position: int, y_position: int, player_color: str, color_on_top: str) -> Generator[tuple[ChessBoard, Move], None, None]:
        """

        Args:
            board: The current chess board
            x_position: The current x position of the piece
            y_position: The current y position of the piece
            player_color: The current player's color
            color_on_top: The color of the player on the top side of the board (this is used to provide the direction of the moving piece)

        Yields: A Generator of all the possible resulting boards and their corresponding move a piece can do given it's position 
                and which player has to play
            
        """
        for possible_move in self.get_possible_moves(board, x_position, y_position, player_color, color_on_top):
            new_board = ChessBoard(copy.deepcopy(board.board))
            new_board.board[possible_move.start[0]][possible_move.start[1]] = ''

            # If the possible move leads to a Queen promotion
            if possible_move.promotion:
                new_board.board[possible_move.end[0]][possible_move.end[1]] = 'q'+ player_color
            else:
                new_board.board[possible_move.end[0]][possible_move.end[1]] = self.piece_name + player_color
            yield new_board, possible_move

    def get_current_value(self) -> int:
        return self.piece_value


class LeapingPiece(ChessPiece):
    """

    This class is a subclass of the ChessPiece class representing the pieces that leaps (Knight and King)

    """
    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, player_color: str, color_on_top: str) -> Generator[Move, None, None]:
        """

        This is an overwrite of the ChessPiece get_possible_moves function
        Taking into account that the ChessPiece leaps

        """
        # Computes the direction the piece moves, based on which player is at the top of the board 
        # and the piece color
        direction: int = 1 if player_color == color_on_top else -1
        for move in self.possible_moves:
            x: int = x_position + move[0]
            y: int = y_position + move[1] * direction
            if 0 <= x < len(board.board) and 0 <= y < len(board.board[0]) and (board.board[y][x] == '' or board.board[y][x][1] != player_color):
                yield Move((y_position, x_position), (y, x))


class SlidingPiece(ChessPiece):
    """

    This class is a subclass of the ChessPiece class representing the pieces that slides (Bishop, Queen and Rock)

    """
    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, player_color: str, color_on_top: str) -> Generator[Move, None, None]:
        """
        
        This is an overwrite of the ChessPiece get_possible_moves function
        Taking into account that the ChessPiece leaps
        
        """
        # Computes the direction the piece moves, based on which player is at the top of the board 
        # and the piece color
        direction: int = 1 if player_color == color_on_top else -1
        for move in self.possible_moves:
            x, y = x_position + move[0], y_position + move[1] * direction
            while 0 <= x < len(board.board) and 0 <= y < len(board.board[0]):
                if board.board[y][x] == '':
                    yield Move((y_position, x_position), (y, x))
                elif board.board[y][x][1] != player_color:
                    yield Move((y_position, x_position), (y, x))
                    break
                else:
                    break
                x += move[0]
                y += move[1] * direction


class Pawn(ChessPiece):
    piece_name = 'p'
    piece_value = 100
    possible_moves = [(0, 1)]

    @override
    def get_possible_moves(self, board: ChessBoard, x_position: int, y_position: int, player_color: str, color_on_top: str) -> Generator[Move, None, None]:

        """

        This is an overwrite of the ChessPiece get_possible_moves function
        It couldn't be the same as the LeapingPiece one because the Pawn
        Can get prommoted and eat diagonaly but not move diagonaly without eating a piece

        """
        direction: int = 1 if player_color == color_on_top else -1
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

        # Possible eating moves
        for move in [(1, 1), (-1, 1)]:
            x: int = x_position + move[0]
            y: int = y_position + move[1] * direction

            if x < 0 or x >= len(board.board) or y < 0 or y >= len(board.board[0]):
                continue
            if board.board[y][x] != '' and board.board[y][x][1] != player_color:
                if y == promotion_row:
                    yield Move((y_position, x_position), (y, x), promotion=True)
                else:
                    yield Move((y_position, x_position), (y, x))


class King(LeapingPiece):
    piece_name = 'k'
    piece_value = 20000
    possible_moves = [(1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)]


class Queen(SlidingPiece):
    piece_name = 'q'
    piece_value = 900
    possible_moves = [(1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)]


class Knight(LeapingPiece):
    piece_name = 'n'
    piece_value = 320
    possible_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]


class Rock(SlidingPiece):
    piece_name = 'r'
    piece_value = 500
    possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Bishop(SlidingPiece):
    piece_name = 'b'
    piece_value = 330
    possible_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
