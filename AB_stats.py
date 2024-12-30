import sys
import json
import uuid
from multiprocessing.dummy import Pool as ThreadPool
from PyQt6.QtWidgets import QApplication

from ChessArenaSimulation import ChessArena, ChessAppSimulation

def simulate_game(white_bot: str, black_bot: str, number_of_turns: int, time_per_turn: float, filepath: str = ""):

    with open(filepath, 'w') as file:
        json.dump([], file, indent=4)

    file.close()

    app = ChessAppSimulation()
    app.start(white_bot, black_bot, number_of_turns, time_per_turn, filepath)

if __name__ == '__main__':
    args: list[str] = sys.argv

    if len(args) == 1:
        for i in range(5):
            simulate_game("minmax_stats", "prunning_stats", 5, 2)
    elif len(args) == 5:
        white_bot, black_bot, number_of_turns, time_per_turn = args[1:]
        uuid: str  = str(uuid.uuid4())
        filepath: str = f"game_stats/{white_bot}_{black_bot}_{number_of_turns}_{time_per_turn}_{uuid}.json"
        simulate_game(white_bot, black_bot, int(number_of_turns), float(time_per_turn), filepath)

