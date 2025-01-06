from dataclasses import dataclass

@dataclass
class Move:
    """ This class serves as an abstraction of a chess Move

    Attributes: 
        start: The start position of the move in (y_start_position, x_start_position) format
        end: The end position of the move in (y_end_position, x_end_position) format
        promotion: A bool representing if the move results into a piece's promotion
    """
    start: tuple[int, int]
    end: tuple[int, int]
    promotion: bool = False

@dataclass
class ChessBoard:
    """ This class serves as an abstraction of the chess board

    Attributes: 
        board: The chess board as a list of list of char
    """
    board: list[list[str]]
