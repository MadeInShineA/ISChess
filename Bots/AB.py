import random
import time

from Bots.AB_Board import Board
from Bots.ChessBotList import register_chess_bot
from Bots.AB_Data_Class import ChessBoard, Move
from Bots.AB_TimeExceededException import TimeExceededException



def chess_bot(player_sequence: str, actual_board: list[list[str]], time_budget: float, **kwargs):

    """

    Args:
        player_sequence: Game's states provided by the runner Class encoded like this [team_id|color|board_orientation]
        actual_board: The current board of the chess game represented as a list of list of char
        time_budget: The time allowed to return a move
        **kwargs: Optional extra arguments

    Returns: The move the bot wants to make in (start_y, start_x) (end_y, end_x) format
        
    """
    def evaluate_with_alpha_beta_pruning(board: ChessBoard, depth: int, alpha: float, beta: float, player_color: str, maximize: bool) -> float:
        """
            This function is an implementation of the alpha beta pruning algorithm
            see https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

        Args:
            board: The current chess board
            depth: The current depth
            alpha: The current alpha's value
            beta: The current beta's value
            color: The current player's color
            maximize: A bool representing if the current iteration wants to maximize or minimize the player's score

        Returns: The board's value for the current iteration
            
        """
        # Throws a custom exception it a timeout occurs
        if time.time() - start_time > time_budget:
            print("Time out inside evaluate_minmax")
            raise TimeExceededException

        opponent_color: str = 'w' if player_color == 'b' else 'b'
        if depth == 0:
            # Returns the current board value + a small random factor to avoid repeting positions
            return board_class.get_current_value(board) + random.uniform(-0.05, 0.05)

        if maximize:
            max_value = float('-inf')
            for new_board, _ in board_class.get_possible_boards(board, player_color):
                value = evaluate_with_alpha_beta_pruning(new_board, depth - 1, alpha, beta, opponent_color, False)
                max_value = max(max_value, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return max_value
        else:
            min_value = float('inf')
            for new_board, _ in board_class.get_possible_boards(board, player_color):
                value = evaluate_with_alpha_beta_pruning(new_board, depth - 1, alpha, beta, opponent_color, True)
                min_value = min(min_value, value)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return min_value



    def find_best_move(board: ChessBoard, depth: int, player_color: str) -> None:
        """
        This functon tries to find the best move possible using the alpha beta pruning algorithm

        Args:
            board: The current chess board
            depth: The wanted depth of the alpha beta pruning algorithm
            player_color: The current player's color

        Returns: Nothing, but updates the value of the best_move directly
            
        """
        nonlocal best_move
        opponent_color: str = 'w' if player_color == 'b' else 'b'

        # Initializes the current best_value, alpha and beta variables
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Evaluates all the possible board from the current one up to the wanted depth 
        # using the alpha beta pruning algorithm
        for new_board, move in board_class.get_possible_boards(board, player_color):
            value = evaluate_with_alpha_beta_pruning(new_board, depth - 1, alpha, beta, opponent_color, False)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, value)
        
        return

    # Initialized the chess board, the board class, the current time and the current best move variables
    chess_board: ChessBoard = ChessBoard(actual_board)
    board_class: Board = Board(player_sequence[1])
    start_time = time.time()
    best_move: Move = Move((0, 0), (0, 0))

    try:
        find_best_move(chess_board, 3, player_sequence[1])
    except TimeExceededException:
        # Stop computation if a timeout occurs
        pass
    finally:
        return best_move.start, best_move.end

register_chess_bot("Rob0 (technique la ref 🗿)", chess_bot)
