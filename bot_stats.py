import json
from os import waitid_result
   
if __name__ == "__main__":

    with open("game_stats.json", "r") as file:

        matchup_stats = json.load(file)


    bots = ["random", "minmax", "pruning"]
    wanted_values = ["0.5", "1.0", "1.5", "2.0", "total"]
    wanted_metrics = ["number_of_evaluations", "timeouts", "turns_played", "number_of_games"]
    wanted_results = {bot: {wanted_metric: {wanted_time: 0 for wanted_time in wanted_values} for wanted_metric in wanted_metrics} for bot in bots}
    

    for bot in bots:
        for matchup_name, matchup_stat in matchup_stats.items():
            if isinstance(matchup_stat, dict):
                for key, values in matchup_stat.items():
                    if key.endswith(bot + "_stats"):
                        for metric, values_ in values.items():
                            for time, values__ in values_.items():
                                if metric in wanted_metrics and time in wanted_values:
                                    wanted_results[bot][metric][time] += values__
                    if key in wanted_metrics and bot in matchup_name:
                        for time, value in values.items():
                            if time in wanted_values:
                                wanted_results[bot][key][time] += value
    new_metrics = {"number_of_evaluations_per_move": "number_of_evaluations", "timeout_frequency": "timeouts"}
    for bot in bots:
        for new_metric, existing_metric in new_metrics.items():
            wanted_results[bot][new_metric] = {}
            for wanted_value in wanted_values:
                wanted_results[bot][new_metric][wanted_value] = 0
                wanted_results[bot][new_metric][wanted_value] += wanted_results[bot][existing_metric][wanted_value]
                wanted_results[bot][new_metric][wanted_value] /= wanted_results[bot]["turns_played"][wanted_value]

    with open("bot_stats.json", "w") as file:
        json.dump(wanted_results, file, sort_keys=True, indent=4)

