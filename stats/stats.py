from collections import defaultdict
import datetime

def is_turn_based(game):
    return game.duration >= datetime.timedelta(hours=8)

class Stats():
    def __init__(self, games) -> None:
        self.games = games

        self.number_of_games = len(games)
        self.different_games_count = 0
        self.different_games = set()
        self.total_time_played = datetime.timedelta(0)
        self.total_time_by_date = defaultdict(datetime.timedelta)
        self.total_time_by_game = defaultdict(datetime.timedelta)

        for game in games:
            self.__update_stats(game)

    def __update_stats(self, game):
        self.different_games.add(game.game_name)
        self.different_games_count = len(self.different_games)
        # Do not count games that are more than 8h long as those most likely are turn-based games
        if not is_turn_based(game):
            self.total_time_played += game.duration
        self.total_time_by_date[game.start.date().strftime('%Y-%m-%d')] += game.duration
        self.total_time_by_game[game.pretty_game_name] += game.duration
        # self.total_time_by_date[game.start.timestamp()] += game.duration

    def get_total_time_by_date_json(self):
        def get_epoch_time(date_str):
            return int(datetime.datetime.strptime(date_str, '%Y-%m-%d').timestamp())
        return {str(get_epoch_time(date)): self.total_time_by_date[date].total_seconds()/60 for date in self.total_time_by_date}

    def get_games_by_date(self):
        ret = {}
        for game in self.games:
            day_date_str = str(game.start.date().strftime('%Y-%m-%d'))
            day_date_str = f'{day_date_str}T03:00:00.000Z'
            if day_date_str not in ret:
                ret[day_date_str] = {}
            if 'details' not in ret[day_date_str]:
                 ret[day_date_str]['details'] = []
            if 'total' not in ret[day_date_str]:
                ret[day_date_str]['total'] = 0
            
            # For turn based games, use a default value of 5min to distortions on the visualization
            normalized_duration = 300 if is_turn_based(game) else game.duration.total_seconds()
            ret[day_date_str]['details'].append({"name": game.pretty_game_name, "date": str(game.start.isoformat()), "value": normalized_duration})
            ret[day_date_str]['total'] += normalized_duration

        correct_ret = []
        for item in ret.keys():
            correct_ret.append({'date': item, 'details': ret[item]['details'], 'total': ret[item]['total']})
        return correct_ret

    def get_normalized_time_by_game(self):
        return [{'text': game, "size": int(self.total_time_by_game[game].total_seconds()/500)} for game in self.total_time_by_game.keys()]