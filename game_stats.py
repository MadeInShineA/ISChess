import json
import math
import os

def analyse_file(filepath: str) -> dict[str, dict[str, str | int | bool]]:
      with open(filepath, 'r') as file:
        data = json.load(file)

        game_infos = data[0]
        turns_infos = data[1:-1]
        end_game_infos = data[-1]

        number_of_turns = game_infos["number_of_turns"]
        time_per_turn = game_infos["time_per_turn"]

        winner = end_game_infos["winner"]

        if winner != "none":
            if end_game_infos["checkmate"]:
                winner = ("black_" if end_game_infos["number_of_turns"] % 2 == 0 else "white_") + winner
            else:
                white_pieces = end_game_infos["white_pieces"]
                black_pieces = end_game_infos["black_pieces"]
                winner = ("white_" if white_pieces > black_pieces else "black_") + winner

        position_before_last_move = turns_infos[-1]["board_before_move"]
        position_after_last_move = turns_infos[-1]["board_after_move"]

        end_game_infos.update({"maximum_number_of_turns": number_of_turns, "time_per_turn": time_per_turn, "winner": winner, "position_before_last_move": position_before_last_move, "position_after_last_move": position_after_last_move})
        end_game_infos.pop("type")

        white_bot = game_infos["white_bot"]
        black_bot = game_infos["black_bot"]

        metrics = {
            "white_" + white_bot: {
                "total_number_of_timeouts": 0,
                "total_time_spent_computing": 0
            },
            "black_" + black_bot: {
                "total_number_of_timeouts": 0,
                "total_time_spent_computing": 0
            },
            "game_stats": end_game_infos
        }


        for index, play_stat in enumerate(turns_infos):

            bot_name = play_stat["bot"]
            metric_category = "white_" + bot_name if index % 2 == 0 else "black_" + bot_name
            
            metrics[metric_category]["total_number_of_timeouts"] += play_stat["is_timeout"]
            metrics[metric_category]["total_time_spent_computing"] += play_stat["elapsed_time"]

            if bot_name == "random_stats":
                pass
            else:
                metrics[metric_category].setdefault("total_number_of_evaluations", 0)
                if bot_name == "pruning_stats":
                    metrics[metric_category].setdefault("total_number_of_branches_cut", 0)
                    metrics[metric_category]["total_number_of_branches_cut"] += play_stat["number_of_branches_cut"]

                metrics[metric_category]["total_number_of_evaluations"] += play_stat["number_of_evaluation"]
        
        return metrics

