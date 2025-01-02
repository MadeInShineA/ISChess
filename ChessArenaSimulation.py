import json
import os

from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6 import uic

from Bots.ChessBotList import *
from ChessRules import *
from ParallelPlayer import *
from Bots import *

import numpy as np


#   Wrap up for QApplication
class ChessAppSimulation(QtWidgets.QApplication):
    def __init__(self) -> object:
        super().__init__([])

    def start(self, white_bot: str, black_bot: str, number_of_turns: int, time_per_turn: float, filepath: str):
        arena = ChessArena(white_bot, black_bot, number_of_turns, time_per_turn, filepath)
        arena.show()
        arena.start()
        arena.launch_game()
        self.exec()

#   Main window to handle the chess board
CHESS_PIECES = ["k",  "q", "n", "b", "r", "p"]
CHESS_COLOR = {"w" : [QtGui.QColor(255,255,255), QtGui.QColor(0,0,0)], "b" : [QtGui.QColor(0,0,0), QtGui.QColor(255,255,255)],
               "r" : [QtGui.QColor(200,0,0), QtGui.QColor(50,255,255)], "y" : [QtGui.QColor(200,200,0), QtGui.QColor(50,50,255)]}
COLOR_NAMES = {"w" : "White", "b":"Black", "r":"Red", "y":"Yellow"}
CHESS_PIECES_NAMES = {"k":"King", "q":"Queen", "n":"Knight", "b":"Bishop", "r":"Rook", "p":"Pawn"}
class ChessArena(QtWidgets.QWidget):
    def __init__(self,white_bot, black_bot, number_of_turns: int, time_per_turn: float, filepath):
        super().__init__()

        uic.loadUi("Data/UI.ui", self)

        #   Render for chess board
        self.chess_scene = QtWidgets.QGraphicsScene()
        self.chess_scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("white")))
        #self.chess_scene.setBackgroundBrush(QBrush(Qt6.lightGray))
        self.chessboardView.setScene(self.chess_scene)

        self.loadBoardButton.clicked.connect(self.select_and_load_board)

        self.launchGameButton.clicked.connect(self.launch_game)

        self.load_assets()

        self.current_player = None

        self.white_bot: str = white_bot
        
        self.black_bot: str = black_bot

        self.number_of_turns: int = number_of_turns

        self.turn_number: int = 0

        self.time_per_turn: float = time_per_turn

        self.filepath: str = filepath

    def write_to_file(self, data: dict[str, str | int | float]):
        if not self.filepath:
            return

        existing_data = []
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
            with open(self.filepath, 'r') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []

        existing_data.append(data)
        with open(self.filepath, 'w') as file:
            json.dump(existing_data, file, indent=4)
        file.close()

    def add_system_message(self, message):
        msg_widget = QtWidgets.QLabel(message)
        msg_widget.setWordWrap(True)
        print("[SYS]", message)
        self.systemMessagesLayout.addWidget(msg_widget)
        self.systemMessagesBox = QtWidgets.QScrollArea()
        self.systemMessagesBox.verticalScrollBar().setSliderPosition(self.systemMessagesBox.verticalScrollBar().maximum())

    #   Called to start the bot simulation
    def launch_game(self):
        self.add_system_message("# Starting new Game #")
        #   Prepare AIs

        self.players_AI = { "w" : CHESS_BOT_LIST[self.white_bot], "b" : CHESS_BOT_LIST[self.black_bot]}
        #
        # self.players_AI = {}
        # for cid, color in enumerate(self.players_AI_choice):
        #     self.players_AI[color] = CHESS_BOT_LIST[self.players_AI_choice[color].currentText()]
        #     self.add_system_message("AI #" + str(cid) + " = " + str(self.players_AI[color].__name__))

        #self.nbr_turn_to_play = int(self.maxTurnBudget.text())
        #self.time_per_turn = float(self.timeBudgetInput.text())

        self.play_next_turn()

    def play_next_turn(self):
        if self.current_player is not None:
            print("Cannot launch new turn while already processing")
            return

        if self.turn_number == self.number_of_turns:
            print("No more play to do")
            self.end_game(None)
            return

        next_player_color = self.player_order[0:3]

        #   Prepare board view
        rotated_view_board = np.rot90(self.board, int(next_player_color[2]))
        self.current_player = ParallelTurn(self.players_AI[next_player_color[1]], self.player_order, rotated_view_board, self.time_per_turn)
        self.current_player.setTerminationEnabled(True)
        self.current_player.start()

        self.turn_number += 1
        #   Timer to call
        QtCore.QTimer.singleShot(int(self.time_per_turn * 1000 * 1.05), self.end_turn)


    def end_turn(self):
        all_other_defeated = False

        if self.current_player.isRunning():
            self.current_player.terminate()
            self.add_system_message(COLOR_NAMES[self.current_player.color] + " did not end his turn")
        else:

            player_color = self.current_player.color

            next_play, stats = self.current_player.next_move

            stats["type"] = "turn_stat"
            stats["turn_number"] = self.turn_number
            self.write_to_file(stats)

            if not move_is_valid(self.player_order, next_play, self.current_player.board):
                self.add_system_message(COLOR_NAMES[player_color] + " invalid move from " + str(next_play[0]) + " to " + str(next_play[1]))
                self.end_game(None, is_stalemate = True)
                return

            self.add_system_message(COLOR_NAMES[player_color] + " moved " + CHESS_PIECES_NAMES[self.current_player.board[next_play[0][0], next_play[0][1]][0]] +
                                    " from " + str(next_play[0]) + " to " + str(next_play[1]))

            if self.current_player.board[next_play[1][0], next_play[1][1]] != '':
                self.add_system_message(COLOR_NAMES[player_color] + " captured " + COLOR_NAMES[self.current_player.board[next_play[1][0], next_play[1][1]][1]] + " " + CHESS_PIECES_NAMES[self.current_player.board[next_play[1][0], next_play[1][1]][0]])

            #   apply move
            self.current_player.board[next_play[1][0], next_play[1][1]] = self.current_player.board[next_play[0][0], next_play[0][1]]
            self.current_player.board[next_play[0][0], next_play[0][1]] = ''

            #   check for promotion
            if self.current_player.board[next_play[1][0], next_play[1][1]][0] == 'p' and next_play[1][0] == self.current_player.board.shape[0]-1:
                self.current_player.board[next_play[1][0], next_play[1][1]] = "q" + self.current_player.board[next_play[1][0], next_play[1][1]][1]

            all_other_defeated = True
            for row in self.board:
                for elem in row:
                    if len(elem) > 0 and elem[0] == 'k':
                        if int(self.player_order[self.player_order.find(elem[1])-1]) != int(self.current_player.team):
                            all_other_defeated = False

        #   Update board state
        self.current_player = None

        self.setup_board()

        #   Current player goes at the end of the play queue
        self.player_order = self.player_order[3:] + self.player_order[0:3]

        if all_other_defeated:
            self.end_game(player_color)
        else:
            self.play_next_turn()


    def end_game(self, winner, is_stalemate: bool = False):

        white_pieces_counter: int = 0
        black_pieces_counter: int = 0

        for row in self.board:
            for square in row:
                if square != '':
                    if square[1] == 'w':
                        white_pieces_counter += 1
                    else:
                        black_pieces_counter += 1


        winner_bot: None | str = None
        is_checkmate: bool = False
        if winner is None:
            if white_pieces_counter == black_pieces_counter:
                winner_bot = "none"
            else:
                if white_pieces_counter > black_pieces_counter:
                    winner_bot = self.white_bot
                else:
                    winner_bot = self.black_bot
        else:
            is_checkmate = True
            if winner == 'w':
                winner_bot = self.white_bot
            else:
                winner_bot = self.black_bot
            
        self.write_to_file({"type": "end_game_stat", "winner": winner_bot, "white_pieces": white_pieces_counter, "black_pieces": black_pieces_counter, "number_of_turns" : self.turn_number, "checkmate": is_checkmate, "stalemate": is_stalemate})
        self.close()

    def select_and_load_board(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Select board", "C:\\Users\\Louis\\Desktop\\ISChess\\Data\\maps", "Board File (*.brd)")

        if path is None:
            return
        path = path[0]

        self.board = self.load_board(path)

        if self.board is None:
            return

        self.setup_board()
        self.setup_players()

    def load_board(self, path):
        try:
            with open(path, "r") as f:
                data = f.read()

                lines = data.split("\n")
                self.player_order = lines[0]
                elems = [l.replace('--', '').split(",") for l in lines[1:]]

                #   Protection against final empty lines
                while len(elems) > 0 and len(elems[-1]) == 0:
                    del elems[-1]

                #   check lines length equals
                for l in elems:
                    if len(l) != len(elems[0]):
                        return None

                return np.array(elems, dtype='O')
        except Exception as e:
            print(e)
            return None

        return None

    def load_assets(self):
        self.white_square = QtGui.QPixmap("Data/assets/light_square.png")
        self.black_square = QtGui.QPixmap("Data/assets/dark_square.png")

        self.pieces_imgs = {}

        for p in CHESS_PIECES:
            image = QtGui.QImage("Data/assets/" + p + ".png")
            self.pieces_imgs[p] = image

    def setup_players(self):
        for i in reversed(range(self.playersList.count())):
            if self.playersList.itemAt(i).widget() is not None:
                self.playersList.itemAt(i).widget().setParent(None)

        self.players_AI_choice = {}
        for color in self.colored_piece_pixmaps:
            l = QtWidgets.QLabel("Color:"  + COLOR_NAMES[color])
            self.playersList.addWidget(l)

            choice = QtWidgets.QComboBox()

            for name in CHESS_BOT_LIST:
                choice.addItem(name, CHESS_BOT_LIST[name])
            choice.setCurrentIndex(0)

            self.players_AI_choice[color] = choice
            self.playersList.addWidget(choice)

        self.playersList.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding))

    def setup_board(self):

        for i in reversed(self.chess_scene.items()):
            self.chess_scene.removeItem((i))

        #   Maintain the pointer towards the items on the board
        self.piece_items = np.array([[None] * self.board.shape[1]]*self.board.shape[0], dtype=object)
        #   Maintain list of colored pixmap
        self.colored_piece_pixmaps = {}

        for y in range(self.board.shape[1]):
            for x in range(self.board.shape[0]):

                square_color = self.white_square if (x+y) % 2 == 0 else self.black_square
                square_item = self.chess_scene.addPixmap(square_color)
                square_item.setPos(QtCore.QPointF(square_color.size().width()*y,square_color.size().height()*x))

                if self.board[x,y] != '' and self.board[x,y] != 'XX':
                    player_piece = self.board[x,y][0]
                    player_color = self.board[x,y][1]

                    if player_color not in self.colored_piece_pixmaps:
                        self.colored_piece_pixmaps[player_color] = {}

                    if player_piece not in self.colored_piece_pixmaps[player_color]:
                        piece_img = self.pieces_imgs[player_piece]
                        copy = piece_img.copy()

                        def mix(Q1, Q2, f, a):
                            return QtGui.QColor(int(Q1.red()   * f + Q2.red()   * (1-f)),
                                                int(Q1.green() * f + Q2.green() * (1-f)),
                                                int(Q1.blue()  * f + Q2.blue()  * (1-f)), a)

                        for px in range(copy.size().width()):
                            for py in range(copy.size().height()):
                                copy.setPixelColor(px, py, mix(CHESS_COLOR[player_color][0], CHESS_COLOR[player_color][1], copy.pixelColor(px, py).red() / 255., copy.pixelColor(px, py).alpha()))

                        self.colored_piece_pixmaps[player_color][player_piece] = QtGui.QPixmap().fromImage(copy)

                    self.piece_items[x,y] = self.chess_scene.addPixmap(self.colored_piece_pixmaps[player_color][player_piece])
                    self.piece_items[x,y].setPos(QtCore.QPointF(square_color.size().width()*y,square_color.size().height()*x))

        self.chessboardView.fitInView(self.chess_scene.sceneRect())

    def start(self):
        self.board = self.load_board("Data/maps/default.brd")
        self.setup_board()
        self.setup_players()
        self.chess_scene.update()
