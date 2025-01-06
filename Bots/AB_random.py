

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

    possible_moves = []

    try:
        for new_board, possible_move in board_class.get_possible_boards(chess_board, player_sequence[1]):
            if time.time() - start_time > time_budget:
                raise TimeExceededException

            possible_moves.append(possible_move)


    except TimeExceededException:
        pass
    finally:
        elapsed_time = time.time() - start_time
        print(f"Number of possible moves: {len(possible_moves)} in {elapsed_time}")
        if possible_moves:
            selected_move = random.choice(possible_moves)

        else:
            selected_move = Move((0, 0), (0, 0))
        return selected_move.start, selected_move.end

register_chess_bot("AB_random", chess_bot)
