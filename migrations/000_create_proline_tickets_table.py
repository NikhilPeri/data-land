from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Date, MetaData

import os

db = create_engine(os.environ('DATABASE_URL'))
meta = MetaData(db)
proline_tickets_table = Table('proline_tickets', meta,
                        Column('id',         Integer, primary_key=True),
                        Column('created_at', DateTime, nullable=False, server_default=func.now()),
                        Column('updated_at', DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now()),
                        Column('ticket_id',  Integer)
                        Column('date',       Date))

with db.connect() as conn:
    proline_tickets_table.create()
