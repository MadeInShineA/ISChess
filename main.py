from Bots.AB_Board import Board

from PyQt6.QtWidgets import QApplication

from ChessArena import ChessArena, ChessApp


if __name__ == '__main__':

    import sys
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)

    sys.excepthook = except_hook

    app = ChessApp()
    app.start()
    """
    board = Board('w')
    print(board.decode_from_fen("r3k1nr/1b1p1p1p/p1pNp1p1/1p3q2/8/PB1PPN2/1PK2PPP/R1B4R", 'w'))
    """
