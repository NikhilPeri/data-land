import pytest
import responses

from app.datasets.database import Database
from app.datasets.proline import ProlineGame, ProlineTicket
from app.jobs.proline.update_tickets import UpdateTickets

@pytest.yield_fixture(autouse=True)
def setup_db():
    db = Database.get_session()

    db.query(ProlineGame).delete()
    db.query(ProlineTicket).delete()
    db.commit()

    yield

@pytest.fixture
def mock_reponse():
    return {
            'lastUpdated': 1524962167748,
            'jsonCallback': None,
            'events': {
                'eventList': [
                    {
                        'listDate': 1524888000000,
                        'listNumber': '2698',
                        'eventList': [
                            {
                                'id': '36',
                                'startTime': '09:00PM',
                                'home': 'LAA',
                                'homeName': 'LA ANAHEIM                              ',
                                'visitor': 'NYY',
                                'visitorName': 'NEW YORK-Y                              ',
                                'sport': 'BBL',
                                'cutoffDate': '2018-04-28 21:00:00.0',
                                'note': None,
                                'eventName': None,
                                'odds': {
                                    'vplus': '2.1',
                                    'v': '1.65',
                                    't': '2.5',
                                    'h': '1.75',
                                    'hplus': '2.4',
                                    'over': '1.75',
                                    'under': '1.65',
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
                                }
                            }
                        ]
                    }
                ]
            }
        }

@responses.activate
def test_fetches_and_creates_new_tickets():
    responses.add(
        responses.GET,
        'https://www.proline.ca/olg-proline-services/rest/api/proline/results/all.json',
        status=200,
        json=mock_reponse)

    UpdateTickets.perform()

    db = Database.get_session()
    ticket = db.query(ProlineTickets).first()

    assert db.query(ProlineTickets).count() == 1
    assert ticket.handle == 2698
    assert ticket.date == 'hi'

@responses.activate
def test_fetches_and_creates_new_games():
    responses.add(
        responses.GET,
        'https://www.proline.ca/olg-proline-services/rest/api/proline/results/all.json',
        status=200,
        json=mock_reponse)

    UpdateTickets.perform()

    db = Database.get_session()
    game = db.query(ProlineGames).first()

    assert db.query(ProlineGames).count() == 1
    assert game.ticket_id == 1
    assert game.handle == 36
    assert game.cutoff_date == 'hi'
    assert game.home == 'LA ANAHEIM'
    assert game.visitor == 'NEW YORK-Y'
    assert game.sport == 'NEW YORK-Y'
    assert game.outcomes == ''
    assert game.v_plus == 2.1
    assert game.v == 1.65
    assert game.t == 2.5
    assert game.h == 1.75
    assert game.h_plus == 2.4
    
@responses.activate
def test_fetches_and_creates_new_games():
    responses.add(
        responses.GET,
        'https://www.proline.ca/olg-proline-services/rest/api/proline/events/all.json',
        status=200,
        json=mock_reponse())

    UpdateTickets.perform()

    db = Database.get_session()
    game = db.query(ProlineGames).first()

    assert db.query(ProlineGames).count() == 1
    assert game.ticket_id == 1
    assert game.handle == 36
    assert game.cutoff_date == 'hi'
    assert game.home == 'LA ANAHEIM'
    assert game.visitor == 'NEW YORK-Y'
    assert game.sport == 'NEW YORK-Y'
    assert game.outcomes == ''
    assert game.v_plus == 2.1
    assert game.v == 1.65
    assert game.t == 2.5
    assert game.h == 1.75
    assert game.h_plus == 2.4
