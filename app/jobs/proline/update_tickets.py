from sqlalchemy import create_engine
from sqlalchemy import MetaData
from datetime import datetime

import os
import requests
import json
import time

class UpdateTickets(object):
    def __init__(self):
        db = create_engine(os.environ['DATABASE_URL'])
        meta = MetaData(db, reflect=True)
        self.tickets_table = meta.tables['proline_tickets']
        self.games_table = meta.tables['proline_games']
        self.conn = db.connect()

    def process(self):
        for ticket in self.fetch_ticket_list():
            self.create_ticket(ticket)

    def create_ticket(self, ticket_data):
        ticket_handle = int(ticket_data['listNumber'])
        ticket_date = datetime.fromtimestamp(ticket_data['listDate']/1000)

        try:
            query = self.tickets_table.insert().values(handle=ticket_handle, date=ticket_date)
            self.conn.execute(query)
        except Exception as e:
            print(e)

        query = self.tickets_table.select().where(self.tickets_table.c.handle == ticket_handle).limit(1)
        ticket_id = self.conn.execute(query).fetchone().id

        if ticket_id != None:
            for game_data in ticket_data['eventList']:
                self.create_game(ticket_id, game_data)
        else:
            print('missing ticket')

    def create_game(self, ticket_id, game_data):
        v_plus = float(game_data['odds']['vplus']) if game_data['odds']['vplus'] != None else 0.0
        v = float(game_data['odds']['v']) if game_data['odds']['v'] != None else 0.0
        t = float(game_data['odds']['t']) if game_data['odds']['t'] != None else 0.0
        h = float(game_data['odds']['h']) if game_data['odds']['h'] != None else 0.0
        h_plus = float(game_data['odds']['hplus']) if game_data['odds']['hplus'] != None else 0.0

        query = self.games_table.insert().values(
            ticket_id=ticket_id,
            game_handle=game_data['id'],
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
        try:
            self.conn.execute(query)
        except Exception as e:
            print(e)
        else:
            print(query)


    def fetch_ticket_list(self):
        OLG_TICKETS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/events/all.json"
        response = requests.get(OLG_TICKETS_ENDPOINT, verify=False).text
        return json.loads(response)['events']['eventList']

if __name__ == '__main__':
    UpdateTickets().process()
