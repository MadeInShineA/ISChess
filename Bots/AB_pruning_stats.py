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

    def evaluate_minmax_with_alpha_beta(board: ChessBoard, depth: int, alpha: float, beta: float, color: str, maximize: bool) -> float:
        nonlocal number_of_evaluation
        nonlocal number_of_branches_cut

        number_of_evaluation += 1
        if time.time() - start_time > time_budget:
            print("Time out inside evaluate_minmax")
            raise TimeExceededException

        opponent_color: str = 'w' if color == 'b' else 'b'
        if depth == 0:
            return board_class.get_current_value(board) + random.uniform(-0.05, 0.05)

        if maximize:
            max_value = float('-inf')
            for new_board, _ in board_class.get_possible_boards(board, color):
                value = evaluate_minmax_with_alpha_beta(new_board, depth - 1, alpha, beta, opponent_color, False)
                max_value = max(max_value, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    number_of_branches_cut += 1
                    break
            return max_value
        else:
            min_value = float('inf')
            for new_board, _ in board_class.get_possible_boards(board, color):
                value = evaluate_minmax_with_alpha_beta(new_board, depth - 1, alpha, beta, opponent_color, True)
                min_value = min(min_value, value)
                beta = min(beta, value)
                if beta <= alpha:
                    number_of_branches_cut += 1
                    break
            return min_value



    def find_best_move_with_alpha_beta(board: ChessBoard, depth: int, color: str) -> Move:
        nonlocal best_move
        nonlocal board_after_move
        opponent_color: str = 'w' if color == 'b' else 'b'
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for new_board, move in board_class.get_possible_boards(board, color):
            value = evaluate_minmax_with_alpha_beta(new_board, depth - 1, alpha, beta, opponent_color, False)
            if value > best_value:
                best_value = value
                best_move = move
                board_after_move = new_board
            alpha = max(alpha, value)

        return best_move


    best_move: Move = Move((0, 0), (0, 0))
    board_after_move: ChessBoard = chess_board
    number_of_evaluation: int = 0
    number_of_branches_cut: int = 0
    is_timeout: bool = False
    depth = 3
    try:
        find_best_move_with_alpha_beta(chess_board, depth, player_sequence[1])
    except TimeExceededException:
       is_timeout = True 
    finally:
        elapsed_time = time.time() - start_time
        print(f"Number of evaluation: {number_of_evaluation} in {elapsed_time}")
        print(f"Number of branches cut: {number_of_branches_cut}")

        stats: dict[str, str | int | float | bool] = {
            "bot": "prunning_stats",
            "board_before_move": board_class.encode_to_fen(chess_board),
            "board_after_move": board_class.encode_to_fen(board_after_move),

            "number_of_evaluation": number_of_evaluation,
            "number_of_branches_cut": number_of_branches_cut,
            "depth": depth,
            "elapsed_time": elapsed_time,
            "is_timeout": is_timeout
        }
        return (best_move.start, best_move.end), stats
register_chess_bot("prunning_stats", chess_bot)
