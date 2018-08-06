import pandas as pd
import pytest
import responses

from datetime import datetime

from dataland.dataset import get_template
from projects.proline.scrapers import ScrapeOdds, ScrapeResults
from tests.utils import as_dicts

class TestScrapeOdds(object):

    @pytest.fixture
    def mock_odds_reponse(self):
        return {
            'lastUpdated': 1524962167748,
            'jsonCallback': None,
            'events': {
                '@class': 'com.olson.olg.proline.dataModels.dto.proline.events.ProlineEventsDTO',
                'eventList': [
                    {
                        '@class': 'com.olson.olg.proline.dataModels.dto.proline.events.ProlineEventListDTO',
                        'listDate': 1524888000000,
                        'listNumber': '2698',
                        'eventList': [
                            {
                                '@class': 'com.olson.olg.proline.dataModels.dto.proline.events.ProlineSingleEventDTO',
                                'id': '50',
                                'startTime': '07:00PM',
                                'home': 'NYM',
                                'homeName': 'NEW YORK-M                              ',
                                'visitor': 'CIN',
                                'visitorName': 'CINCINNATI                              ',
                                'sport': 'BBL',
                                'cutoffDate': '2018-08-06 19:00:00.0',
                                'note': None,
                                'eventName': None,
                                'odds': {
                                    'vplus': '2.9',
                                    'v': '2.25',
                                    't': '2.35',
                                    'h': '1.4',
                                    'hplus': '1.85',
                                    'over': '1.6',
                                    'under': '1.8',
                                    'overUnder': '7.5'
                                },
                                'status': {
                                    'closed': False,
                                    'suspended': False,
                                    'cancelled': False,
                                    'outcomeEN': None,
                                    'outcomeFR': None,
                                    'eventOutcomeEN': None,
                                    'eventOutcomeFR': None,
                                    'overUnderClosed': False,
                                    'overUnderSuspended': False,
                                    'overUnderOutcomeEN': None,
                                    'overUnderOutcomeFR': None
                                }}]}]}}

    @responses.activate
    def test_new_records_returns_odds(self, mock_odds_reponse):
        responses.add(
            responses.GET,
            'https://www.proline.ca/olg-proline-services/rest/api/proline/events/all.json',
            status=200,
            json=mock_odds_reponse)

        expected = [{
            'ticket_handle': 2698,
            'game_handle': 50,
            'sport': 'BBL',
            'visitor': 'CINCINNATI',
            'home': 'NEW YORK-M',
            'cutoff_date': pd.Timestamp('2018-08-06 19:00:00.0'),
            'h_plus': 1.85,
            'h': 1.4,
            't': 2.35,
            'v': 2.25,
            'v_plus': 2.9
        }]

        assert sorted(as_dicts(ScrapeOdds().new_records())) == sorted(expected)

class TestScrapeResults(object):

    @pytest.fixture
    def mock_results_reponse(self):
        return {
            'response': {
                'lastUpdated': 1533575002697,
                'jsonCallback': '_jqjsp',
                'results': {
                'resultList': [{
                    'type': 'PL',
                    'date': 1533441600000,
                    'listNumber': '2732',
                    'results': [
                        {
                            'id': '35',
                            'startTime': '01:00PM',
                            'home': 'NYM',
                            'homeName': 'NEW YORK-M                              ',
                            'visitor': 'ATL',
                            'visitorName': 'ATLANTA                                 ',
                            'sport': 'BBL',
                            'odds': {
                                'vplus': None,
                                'v': '1.55',
                                't': '2.6',
                                'h': None,
                                'hplus': None,
                                'over': '1.75',
                                'under': None,
                                'overUnder': '8.5'
                            },
                            'status': {
                                'closed': False,
                                'suspended': False,
                                'cancelled': False,
                                'outcomeEN': None,
                                'outcomeFR': None,
                                'eventOutcomeEN': None,
                                'eventOutcomeFR': None,
                                'overUnderClosed': False,
                                'overUnderSuspended': False,
                                'overUnderOutcomeEN': None,
                                'overUnderOutcomeFR': None
                            },
                            'note': None
                        }]}]}}}

    @responses.activate
    def test_new_records_returns_results(self, mock_results_reponse):
        responses.add(
            responses.GET,
            'https://www.proline.ca/olg-proline-services/rest/api/proline/results/all.jsonp?callback=_jqjsp',
            status=200,
            json=mock_results_reponse)

        expected = [{
            'ticket_handle': 2732,
            'game_handle': 35,
            'outcome_h_plus': 0,
            'outcome_h': 0,
            'outcome_t': 1,
            'outcome_v': 1,
            'outcome_v_plus': 0
        }]

        assert sorted(as_dicts(ScrapeResults().new_records())) == sorted(expected)
