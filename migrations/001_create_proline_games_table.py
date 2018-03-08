from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, Date, MetaData, Time
from datetime import datetime

import os

db = create_engine(os.environ['DATABASE_URL'])
meta = MetaData(db)
proline_games_table = Table('proline_games', meta,
                        Column('id',             Integer, primary_key=True),
                        Column('created_at',     Time, nullable=False, default=datetime.utcnow),
                        Column('updated_at',     Time, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
                        Column('ticket_id',      Integer),
                        Column('game_id',        Integer),
                        Column('cutoff',         Time),
                        Column('home_symbol',    String),
                        Column('visitor_symbol', String),
                        Column('home_name',      String),
                        Column('visitor_name',   String),
                        Column('sport',          String),
                        Column('outcome',        String),
                        Column('v_plus',         Float),
                        Column('v',              Float),
                        Column('h',              Float),
                        Column('h_plus',         Float)
                        )

with db.connect() as conn:
    proline_games_table.create()
