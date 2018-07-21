import requests
import json
from datetime import datetime

from app.datasets.database import Database
from app.datasets.proline import ProlineTicket, ProlineGame

class ScrapeResults(object):
    def run(self, output):
        for ticket_data in self.fetch_ticket_result_data():
            ticket = self.db.query(ProlineTickets).filter_by(handle=ticket_data['listNumber']).first()
            for game_data in ticket_data['results']:
                game = self.db.query(ProlineGames).filter_by(ticket_id=ticket.id, handle=game_data['']).first()
                game.outcomes = self.parse_outcomes(game_data['odds'])
                self.save_record(game)


    def parse_outcomes(self, raw_outcomes):
        results = []
        if raw_results['vplus'] is not None:
            results.append('v+')
        if raw_results["v"] is not None:
            results.append('v')
        if raw_results["t"] is not None:
            results.append('t')
        if raw_results["hplus"] is not None:
            results.append('h+')
        if raw_results["h"] is not None:
            results.append('h')
        return results

    def fetch_ticket_result_data(self):
        OLG_RESULTS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/results/all.jsonp?callback=_jqjsp"
        response = requests.get(OLG_RESULTS_ENDPOINT, verify=False).text
        response = response.replace('_jqjsp(', '', 1)
        response = response.replace(');', '', 1)
        return json.loads(response)['response']['results']['resultList']


class ScrapeTickets(object):
    def run(self, output):
        for ticket in self.fetch_ticket_list():
            self.create_ticket(ticket)

    def create_ticket(self, ticket_data):
        ticket_handle = int(ticket_data['listNumber'])
        ticket_date = datetime.fromtimestamp(ticket_data['listDate']/1000)

        ticket = ProlineTicket(handle=ticket_handle, date=ticket_date)

        self.save_record(ticket)
        ticket = self.db.query(ProlineGame).filter_by(handle=ticket.handle).first()

        if ticket.id != None:
            for game_data in ticket_data['eventList']:
                self.create_game(ticket, game_data)
        else:
            print('missing ticket')
            return

    def create_game(self, ticket, game_data):
        v_plus = float(game_data['odds']['vplus']) if game_data['odds']['vplus'] != None else 0.0
        v = float(game_data['odds']['v']) if game_data['odds']['v'] != None else 0.0
        t = float(game_data['odds']['t']) if game_data['odds']['t'] != None else 0.0
        h = float(game_data['odds']['h']) if game_data['odds']['h'] != None else 0.0
        h_plus = float(game_data['odds']['hplus']) if game_data['odds']['hplus'] != None else 0.0

        game = ProlineGame(
            ticket_id=ticket.id,
            handle=game_data['id'],
            cutoff_date=datetime.strptime(game_data['cutoffDate'], '%Y-%m-%d %H:%M:%S.0'),
            home=game_data['homeName'].strip(),
            visitor=game_data['visitorName'].strip(),
            sport=game_data['sport'].strip(),
            v_plus=v_plus,
            v=v,
            t=t,
            h=h,
            h_plus=h_plus
        )
        self.save_record(game)


    def fetch_ticket_list(self):
        OLG_TICKETS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/events/all.json"
        response = requests.get(OLG_TICKETS_ENDPOINT, verify=False).text
        return json.loads(response)['events']['eventList']
