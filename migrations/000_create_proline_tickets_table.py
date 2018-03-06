from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Date, MetaData, Time
from datetime import datetime

import os

db = create_engine(os.environ['DATABASE_URL'])
meta = MetaData(db)
proline_tickets_table = Table('proline_tickets', meta,
    Column('id', Integer, primary_key=True),
    Column('created_at', Time, nullable=False, default=datetime.utcnow),
    Column('updated_at', Time, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
    Column('ticket_id', Integer),
    Column('date', Date))

with db.connect() as conn:
    proline_tickets_table.create()