if __name__ == '__main__':
    base_path = 'game_stats'
    game_stats_version = 4

    matchup_stats = {}

    for root, dirs, files in os.walk(base_path):
        if "v" + str(game_stats_version)  in root:
            for file in files:
                path = os.path.join(root, file)
                metrics = analyse_file(path)
                
                white_bot, black_bot = list(metrics.keys())[0:2]
                matchup_stat = f"{white_bot} vs {black_bot}"

                matchup_stats.setdefault("total_number_of_games", 0)
                matchup_stats["total_number_of_games"] += 1

                matchup_stats.setdefault(matchup_stat, {})
                matchup_stats[matchup_stat].setdefault(white_bot + "_wins", {})
                matchup_stats[matchup_stat].setdefault(black_bot + "_wins", {})
                matchup_stats[matchup_stat].setdefault("draws", {})
                matchup_stats[matchup_stat].setdefault("number_of_turns", {"total": 0})
                matchup_stats[matchup_stat].setdefault("number_of_games", {"total": 0})

                game_stats = metrics["game_stats"]
                time_per_turn = str(game_stats["time_per_turn"])

                matchup_stats[matchup_stat]["number_of_games"].setdefault(time_per_turn, 0)
                matchup_stats[matchup_stat]["number_of_games"][time_per_turn] += 1
                matchup_stats[matchup_stat]["number_of_games"]["total"] += 1

                matchup_stats[matchup_stat]["number_of_turns"].setdefault(time_per_turn, 0)
                matchup_stats[matchup_stat]["number_of_turns"][time_per_turn] += game_stats["number_of_turns"]
                matchup_stats[matchup_stat]["number_of_turns"]["total"] += game_stats["number_of_turns"]

                
                winner = game_stats["winner"]

                matchup_stats[matchup_stat][white_bot + "_wins"].setdefault("total", 0)
                matchup_stats[matchup_stat][white_bot + "_wins"].setdefault(time_per_turn, {"checkmate": 0, "pieces": 0, "total": 0})

                matchup_stats[matchup_stat][black_bot + "_wins"].setdefault(time_per_turn, {"checkmate": 0, "pieces": 0, "total": 0})
                matchup_stats[matchup_stat][black_bot + "_wins"].setdefault("total", 0)

                matchup_stats[matchup_stat]["draws"].setdefault(time_per_turn, {"stalemate": 0, "pieces": 0, "total": 0})
                matchup_stats[matchup_stat]["draws"].setdefault("total", 0)

                if winner == "none":

                    matchup_stats[matchup_stat]["draws"]["total"] += 1
                    matchup_stats[matchup_stat]["draws"][time_per_turn]["total"] += 1

                    if game_stats["stalemate"]:
                        matchup_stats[matchup_stat]["draws"][time_per_turn]["stalemate"] += 1
                    else:
                        matchup_stats[matchup_stat]["draws"][time_per_turn]["pieces"] += 1
                elif winner == white_bot:
                    matchup_stats[matchup_stat][white_bot + "_wins"]["total"] += 1
                    matchup_stats[matchup_stat][white_bot + "_wins"][time_per_turn]["total"] += 1
                    if game_stats["checkmate"]:
                        matchup_stats[matchup_stat][white_bot + "_wins"][time_per_turn]["checkmate"] += 1
                    else:
                        matchup_stats[matchup_stat][white_bot + "_wins"][time_per_turn]["pieces"] += 1
                elif winner == black_bot:
                    matchup_stats[matchup_stat][black_bot + "_wins"]["total"] += 1
                    matchup_stats[matchup_stat][black_bot + "_wins"][time_per_turn]["total"] += 1
                    if game_stats["checkmate"]:
                        matchup_stats[matchup_stat][black_bot + "_wins"][time_per_turn]["checkmate"] += 1
                    else:
                        matchup_stats[matchup_stat][black_bot + "_wins"][time_per_turn]["pieces"] += 1

                for bot in white_bot, black_bot:
                    
                    matchup_bot_default = metrics[bot].copy()
                    
                    matchup_bot_default.pop("total_number_of_timeouts", None)
                    matchup_bot_default.pop("total_number_of_evaluations", None)
                    matchup_bot_default.pop("total_time_spent_computing", None)
                    matchup_bot_default.pop("total_number_of_branches_cut", None)

                    matchup_stats[matchup_stat].setdefault(bot, matchup_bot_default.copy())
                    matchup_stats[matchup_stat][bot].setdefault("timeouts", {"total": 0})
                    matchup_stats[matchup_stat][bot]["timeouts"].setdefault(time_per_turn, 0)

                    matchup_stats[matchup_stat][bot]["timeouts"]["total"] += metrics[bot]["total_number_of_timeouts"]
                    matchup_stats[matchup_stat][bot]["timeouts"][time_per_turn] += metrics[bot]["total_number_of_timeouts"]

                    matchup_stats[matchup_stat][bot].setdefault("time_spent_computing", {"total": 0})
                    matchup_stats[matchup_stat][bot]["time_spent_computing"].setdefault(time_per_turn, 0)

                    matchup_stats[matchup_stat][bot]["time_spent_computing"]["total"] += metrics[bot]["total_time_spent_computing"]
                    matchup_stats[matchup_stat][bot]["time_spent_computing"][time_per_turn] += metrics[bot]["total_time_spent_computing"]

                    matchup_stats[matchup_stat][bot].setdefault("turns_played", {"total": 0})

                    matchup_stats[matchup_stat][bot]["turns_played"].setdefault(time_per_turn, 0)

                    turns_played = math.ceil(game_stats["number_of_turns"] / 2.0) if bot == white_bot else math.floor(game_stats["number_of_turns"]/ 2.0)
                    matchup_stats[matchup_stat][bot]["turns_played"][time_per_turn] += turns_played
                    matchup_stats[matchup_stat][bot]["turns_played"]["total"] += turns_played


                    
                    if "total_number_of_evaluations" in metrics[bot].keys():
                        matchup_stats[matchup_stat][bot].setdefault("number_of_evaluations", {"total": 0})
                        matchup_stats[matchup_stat][bot]["number_of_evaluations"].setdefault(time_per_turn, 0)

                        matchup_stats[matchup_stat][bot]["number_of_evaluations"]["total"] += metrics[bot]["total_number_of_evaluations"]
                        matchup_stats[matchup_stat][bot]["number_of_evaluations"][time_per_turn] += metrics[bot]["total_number_of_evaluations"]

                    if "total_number_of_branches_cut" in metrics[bot].keys():
                        matchup_stats[matchup_stat][bot].setdefault("branches_cut", {"total": 0})
                        matchup_stats[matchup_stat][bot]["branches_cut"].setdefault(time_per_turn, 0)

                        matchup_stats[matchup_stat][bot]["branches_cut"]["total"] += metrics[bot]["total_number_of_branches_cut"]
                        matchup_stats[matchup_stat][bot]["branches_cut"][time_per_turn] += metrics[bot]["total_number_of_branches_cut"]


                        

                    for metric, value in matchup_bot_default.items():
                        matchup_stats[matchup_stat][bot][metric] += value


    with open("stats/game_stats.json", "w") as file:
        json.dump(matchup_stats, file, sort_keys=True, indent=4)


