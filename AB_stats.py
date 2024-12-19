
from multiprocessing.dummy import Pool as ThreadPool
from PyQt6.QtWidgets import QApplication

from ChessArenaSimulation import ChessArena, ChessAppSimulation

def simulate_game(white_bot: str, black_bot: str):
    app = ChessAppSimulation()
    app.start(white_bot, black_bot, 10)

if __name__ == '__main__':
    pool = ThreadPool(4)

    simulate_game("AB_BOT", "AB_BOT")


