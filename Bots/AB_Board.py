from Bots.AB_Data_Class import ChessBoard, Move
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
        res = 0
        for y, row in enumerate(board.board):
            for x, square in enumerate(row):
                if square:
                    square_piece = square[0]
                    square_color = square[1]
                    value = self.piece_dictionary[square_piece].get_current_value(x, y)
                    res += value if square_color == self.color_on_top else -value
        return res

    def get_possible_boards(self, board: ChessBoard, color: str) -> list[tuple[ChessBoard, Move]]:
        res = []
        for y, row in enumerate(board.board):
            for x, square in enumerate(row):
                if square and square[1] == color:
                    res += self.piece_dictionary[square[0]].get_resulting_boards(board, x, y, color, self.color_on_top)
        return res
