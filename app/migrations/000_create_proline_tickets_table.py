from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Index, Integer, Date, MetaData, Time
from datetime import datetime

import os

db = create_engine(os.environ['DATABASE_URL'])
meta = MetaData(db)
proline_tickets_table = Table('proline_tickets', meta,
    Column('id',         Integer, primary_key=True),
    Column('created_at', Time,    default=datetime.utcnow),
    Column('updated_at', Time,    default=datetime.utcnow, onupdate=datetime.utcnow),
    Column('handle',     Integer, nullable=False),
    Column('date',       Date,    nullable=False),
    Index('idx_handle_date', 'handle', 'date', unique=True)
    )

with db.connect() as conn:
    proline_tickets_table.create()
