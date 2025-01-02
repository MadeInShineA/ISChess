from dataclasses import dataclass

@dataclass
class Move:
    start: tuple[int, int]
    end: tuple[int, int]
    promotion: bool = False

@dataclass
class ChessBoard:
    board: list[list[str]]
