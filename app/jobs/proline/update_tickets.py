from datetime import datetime

import requests
import json
import time

class UpdateTickets(object):
    def process():
        for ticket in fetch_ticket_list():
            create_ticket(ticket)

    def create_ticket(ticket_data):
        ticket_id = int(ticket_data['listNumber'])
        ticket_date = datetime.fromtimestamp(ticket_data['listDate']/1000)

        for game_data in ticket_data['eventList']:
            create_game(ticket_id, game_data)

    def create_game(ticket_id, game_data):
        game_id = game_data['id']
        cuttoff_date = datetime.strptime(game_data['cutoffDate'], '%Y-%m-%d %H:%M:%S.0')
        home_symbol = game_data['home']
        visitor_symbol = game_data['visitor']
        home_name = game_data['homeName']
        visitor_name = game_data['visitorName']
        sport = game_data['sport']
        v_plus = game_data['vplus']
        v = game_data['v']
        h = game_data['h']
        h_plus = game_data['hplus']


    def fetch_ticket_list():
        OLG_TICKETS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/events/all.json"
        response = requests.get(OLG_TICKETS_ENDPOINT, verify=False).text
        return json.loads(response)['events']['eventList']
