import sys
import os
import json
import uuid
from multiprocessing.dummy import Pool as ThreadPool
from PyQt6.QtWidgets import QApplication

from ChessArenaSimulation import ChessArena, ChessAppSimulation

def simulate_game(white_bot: str, black_bot: str, number_of_turns: int, time_per_turn: float, filepath: str = ""):

    if filepath:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            stats = {
                "type": "game_infos",
                "white_bot": white_bot,
                "black_bot": black_bot,
                "number_of_turns": number_of_turns,
                "time_per_turn": time_per_turn
            }
            json.dump([stats], file, indent=4)

        file.close()

    app = ChessAppSimulation()
    app.start(white_bot, black_bot, number_of_turns, time_per_turn, filepath)

if __name__ == '__main__':
    args: list[str] = sys.argv

    if len(args) == 1:
        simulate_game("minmax_stats", "random_stats", 5, 2)
    elif len(args) == 6:
        white_bot, black_bot, number_of_turns, time_per_turn, numer_of_iterations = args[1:]
        for i in range(int(numer_of_iterations)):
            game_uuid: str  = str(uuid.uuid4())
            filepath: str = f"game_stats/{white_bot}_{black_bot}_v4/{number_of_turns}_{time_per_turn}_{game_uuid}.json"
            sys.stderr.write(f"Starting game {filepath}\n")
            simulate_game(white_bot, black_bot, int(number_of_turns), float(time_per_turn), filepath)
            sys.stderr.write(f"Game finished with success: {filepath}\n")

