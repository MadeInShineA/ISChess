import random

#
#   Example function to be implemented for
#       Single important function is next_best
#           color: a single character str indicating the color represented by this bot ('w' for white)
#           board: a 2d matrix containing strings as a descriptors of the board '' means empty location "XC" means a piece represented by X of the color C is present there
#           budget: time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs, ys moving to xd, yd
#

from PyQt6 import QtCore

from Bots.AB import King, Pawn, Knight, Rock, Bishop, Queen
#   Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot

#   Simply move the pawns forward and tries to capture as soon as possible


piece_list = [King(), Pawn(), Knight(), Rock(), Bishop(), Queen()]
def chess_bot(player_sequence, board, time_budget, **kwargs):

    print(board)
    color = player_sequence[1]
    print(f"Color: {color}")
    moves = []
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            for piece in piece_list:
                if board[y,x] == piece.piece_name + color:
                    for move in piece.get_possible_moves(board, x, y, color):
                        moves.append(move)
    return random.choice(moves)

#   Example how to register the function
register_chess_bot("TestBot", chess_bot)

