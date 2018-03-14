from sqlalchemy import create_engine
from sqlalchemy import MetaData

import os
import csv

db = create_engine(os.environ['DATABASE_URL'])
meta = MetaData(db, reflect=True)

tickets_table = meta.tables['proline_tickets']
games_table = meta.tables['proline_games']

with db.connect() as conn:
    games_csv = open('data/csv/backfill_games.csv')
    games = csv.DictReader(games_csv)
    for game in games:
        query = tickets_table.select().where(tickets_table.c.handle == game['ticket_handle']).limit(1)
        ticket_id = conn.execute(query).fetchone().id

        query = games_table.insert().values(
            ticket_id=ticket_id,
            game_handle=game['game_handle'],
            cutoff_date=game['cuttoff_date'],
            home=game['home'],
            visitor=game['visitor'],
            sport=game['sport'],
            outcomes=game['outcomes'],
            v_plus=game['v+'],
            v=game['v'],
            t=game['t'],
            h=game['h'],
            h_plus=game['h+']
        )
        try:
            conn.execute(query)
        except Exception as e:
            print(e)
