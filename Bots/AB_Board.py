from Bots.AB_Data_Class import ChessBoard, Move
import sys
import numpy as np
from Bots.AB_Chess_Piece import ChessPiece, King, Queen, Bishop, Knight, Rock, Pawn

class Board:
    """

    Attributes: 
        piece_dictionary: A dictionary containing a mapping of the grid piece char to the corresponding ChessPiece class
        color_on_top: The color at the top of the board array when creating the class
    """
    piece_dictionary: dict[str, ChessPiece] = {
        'k': King(), 'n': Knight(), 'p': Pawn(),
        'r': Rock(), 'b': Bishop(), 'q': Queen()
    }

    color_on_top: str

    def __init__(self, color_on_top: str):
        self.color_on_top = color_on_top

    def get_current_value(self, board: ChessBoard) -> int:
        """

        Args:
            board: The board to evaluate

        Returns: The value of the current board
            
        """

        # This bool is used to assure the king safety
        is_king_on_board: bool = False

        res = 0

        # This loop iterates through the squares of the board
        # And updates the res variable according to the ChessPiece current value
        for y, row in enumerate(board.board):
            for x, square in enumerate(row):
                if square:
                    square_piece = square[0]
                    square_color = square[1]
                    if square_piece == 'k' and square_color == self.color_on_top:
                        is_king_on_board = True
                    value = self.piece_dictionary[square_piece].get_current_value()
                    res += value if square_color == self.color_on_top else - value

        # If the king isn't on the board, it returns the maximum negative value possible
        if not is_king_on_board:
            return - sys.maxsize - 1
        return res

    def get_possible_boards(self, board: ChessBoard, player_color: str) -> list[tuple[ChessBoard, Move]]:
        """

        Args:
            board: The starting board
            player_color: The color char of the next player to make a move on the board

        Returns: A list of Tuple representing all the possible chess boards and their corresponding move
                 after a move from a certain player
            
        """
        res = []
        for y, row in enumerate(board.board):
            for x, square in enumerate(row):
                if square and square[1] == player_color:
                    res += self.piece_dictionary[square[0]].get_resulting_boards(board, x, y, player_color, self.color_on_top)
        return res

    def encode_to_fen(self, board: ChessBoard) -> str:

        """

        Args:
            board: The board to encode to fen notation

        Returns: a String of the board encoded to FEN notation
            
        """
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
    
    
    def decode_from_fen(self, fen_position: str, color_on_top: str) -> ChessBoard:
        """

        Args:
            fen_position: The FEN string of the current board position
            color_on_top: The color on top of the board

        Returns: A ChessBoard containing the decoded FEN position as it's board
            
        """
        piece_mapping = {
            'R': 'rw', 'N': 'nw', 'B': 'bw', 'Q': 'qw', 'K': 'kw', 'P': 'pw',
            'r': 'rb', 'n': 'nb', 'b': 'bb', 'q': 'qb', 'k': 'kb', 'p': 'pb',
        }

        board_rows = fen_position.split('/')
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
