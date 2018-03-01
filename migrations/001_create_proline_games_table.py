from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, DateTime, String, MetaData

import os

db = create_engine(os.environ('DATABASE_URL'))
meta = MetaData(db)
proline_games_table = Table('proline_games', meta,
                        Column('id',             Integer, primary_key=True),
                        Column('created_at'      DateTime, nullable=False, server_default=func.now()),
                        Column('updated_at'      DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now()),
                        Column('ticket_id',      Integer),
                        Column('game_id',        Integer),
                        Column('cutoff_date',    DateTime),
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
