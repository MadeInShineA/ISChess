import random

#
#   Example function to be implemented for
#       Single important function is next_best
#           color: a single character str indicating the color represented by this bot ('w' for white)
#           board: a 2d matrix containing strings as a descriptors of the board '' means empty location "XC" means a piece represented by X of the color C is present there
#           budget: time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs, ys moving to xd, yd
#

from PyQt6 import QtCore

from Bots.AB import Board, ChessBoard, Move
#   Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot

#   Simply move the pawns forward and tries to capture as soon as possible


chess_board = Board()
def chess_bot(player_sequence, board, time_budget, **kwargs):

    color = player_sequence[1]
    print(f"Color: {color}")

    converted_board = ChessBoard(board)
    board_value = chess_board.get_current_value(converted_board, color)
    print(f"Board value: {board_value}")

    possible_boards: list[tuple[ChessBoard, Move]] = chess_board.get_possible_boards(converted_board, color)

    moves = []
    for possible_board, move in possible_boards:
        moves.append(move)

    chosen_move = random.choice(moves)

    return chosen_move.start, chosen_move.end

#   Example how to register the function
register_chess_bot("TestBot", chess_bot)

