import random
import time

from Bots.AB_Board import Board
from Bots.ChessBotList import register_chess_bot
from Bots.AB_Data_Class import ChessBoard, Move
from Bots.AB_TimeExceededException import TimeExceededException 

def chess_bot(player_sequence, actual_board, time_budget, **kwargs):
    chess_board: ChessBoard = ChessBoard(actual_board)
    board_class: Board = Board(player_sequence[1])

    start_time = time.time()

    def evaluate_minmax(board: ChessBoard, depth: int, color: str, maximize: bool) -> float:
        if time.time() - start_time > time_budget:
            print("Time out inside evaluate_minmax")
            raise TimeExceededException
        opponent_color: str = 'w' if color == 'b' else 'b'
        if depth == 0:
            board_value = board_class.get_current_value(board)
            random_factor = random.uniform(-0.05, 0.05)
            return board_value + random_factor

        if maximize:
            max_value = float('-inf')
            for new_board, _ in board_class.get_possible_boards(board, color):
                max_value = max(max_value, evaluate_minmax(new_board, depth - 1, opponent_color, False))
            return max_value 
        else:
            min_value = float('inf')
            for new_board, _ in board_class.get_possible_boards(board, color):
                min_value = min(min_value, evaluate_minmax(new_board, depth - 1, opponent_color, True))
            return min_value

    def find_best_move(board: ChessBoard, depth: int, color: str) -> Move:
        opponent_color: str = 'w' if color == 'b' else 'b'
        best_value = float('-inf')
        nonlocal best_move

        for new_board, move in board_class.get_possible_boards(board, color):
            value = evaluate_minmax(new_board, depth - 1, opponent_color, False)
            if value > best_value:
                best_value = value
                best_move = move

        return best_move

    best_move = Move((0, 0), (0, 0))
    try:
        find_best_move(chess_board, 3, player_sequence[1])
    except TimeExceededException:
        pass
    finally:
        return best_move.start, best_move.end

register_chess_bot("AB_minmax", chess_bot)
