import pytest
import pandas as pd
from dataland.dataset import read

from projects.sports_betting.jobs.build_training_set import BuildTrainingSet

@pytest.fixture
def nba_games():
    return read('projects/sports_betting/data/nba_games').head()

@pytest.fixture
def nba_standings():
    return read('projects/sports_betting/data/nba_standings').head()

class TestBuildTrainingSet(object):
    def test_seven_day_stats(self):
        input_stats = pd.DataFrame({
            'date': ['2017-10-01','2017-10-02','2017-10-03','2017-10-04','2017-10-05','2017-10-06','2017-10-07'],
            'team_name': ['team','team','team','team','team','team','team'],
            'games': [1,2,3,4,5,6,7],
            'minutes': [240, 480, 720, 960, 1200, 1440, 1680],
            'field_goals': [97, 184, 287, 398, 495, 592, 692],
            'field_goal_attempts': [147, 234, 347, 428, 535, 622, 722],
            'field_goal_percentage': [0.6597, 0.786, 0.827, 0.9297, 0.9253, 0.9517, 0.9585],
            'three_points': [97, 184, 287, 398, 495, 592, 692],
            'three_point_attempts': [147, 234, 347, 428, 535, 622, 722],
            'three_point_percentage': [0.6597, 0.786, 0.827, 0.9297, 0.9253, 0.9517, 0.9585],
            'two_points': [97, 184, 287, 398, 495, 592, 692],
            'two_point_attempts': [147, 234, 347, 428, 535, 622, 722],
            'two_point_percentage': [0.6597, 0.786, 0.827, 0.9297, 0.9253, 0.9517, 0.9585],
            'free_throws': [97, 184, 287, 398, 495, 592, 692],
            'free_throw_attempts': [147, 234, 347, 428, 535, 622, 722],
            'free_throw_percentage': [0.6597, 0.786, 0.827, 0.9297, 0.9253, 0.9517, 0.9585],
            'offensive_rebounds': [7, 14, 21, 28, 35, 42, 49],
            'defensive_rebounds': [7, 14, 21, 28, 35, 42, 49],
            'total_rebounds': [14, 28, 42, 56, 70, 84, 98],
            'assists': [7, 14, 21, 28, 35, 42, 49],
            'steals': [7, 14, 21, 28, 35, 42, 49],
            'turn_overs': [7, 14, 21, 28, 35, 42, 49],
            'personal_fouls': [7, 14, 21, 28, 35, 42, 49],
            'points': [40, 80, 120, 160, 200, 240, 280]
        })

        expected_output = pd.DataFrame({
            'date': ['2017-10-07'],
            'team_name': ['team'],
            'field_goals_per_game': input_stats['field_goals'].max() / 7.0,
            'field_goal_attempts_per_game': input_stats['field_goal_attempts'].max() / 7.0,
            'field_goal_attempts_per_game': input_stats['field_goal_attempts'].max() / 7.0,
            'field_goal_attempts_per_game': input_stats['field_goal_attempts'].max() / 7.0,
        })

        assert expected_output == BuildTrainingSet().seven_day_stats(input_stats)
