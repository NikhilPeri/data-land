import requests
import json
from datetime import datetime

from dataland.scheduler import AppendOperation


class ScrapeOdds(AppendOperation):
    INPUT = 'data/proline/odds.csv'

    def new_records(self):
        odds = self.get_template()

        for ticket in self.fetch_ticket_list():
            ticket_handle = int(ticket['listNumber'])
            for game in ticket['eventList']:
                record = {
                    'ticket_handle': ticket_handle,
                    'game_handle': int(game['id']),
                    'h_plus': float(game['odds']['hplus']) if game['odds']['hplus'] != None else 0.0,
                    'h': float(game['odds']['h']) if game['odds']['h'] != None else 0.0,
                    't': float(game['odds']['t']) if game['odds']['t'] != None else 0.0,
                    'v': float(game['odds']['v']) if game['odds']['v'] != None else 0.0,
                    'v_plus': float(game['odds']['vplus']) if game['odds']['vplus'] != None else 0.0,
                    'home': game['homeName'].strip(),
                    'visitor': game['visitorName'].strip(),
                    'cutoff_date': datetime.strptime(game['cutoffDate'], '%Y-%m-%d %H:%M:%S.0'),
                    'sport': game['sport'].strip()
                }
                odds = odds.append(record, ignore_index=True)

        return odds

    def fetch_ticket_list(self):
        OLG_TICKETS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/events/all.json"
        response = requests.get(OLG_TICKETS_ENDPOINT, verify=False).text
        return json.loads(response)['events']['eventList']

class ScrapeResults(AppendOperation):
    INPUT = 'data/proline/results.csv'

    def new_records(self):
        results = self.get_template()

        for ticket in self.fetch_ticket_results():
            ticket_handle = int(ticket['listNumber'])
            for game in ticket['results']:
                record = {
                    'ticket_handle': ticket_handle,
                    'game_handle': int(game['id']),
                    'outcome_h_plus': 1 if game['odds']['hplus'] != None else 0,
                    'outcome_h': 1 if game['odds']['h'] != None else 0,
                    'outcome_t': 1 if game['odds']['t'] != None else 0,
                    'outcome_v': 1 if game['odds']['v'] != None else 0,
                    'outcome_v_plus': 1 if game['odds']['vplus'] != None else 0,
                }
                results = results.append(record, ignore_index=True)

        return results

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

    def fetch_ticket_results(self):
        OLG_RESULTS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/results/all.jsonp?callback=_jqjsp"
        response = requests.get(OLG_RESULTS_ENDPOINT, verify=False).text
        response = response.replace('_jqjsp(', '', 1)
        response = response.replace(');', '', 1)
        return json.loads(response)['response']['results']['resultList']
