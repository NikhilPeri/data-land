import pandas as pd

class BuildTrainingSet(object):
    def __init__(self, nba_games, nba_standings):
        self.nba_games = nba_games
        self.nba_standings = nba_standings

    def apply(self):
        nba_games = self.nba_games[self.nba_games['date'] > '2017-11-01']
        for _, game in nba_games.iterrows():
            recent_standings = self.recent_standings(game['visitor'], game['date'], 7)

    def recent_standings(self, team, date, count):
        import pdb; pdb.set_trace()
        current_game_count = self.nba_standings[self.nba_standings['team_name'] == team and self.nba_standings['date'] == date]['games']
        return self.nba_standings[self.nba_standings['team_name'] == team and self.nba_standings['games'] in range(current_game_count - count, current_game_count)].unique()

if __name__ == '__main__':
    nba_games = pd.read_csv('projects/sports_betting/data/nba_games/2018-07-14-2245.csv')
    nba_standings = pd.read_csv('projects/sports_betting/data/nba_standings/2018-07-14-2245.csv')

    output = BuildTrainingSet(nba_games, nba_standings).apply()
