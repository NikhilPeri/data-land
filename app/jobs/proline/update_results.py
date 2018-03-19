import os
import requests
import json
from datetime import datetime


from sqlalchemy import MetaData, create_engine

class UpdateProlineResults(object):
    def perform(self):
        for ticket_data in self.fetch_ticket_result_data():
            ticket_id = #TODO
            for game_data in ticket_data['results']:
                game_id = #TODO
                outcomes = self.parse_results(game_data['odds'])
                if outcomes != []:


    def parse_results(self, raw_results):
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

if __name__ == '__main__':
    UpdateProlineResults().perform()
