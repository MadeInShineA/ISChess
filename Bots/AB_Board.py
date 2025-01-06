from Bots.AB_Data_Class import ChessBoard, Move
import sys
import numpy as np
from Bots.AB_Chess_Piece import King, Queen, Bishop, Knight, Rock, Pawn

class Board:
    piece_dictionary = {
        'k': King(), 'n': Knight(), 'p': Pawn(),
        'r': Rock(), 'b': Bishop(), 'q': Queen()
    }

    color_on_top: str

    def __init__(self, color_on_top: str):
        self.color_on_top = color_on_top

    def get_current_value(self, board: ChessBoard) -> int:
        is_king_on_board: bool = False
        res = 0
        for y, row in enumerate(board.board):
            for x, square in enumerate(row):
                if square:
                    square_piece = square[0]
                    square_color = square[1]
                    if square_piece == 'k' and square_color == self.color_on_top:
                        is_king_on_board = True
                    value = self.piece_dictionary[square_piece].get_current_value(x, y)
                    res += value if square_color == self.color_on_top else - value

        if not is_king_on_board:
            return - sys.maxsize - 1
        return res

    def get_possible_boards(self, board: ChessBoard, color: str) -> list[tuple[ChessBoard, Move]]:
        res = []
        for y, row in enumerate(board.board):
            for x, square in enumerate(row):
                if square and square[1] == color:
                    res += self.piece_dictionary[square[0]].get_resulting_boards(board, x, y, color, self.color_on_top)
        return res

    def encode_to_fen(self, board: ChessBoard) -> str:

        board_to_encode = board.board.copy()
        if self.color_on_top == 'w':
            board_to_encode = np.rot90(np.rot90(board_to_encode))

        piece_mapping = {
            'rw': 'R', 'nw': 'N', 'bw': 'B', 'qw': 'Q', 'kw': 'K', 'pw': 'P',
            'rb': 'r', 'nb': 'n', 'bb': 'b', 'qb': 'q', 'kb': 'k', 'pb': 'p',
            '': ''
        }


        fen_rows = []
        for row in board_to_encode:
            fen_row = []
            empty_count = 0
            for square in row:
                if square == '':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row.append(str(empty_count))
                        empty_count = 0
                    fen_row.append(piece_mapping[square])
            if empty_count > 0:
                fen_row.append(str(empty_count))
            fen_rows.append(''.join(fen_row))
        
        fen_position = '/'.join(fen_rows)
        return fen_position
    
    
    def decode_from_fen(self, fen: str, color_on_top: str) -> ChessBoard:
        piece_mapping = {
            'R': 'rw', 'N': 'nw', 'B': 'bw', 'Q': 'qw', 'K': 'kw', 'P': 'pw',
            'r': 'rb', 'n': 'nb', 'b': 'bb', 'q': 'qb', 'k': 'kb', 'p': 'pb',
        }

        board_rows = fen.split('/')
        board = []

        for row in board_rows:
            board_row = []
            for char in row:
                if char.isdigit():
                    board_row.extend(['--'] * int(char))
                else:
                    board_row.append(piece_mapping[char])
            board.append(board_row)

        board_array = np.array(board, dtype=object)

        if color_on_top == 'w':
            board_array = np.rot90(np.rot90(board_array))

        return ChessBoard(board=board_array)



