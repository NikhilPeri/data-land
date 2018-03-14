from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, Date, MetaData, Time
from datetime import datetime

import os
import csv

db = create_engine(os.environ['DATABASE_URL'])
meta = MetaData(db, reflect=True)
tickets_table = meta.tables['proline_tickets']

with db.connect() as conn:
    tickets_csv = open('data/csv/backfill_tickets.csv')
    tickets = csv.DictReader(tickets_csv)
    for ticket in tickets:
        query = tickets_table.insert().values(handle=ticket['handle'], date=ticket['date'])
        conn.execute(query)
