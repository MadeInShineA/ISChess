import random

from Bots.AB_Board import Board
from Bots.ChessBotList import register_chess_bot
from Bots.AB_Data_Class import ChessBoard, Move


def chess_bot(player_sequence, actual_board, time_budget, **kwargs):
    chess_board: ChessBoard = ChessBoard(actual_board)
    board_class: Board = Board(player_sequence[1])

    def evaluate_minmax(board: ChessBoard, depth: int, color: str, maximize: bool) -> float:
        opponent_color: str = 'w' if color == 'b' else 'b'
        if depth == 0:
            return board_class.get_current_value(board)

        if maximize:
            max_value = float('-inf')
            for new_board, _ in board_class.get_possible_boards(board, color):
                max_value = max(max_value, evaluate_minmax(new_board, depth - 1, opponent_color, False))
            return max_value + random.randint(-5, 5)
        else:
            min_value = float('inf')
            for new_board, _ in board_class.get_possible_boards(board, color):
                min_value = min(min_value, evaluate_minmax(new_board, depth - 1, opponent_color, True))
            return min_value

    def find_best_move(board: ChessBoard, depth: int, color: str) -> Move:
        opponent_color: str = 'w' if color == 'b' else 'b'
        best_value = float('-inf')
        best_move = Move((0, 0), (0, 0))
        for new_board, move in board_class.get_possible_boards(board, color):
            value = evaluate_minmax(new_board, depth - 1, opponent_color, False)
            if value > best_value:
                best_value = value
                best_move = move

        return best_move

    actual_best_move = find_best_move(chess_board, 3, player_sequence[1])
    return actual_best_move.start, actual_best_move.end

register_chess_bot("AB_BOT", chess_bot)
